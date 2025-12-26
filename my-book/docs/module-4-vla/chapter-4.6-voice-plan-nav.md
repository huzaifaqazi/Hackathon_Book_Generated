# Chapter 4.6: Building Voice → Plan → Navigation Pipelines

The journey through Vision-Language-Action (VLA) systems has introduced you to individual components: voice command extraction with Whisper, cognitive planning with LLMs, and multi-modal perception for object interaction. The true power of VLA, however, lies in integrating these elements into a cohesive, functional pipeline that enables a humanoid robot to execute complex tasks based on natural language commands.

This chapter will guide you through the process of architecting and building an end-to-end Voice → Plan → Navigation pipeline, demonstrating how these components interoperate within the ROS 2 framework.

## 1. The End-to-End VLA Pipeline Architecture

Consider a scenario where a human commands, "Robot, go to the kitchen and find the coffee mug on the table." Here's how a VLA pipeline typically processes this:

```mermaid
graph TD
    A[Human Voice Command] --> B(Whisper ASR Node);
    B -- Transcribed Text --> C[LLM Cognitive Planner Node];
    C -- High-level Plan (Function Calls) --> D[Plan Translation Node];
    D -- Navigation Goal --> E[Nav2 Action Server];
    E -- Velocity Commands --> F[Robot Control (ros2_control)];
    F --> G[Humanoid Robot (Isaac Sim)];
    G -- Visual/IMU Feedback --> H[Isaac ROS Perception Nodes];
    H -- Environment State --> D;
    H -- Environment State --> E;
    D -- Manipulation Actions --> I[Manipulation Action Server];
    I -- Joint Commands --> F;
```

**Key Stages:**

1.  **Voice Input (Human)**: A human issues a command.
2.  **Speech-to-Text (Whisper)**: The `whisper_asr_node` (Chapter 4.2) captures the audio, transcribes it, and publishes the text to a ROS 2 topic (e.g., `/humanoid/voice_command`).
3.  **Cognitive Planning (LLM)**: An `llm_cognitive_planner_node` (Chapter 4.3) subscribes to the transcribed text. It uses an LLM (via API or local inference) to understand the intent and generate a high-level plan as a sequence of symbolic actions (e.g., `move_to(kitchen)`, `find_object(coffee_mug)`, `pick_up(coffee_mug)`, `navigate_to(home_location)`). This plan is published to another ROS 2 topic (e.g., `/humanoid/llm_plan`).
4.  **Plan Translation/Grounding**: The `plan_translation_node` (Chapter 4.4) subscribes to the LLM's plan. This node is responsible for:
    -   **Grounding**: Translating abstract LLM actions into specific ROS 2 commands (e.g., `move_to(kitchen)` becomes a `NavigateToPose` action goal for Nav2).
    -   **Perception Queries**: Interacting with Isaac ROS perception nodes (Chapter 3.4, Chapter 4.5) to identify and localize objects or verify locations (e.g., "Where is the coffee mug?").
    -   **Action Orchestration**: Sending goals to ROS 2 action servers (e.g., Nav2 `NavigateToPose`, or custom manipulation action servers).
    -   **Error Handling**: If an action fails, it can inform the LLM or prompt the human for clarification.
5.  **Perception (Isaac ROS)**: Isaac ROS perception nodes (Chapter 3.4) continuously process sensor data from the humanoid (simulated in Isaac Sim or real) to provide:
    -   **Localization**: The robot's current pose in the map.
    -   **Object Detection/Pose Estimation**: 3D location and identity of objects (Chapter 4.5).
    -   **Scene Understanding**: Information about the environment.
    This information is published to relevant ROS 2 topics and consumed by Nav2 and the `plan_translation_node`.
6.  **Navigation (Nav2)**: Nav2 (Chapter 3.6), possibly adapted for humanoid locomotion, receives navigation goals from the `plan_translation_node` and generates velocity commands or footstep plans.
7.  **Robot Control (`ros2_control`)**: The low-level `ros2_control` framework (Chapter 1.5) and its controllers execute the velocity commands or joint trajectories, making the humanoid move.
8.  **Physical Humanoid (or Isaac Sim)**: The commands are executed on the simulated robot in Isaac Sim, which provides visual and sensor feedback to the perception nodes, completing the loop.

## 2. Implementing the Pipeline Components (Python in ROS 2)

Each stage of the VLA pipeline will typically be implemented as one or more ROS 2 Python nodes.

### 2.1. `whisper_asr_node` (from Chapter 4.2)

-   **Input**: Microphone audio stream.
-   **Output**: `std_msgs/msg/String` to `/humanoid/voice_command`.

### 2.2. `llm_cognitive_planner_node` (from Chapter 4.3)

-   **Input**: `std_msgs/msg/String` from `/humanoid/voice_command`.
-   **Output**: `std_msgs/msg/String` (e.g., JSON string representing a list of actions) to `/humanoid/llm_plan`.
-   **Internal Logic**:
    -   Uses LLM API (GPT, Claude) or local LLM inference.
    -   Leverages prompt engineering to define robot capabilities and expected output format.

### 2.3. `plan_translation_node` (from Chapter 4.4)

-   **Input**: `std_msgs/msg/String` from `/humanoid/llm_plan`.
-   **Output**: Goal messages to various ROS 2 Action Clients (Nav2, manipulation, etc.).
-   **Internal Logic**:
    -   Parses LLM plan.
    -   Communicates with perception service (e.g., `find_object` service providing `geometry_msgs/PoseStamped` for a detected object).
    -   Creates and sends `NavigateToPose.Goal()` to Nav2 action client.
    -   Creates and sends `Pick.Goal()` or `Place.Goal()` to custom manipulation action clients.
    -   Handles action server responses and feedback.

### 2.4. Isaac ROS Perception Nodes (from Chapter 3.4)

-   **Input**: Sensor data from Isaac Sim (e.g., `/humanoid/camera/rgb/image_raw`, `/humanoid/camera/depth/points`, `/humanoid/imu/imu`).
-   **Output**: `nav_msgs/Odometry`, TF transforms, `vision_msgs/Detection3DArray` (for detected objects).
-   **Nodes**: `visual_slam_node`, `segmentation_node`, `object_detection_node`, etc.

### 2.5. Nav2 Stack (from Chapter 3.6)

-   **Input**: `NavigateToPose.Goal()` from `plan_translation_node`, odometry from VSLAM, costmap updates from perception nodes.
-   **Output**: Velocity commands for the robot (or footstep plans for humanoid-adapted Nav2).

### 2.6. Humanoid Control (from Chapter 1.5)

-   **Input**: Velocity commands or joint trajectories from Nav2 / manipulation action servers.
-   **Output**: Joint commands to the simulated humanoid in Isaac Sim.

## 3. Orchestrating the Pipeline with Launch Files

A master Python launch file (`humanoid_vla.launch.py`) will orchestrate all these components.

```python
# humanoid_vla.launch.py (conceptual)
from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
import os
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():
    pkg_humanoid_vla = get_package_share_directory('humanoid_vla_pkg') # Your VLA package
    pkg_humanoid_isaac_nav = get_package_share_directory('humanoid_isaac_nav') # Nav/Isaac package
    pkg_humanoid_isaac_ros_perception = get_package_share_directory('isaac_ros_perception_pkg') # Placeholder for Isaac ROS launches

    # 1. Launch Isaac Sim with Humanoid Robot and Sensors (conceptual)
    # This would typically be a complex launch file from your Isaac Sim project
    isaac_sim_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(os.path.join(
            pkg_humanoid_isaac_nav, 'launch', 'humanoid_isaac_sim.launch.py' # Spawns robot, configures sensors
        ))
    )

    # 2. Launch Whisper ASR Node
    whisper_node = Node(
        package='humanoid_vla_pkg',
        executable='whisper_asr_node',
        name='whisper_asr_node',
        output='screen',
        parameters=[{'whisper_model_name': 'small'}]
    )

    # 3. Launch LLM Cognitive Planner Node
    llm_planner_node = Node(
        package='humanoid_vla_pkg',
        executable='llm_cognitive_planner_node',
        name='llm_cognitive_planner_node',
        output='screen',
        # Parameters for API keys, model names, etc.
    )

    # 4. Launch Plan Translation Node
    plan_translation_node = Node(
        package='humanoid_vla_pkg',
        executable='plan_translation_node',
        name='plan_translation_node',
        output='screen',
        # Parameters for known locations, object mappings, etc.
    )

    # 5. Launch Isaac ROS Perception (VSLAM, Object Detection, etc.)
    # This would likely be another IncludeLaunchDescription that brings up multiple nodes
    isaac_ros_perception_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(os.path.join(
            pkg_humanoid_isaac_ros_perception, 'launch', 'perception_pipeline.launch.py'
        ))
    )

    # 6. Launch Nav2 Stack (Humanoid Adapted)
    # This would be an IncludeLaunchDescription of your customized Nav2 setup
    humanoid_nav2_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(os.path.join(
            pkg_humanoid_isaac_nav, 'launch', 'humanoid_nav2_bringup.launch.py' # Your Nav2 config
        ))
    )

    return LaunchDescription([
        isaac_sim_launch,
        whisper_node,
        llm_planner_node,
        plan_translation_node,
        isaac_ros_perception_launch,
        humanoid_nav2_launch,
    ])
```

## 4. Debugging and Validation

Building such a complex pipeline requires rigorous testing and debugging at each stage:

-   **Component Testing**: Verify each node (Whisper, LLM planner, plan translator) works independently.
-   **Communication Testing**: Use `ros2 topic echo`, `ros2 node info`, `ros2 graph` to check data flow and connectivity between nodes.
-   **Grounding Validation**: Ensure the robot's perception accurately maps to the LLM's understanding of objects and locations.
-   **Plan Execution Testing**: Execute small segments of the LLM-generated plan to verify robot behaviors.
-   **Error Recovery**: Test how the system handles failures at various stages.

## Conclusion

Building an end-to-end Voice → Plan → Navigation pipeline integrates all the advanced components of a VLA system. By carefully designing each ROS 2 node, leveraging Isaac Sim for realistic simulation, Isaac ROS for accelerated perception, and LLMs for cognitive planning, you can empower your humanoid robot to understand and execute complex natural language commands. This complete pipeline is a significant step towards developing truly intelligent and interactive humanoid robotics.
