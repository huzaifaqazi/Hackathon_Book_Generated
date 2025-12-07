# Chapter 1.7: Assignment + Mini Project (Humanoid ROS Controller)

This assignment is the culmination of Module 1, designed to integrate your understanding of ROS 2 concepts, Python package development, URDF modeling, and inter-node communication. You will build a ROS 2 Python package to control a simulated humanoid robot, demonstrating your ability to orchestrate its movements.

## Project Goal

Develop a ROS 2 Python package that allows for basic control of a simulated humanoid robot's joints. Your solution should:

1.  Properly define a simple humanoid robot using URDF (or Xacro).
2.  Launch the robot in a Gazebo simulation environment.
3.  Implement a ROS 2 Python node that publishes commands to specific joints of the humanoid.
4.  Visualize the robot's movement in RViz.

## Deliverables

1.  **ROS 2 Package**: A complete ROS 2 Python package (e.g., `humanoid_controller_pkg`) containing:
    -   Your humanoid's URDF/Xacro description file (`.urdf` or `.xacro`).
    -   A Python node (`joint_commander.py`) that publishes joint commands.
    -   A Python launch file (`humanoid_control.launch.py`) to bring up all necessary components.
    -   `package.xml` and `setup.py` correctly configured.
2.  **Report**: A short report (500-800 words) detailing:
    -   Your URDF design choices (e.g., chosen joints, links, limits).
    -   How your `joint_commander.py` node works.
    -   Instructions on how to run your package.
    -   A screenshot of your robot moving in Gazebo and RViz.
3.  **Video Demonstration (2-3 minutes)**: A brief video showcasing your robot performing a simple movement sequence (e.g., waving an arm, nodding its head, or taking a single step).

## Step-by-Step Guide

### Step 1: Humanoid URDF/Xacro Model

-   **Create a `humanoid_description` Package**: If you haven't already, create a separate ROS 2 package for your robot's description (e.g., `ros2 pkg create --build-type ament_cmake humanoid_description`).
-   **Design Your Humanoid**: Start with a simple humanoid model. It doesn't need to be complex, but it should have at least:
    -   A `base_link`
    -   A `torso_link`
    -   At least one arm with shoulder, elbow, and wrist joints (revolute joints).
    -   A `head_link` with a neck joint.
-   **Define Links and Joints**: Use `<link>` and `<joint>` elements in your `.urdf` or `.xacro` file. Pay attention to:
    -   **`origin`**: Correctly position child links relative to parents.
    -   **`axis`**: Define the correct axis of rotation for revolute joints.
    -   **`limit`**: Set realistic `lower` and `upper` limits, `effort`, and `velocity` for each joint.
    -   **`<visual>` and `<collision>`**: Add basic geometries (boxes, cylinders) and materials for visualization and collision detection.
    -   **`<inertial>`**: Add basic mass and inertia values (even approximations are fine for this project).
-   **Add Gazebo Elements**: Include `<gazebo>` tags within your URDF for Gazebo-specific configurations, such as:
    -   `libgazebo_ros_init.so` and `libgazebo_ros_factory.so` plugins.
    -   `gazebo_ros2_control` plugin to connect `ros2_control` with Gazebo.
    -   `<transmission>` tags for each controllable joint.

### Step 2: ROS 2 Controller Package

-   **Create a `humanoid_controller_pkg`**: Create a Python ROS 2 package (e.g., `ros2 pkg create --build-type ament_python humanoid_controller_pkg --dependencies rclpy std_msgs geometry_msgs trajectory_msgs`).
-   **Controller Configuration**: Create a `config/` directory inside `humanoid_controller_pkg`. Define a YAML file (e.g., `humanoid_controllers.yaml`) that configures:
    -   `controller_manager`
    -   `joint_state_broadcaster`
    -   `joint_trajectory_controller` (or multiple `position_controllers/JointController` for individual joints) for your humanoid's joints.
-   **Python Joint Commander Node (`joint_commander.py`)**:
    -   Create a Python node that subscribes to some trigger (e.g., a timer, or a simple keyboard input) and publishes `JointTrajectory` messages to your `joint_trajectory_controller`.
    -   The `JointTrajectory` message should specify target positions for several joints over a short duration to create a simple movement (e.g., move arm up, then down).

### Step 3: Launch Files

-   **Primary Launch File (`humanoid_control.launch.py`)**: Create a Python launch file in your `humanoid_controller_pkg/launch/` directory that:
    -   Launches Gazebo with an empty world.
    -   Spawns your humanoid robot model using `spawn_entity.py` (topic should be `robot_description` from `robot_state_publisher`).
    -   Launches the `robot_state_publisher` node, processing your URDF/Xacro.
    -   Launches the `controller_manager` node and loads your `joint_state_broadcaster` and `joint_trajectory_controller` using parameters from your YAML file.
    -   Starts your `joint_commander.py` node.

### Step 4: Verification and Demonstration

1.  **Build Your Workspace**: After creating/modifying files, navigate to your workspace root (`~/ros2_ws`) and `colcon build --packages-up-to humanoid_controller_pkg`.
2.  **Source Setup Files**: `source install/setup.bash`.
3.  **Launch Your System**: `ros2 launch humanoid_controller_pkg humanoid_control.launch.py`.
4.  **Observe in Gazebo**: Verify that your robot appears, falls (if not balanced), and moves when your `joint_commander.py` node sends commands.
5.  **Observe in RViz**: Launch `rviz2` in a separate terminal. Configure `RobotModel` and `Fixed Frame` to visualize the robot's state and movement corresponding to Gazebo.
6.  **Record Video**: Capture a short video of your robot executing its programmed movement.

## Assessment Criteria

-   **URDF Correctness**: Well-formed URDF/Xacro with appropriate links, joints, limits, visual, collision, and inertial properties.
-   **Gazebo Integration**: Robot spawns correctly in Gazebo, respects physics (gravity, collisions).
-   **Controller Implementation**: Correct configuration of `ros2_control` and controllers.
-   **ROS 2 Node Functionality**: `joint_commander.py` effectively sends commands, and robot moves as intended.
-   **Launch File Orchestration**: All components launch seamlessly from a single launch file.
-   **Visualization**: Robot is correctly displayed and moves in RViz.
-   **Report Quality**: Clarity of explanations, accuracy of details, and proper screenshots.
-   **Video Demonstration**: Clear and concise demonstration of the robot's movement.

Good luck with your first humanoid ROS 2 controller! This project forms a strong foundation for all subsequent modules.
