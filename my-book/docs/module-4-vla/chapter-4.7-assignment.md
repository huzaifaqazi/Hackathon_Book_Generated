# Chapter 4.7: Assignment + Mini Project (LLM-Driven Humanoid Task)

This assignment is the capstone for Module 4 and, indeed, for the entire course. It challenges you to integrate all the concepts learned – ROS 2 control, digital twins, Isaac Sim perception, and Vision-Language-Action (VLA) systems – into a fully functional pipeline. You will empower a simulated humanoid robot to perform a multi-step task based on natural language commands.

## Project Goal

Develop an end-to-end VLA pipeline that enables a simulated humanoid robot in Isaac Sim to execute a multi-step task specified by natural language voice commands. Your solution should demonstrate the integration of:

1.  **Voice Command Extraction**: Using Whisper to convert spoken commands to text.
2.  **Cognitive Planning**: Employing an LLM to generate a high-level action plan from the text command.
3.  **Plan Translation**: Converting the LLM's plan into executable ROS 2 actions (e.g., navigation, manipulation).
4.  **Multi-modal Perception**: Leveraging Isaac ROS perception for object recognition and localization within the environment.
5.  **Humanoid Navigation and Control**: Guiding the humanoid robot through the simulated environment and interacting with objects.

## Recommended Task

Design a multi-step task that involves navigation to different locations and interaction with at least two distinct objects. For example:

-   "Robot, please go to the living room, pick up the red ball from the floor, then take it to the box in the corner and place it inside."

## Deliverables

1.  **Isaac Sim Project**: A complete Isaac Sim project with your humanoid robot and a suitable environment (e.g., a simple apartment layout with furniture and objects).
2.  **ROS 2 Package(s)**: A ROS 2 workspace containing all necessary packages, including:
    -   Your `humanoid_vla_pkg` (containing `whisper_asr_node`, `llm_cognitive_planner_node`, `plan_translation_node`).
    -   Packages for Isaac ROS perception and adapted Nav2 configuration from Module 3.
    -   Launch files to bring up the entire VLA pipeline.
3.  **Codebase**: Well-commented Python code for all custom ROS 2 nodes and scripts.
4.  **Report**: A detailed technical report (1000-1500 words) documenting:
    -   The overall VLA system architecture and data flow.
    -   Your design choices for each component (Whisper model, LLM prompting strategy, plan translation logic, perception modules).
    -   How natural language commands are grounded into executable robotic actions.
    -   Challenges encountered and solutions implemented.
    -   Instructions on how to set up, build, and run your entire VLA system.
    -   Screenshots of the robot executing the task in Isaac Sim and relevant ROS 2 topic visualizations (e.g., in RViz).
5.  **Video Demonstration (5-8 minutes)**: A comprehensive video demonstrating your humanoid robot successfully performing the chosen multi-step task based on a natural language voice command. The video should show the full pipeline in action, from voice input to robot execution.

## Step-by-Step Guide

### Step 1: Environment and Robot Setup (Isaac Sim)

-   **Isaac Sim Environment**: Create or adapt an Isaac Sim environment that is appropriate for your chosen task. Populate it with the necessary objects (e.g., a red ball, a box, a table).
-   **Humanoid Robot**: Ensure your humanoid robot model is correctly imported and configured in Isaac Sim, with its sensors (RGB-D, IMU) publishing to ROS 2 topics and its joints controllable via `ros2_control`.

### Step 2: Individual Component Implementation & Testing

Re-use and refine the components developed in previous chapters:

-   **`whisper_asr_node`**: Ensure it accurately transcribes voice commands. Test by speaking commands and echoing the `/humanoid/voice_command` topic.
-   **`llm_cognitive_planner_node`**: Refine your LLM prompts. Test with various commands to ensure it generates correct and robust multi-step action plans (e.g., in JSON or a consistent text format). Ensure the output is published to `/humanoid/llm_plan`.
-   **Isaac ROS Perception**: Verify that your Isaac ROS VSLAM and object detection modules are correctly configured and publishing accurate localization and object pose information.
-   **Nav2 Integration**: Confirm your adapted Nav2 setup for humanoid navigation is working in Isaac Sim. Test with simple `NavigateToPose` goals.
-   **Manipulation Action Server**: Implement a simplified manipulation action server for basic picking and placing. This server will receive a pick/place goal and translate it into `ros2_control` joint commands.

### Step 3: `plan_translation_node` Development

This is the central orchestrator:

-   **Subscribe to LLM Plan**: Receive the LLM's high-level action plan.
-   **Iterate and Execute Actions**: Loop through the LLM's planned actions.
-   **Grounding**:
    -   For `move_to(location)`: Translate `location` (e.g., "kitchen") into a `PoseStamped` goal for Nav2.
    -   For `find_object(object_name)`: Query your Isaac ROS object detection (e.g., via a ROS 2 service call) to get the 3D pose of the `object_name`.
    -   For `pick_up(object_name)`: Use the object's 3D pose to send a goal to your manipulation action server.
    -   For `place(object_name, location)`: Similar to `pick_up`, but for placing.
-   **Error Handling**: Implement basic error handling (e.g., if Nav2 fails, or object not found). You can publish feedback to a new ROS 2 topic for debugging or even to the LLM for re-planning.

### Step 4: Full Pipeline Orchestration with Launch Files

-   **`humanoid_vla_capstone.launch.py`**: Create a master launch file that brings up:
    -   Isaac Sim (via its own launch file).
    -   All Isaac ROS perception nodes.
    -   Your `whisper_asr_node`.
    -   Your `llm_cognitive_planner_node`.
    -   Your `plan_translation_node`.
    -   Your adapted Nav2 stack.
    -   Your manipulation action server.

### Step 5: Testing and Demonstration

1.  **Build and Source**: `colcon build` and `source install/setup.bash`.
2.  **Launch**: `ros2 launch humanoid_vla_pkg humanoid_vla_capstone.launch.py`.
3.  **Issue Voice Command**: Speak your chosen multi-step command clearly to the simulated robot.
4.  **Observe**: Monitor the robot's behavior in Isaac Sim, and check ROS 2 topics (e.g., `/humanoid/voice_command`, `/humanoid/llm_plan`, `/tf`, `/nav2/goal`) for debugging.
5.  **Record**: Capture your demonstration video.

## Assessment Criteria

-   **End-to-End Functionality**: Robot successfully completes the multi-step task based on voice command.
-   **Pipeline Integration**: Smooth and correct data flow and interaction between all VLA components.
-   **LLM Planning Quality**: LLM generates logical and executable plans for the task.
-   **Perception Accuracy**: Robot successfully identifies and localizes objects for manipulation.
-   **Navigation Robustness**: Humanoid navigates effectively through the environment.
-   **Code Quality**: Well-structured, commented, and Pythonic code.
-   **Report Quality**: Clear, comprehensive, and accurate documentation of the system.
-   **Video Demonstration**: Engaging and clear showcase of the VLA system's capabilities.

This final project is your chance to showcase your expertise in building truly intelligent and interactive humanoid robots. Good luck!
