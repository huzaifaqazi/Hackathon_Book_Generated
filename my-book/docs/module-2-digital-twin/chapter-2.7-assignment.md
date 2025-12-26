# Chapter 2.7: Assignment + Mini Project (Humanoid Digital Twin)

This assignment is the culminating project for Module 2, designed to solidify your understanding of digital twins, Gazebo physics, and Unity visualization. You will create a functional digital twin of a simple humanoid robot and demonstrate its interaction within a simulated environment.

## Project Goal

Develop a digital twin of a simple humanoid robot capable of:

1.  Being spawned into a Gazebo world with a defined environment.
2.  Accurately simulating physics, collisions, and gravity.
3.  Streaming sensor data (IMU, optional depth camera/LiDAR) via ROS 2 topics.
4.  Optionally, visualizing the robot and its environment in Unity with enhanced fidelity.

## Deliverables

1.  **ROS 2 Package(s)**:
    -   A `humanoid_digital_twin_description` package containing your humanoid URDF/Xacro model with Gazebo-specific extensions (inertial properties, collision geometries, Gazebo plugins for `ros2_control`, sensors).
    -   A `humanoid_digital_twin_control` package (Python) that includes a launch file to:
        -   Bring up Gazebo with your custom world and humanoid.
        -   Launch `robot_state_publisher` and `ros2_control` with appropriate controllers.
        -   Optionally, a simple ROS 2 node that subscribes to sensor data and performs a basic action (e.g., printing IMU data).
2.  **Gazebo World File**: A custom `.world` file defining a simple interactive environment (e.g., a ground plane, a few static obstacles like a table and a box).
3.  **Unity Project (Optional but Recommended)**: A Unity project that:
    -   Imports your humanoid URDF model.
    -   Subscribes to the robot's pose from ROS 2 (e.g., `/tf` data from `robot_state_publisher`) to visualize its movement.
    -   Optionally, publishes basic HRI events (e.g., a virtual button press) to a ROS 2 topic.
4.  **Report**: A concise report (700-1000 words) documenting:
    -   Your humanoid's URDF/SDF design choices, focusing on inertial and collision properties.
    -   The Gazebo world design and any custom models.
    -   Details on sensor simulation and ROS 2 topic streaming.
    -   If Unity is used, explain the integration and any HRI elements.
    -   Instructions on how to build and run your project.
    -   Screenshots of your humanoid in Gazebo and Unity (if applicable), and `ros2 topic echo` output for sensor data.
5.  **Video Demonstration (3-5 minutes)**: A video showcasing:
    -   Your humanoid spawning correctly in Gazebo.
    -   Its interaction with the environment (e.g., falling due to gravity, colliding with an obstacle).
    -   Real-time streaming of simulated sensor data.
    -   If Unity is used, the visual fidelity and any HRI components.

## Step-by-Step Guide

### Step 1: Humanoid URDF/SDF Refinement

-   **Start with your Module 1 Humanoid**: Take the URDF/Xacro model you developed in Module 1.
-   **Enhance Inertial Properties**: Ensure each link has realistic `mass`, `origin` (center of mass), and `inertia` values.
-   **Refine Collision Geometries**: Use simple, accurate `<collision>` shapes for all links to represent their physical bounds. Define friction and restitution if interacting with specific surfaces.
-   **Integrate `ros2_control`**: Verify `<transmission>` tags are correctly defined for all controllable joints.
-   **Add Gazebo Plugins**:
    -   `libgazebo_ros2_control.so`: To bridge `ros2_control` with Gazebo.
    -   Sensor Plugins: Add `<gazebo>` sensor blocks (LiDAR, depth camera, IMU) to relevant links, configuring them to publish data to ROS 2 topics (refer to Chapter 2.5).

### Step 2: Custom Gazebo World

-   **Create a new `.world` file**: Define a simple indoor or outdoor environment relevant to a humanoid robot.
-   **Include Basic Elements**: Start with `sun` and `ground_plane` models.
-   **Add Static Obstacles**: Include models like `table`, `chair`, `box` from the Gazebo Model Database, or create simple custom models. Position them strategically for interaction.
-   **Define Custom Materials (Optional)**: If you want specific friction/restitution properties for your ground or objects, define them within the `.world` file.

### Step 3: ROS 2 Control and Launch Package

-   **`humanoid_digital_twin_control` Package**: Create a Python package for your launch files and any simple nodes.
-   **Controllers Configuration**: Create a `config/` directory and define your `ros2_control` YAML file, including `joint_state_broadcaster` and appropriate joint controllers (e.g., `JointTrajectoryController`).
-   **Launch File (`humanoid_digital_twin.launch.py`)**:
    -   **Launch Gazebo**: Use `IncludeLaunchDescription` to launch Gazebo with your custom `.world` file.
    -   **Spawn Robot**: Use the `spawn_entity.py` node to spawn your humanoid.
    -   **Robot State Publisher**: Launch `robot_state_publisher` to publish the robot's TF frames.
    -   **`ros2_control`**: Launch `ros2_control_node` and load/start your controllers.
    -   **Sensor Data Monitor (Optional)**: A simple Python node that subscribes to your simulated sensor topics and prints incoming data to the console (e.g., IMU linear acceleration, LiDAR ranges).

### Step 4: Unity Integration (Optional but Recommended for Visual Fidelity)

-   **New Unity Project**: Create a new 3D Unity project.
-   **Unity Robotics Hub**: Install the Unity Robotics Hub packages (ROS TCP Connector, URDF Importer).
-   **Import URDF**: Import your `humanoid_digital_twin_description` URDF into Unity.
-   **ROS 2 Connection**: Set up the `ROSConnection` component in a Unity GameObject.
-   **Robot Visualization**: Write a C# script to subscribe to `/tf` messages (or specific joint state topics) from ROS 2 and apply the transformations to your Unity robot model.
-   **Basic HRI (Optional)**: Add a simple interactive element (e.g., a button in the Unity UI) that, when clicked, publishes a message to a ROS 2 topic, which your ROS 2 control nodes can respond to (e.g., make the robot wave).

### Step 5: Build, Run, and Document

1.  **Build**: `colcon build --packages-up-to humanoid_digital_twin_control`
2.  **Source**: `source install/setup.bash`
3.  **Launch**: `ros2 launch humanoid_digital_twin_control humanoid_digital_twin.launch.py`
4.  **Verify**:
    -   Does the robot spawn correctly in Gazebo?
    -   Does it react to gravity and collisions realistically?
    -   Are sensor topics publishing data (use `ros2 topic echo`)?
    -   (If Unity) Does the robot animate correctly in Unity? Does your HRI element work?

## Assessment Criteria

-   **Model Accuracy**: Quality of URDF/SDF, especially inertial and collision properties matching physical dimensions.
-   **Gazebo Simulation**: Stable physics, correct interaction with world elements, sensor data integrity.
-   **ROS 2 Integration**: Seamless data flow from simulated sensors to ROS 2 topics. `ros2_control` correctly configured.
-   **Environmental Design**: Thoughtful design of the Gazebo world with interactive elements.
-   **Unity Visualization (if included)**: Visual fidelity, accurate mirroring of Gazebo state, functional HRI elements.
-   **Report Quality**: Clear explanation of design choices, setup, and results.
-   **Video Demonstration**: Comprehensive showcase of the digital twin's functionality, sensor data, and interaction.

This assignment will provide you with a hands-on understanding of creating and utilizing digital twins, a critical skill for any modern robotics engineer.
