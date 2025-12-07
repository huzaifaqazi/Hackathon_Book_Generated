# Chapter 1.6: Validating Models in RViz and Gazebo

Once you have defined your humanoid robot's kinematics and physical properties using URDF (and optionally Xacro), the next crucial step is to validate that your model is correctly interpreted and behaves as expected. **RViz** is ROS 2's primary 3D visualization tool, and **Gazebo** is the go-to simulator for physics-based interaction. Together, they form an indispensable pair for developing and debugging robotic systems.

## 1. Visualizing Your Humanoid in RViz

**RViz** (ROS Visualization) is a powerful 3D visualizer for displaying sensor data, robot models, and other information from a ROS 2 system. It's essential for verifying the visual correctness of your URDF model, checking joint frames, and observing robot state.

### 1.1. Prerequisites

Ensure your `humanoid_description` package (or wherever your URDF is located) is built and sourced, and that `robot_state_publisher` is running (as typically done in a launch file, see Chapter 1.5).

```bash
# Example: If your URDF is in humanoid_description package
cd ~/ros2_ws
colcon build --packages-select humanoid_description
source install/setup.bash

# Manually run robot_state_publisher (often in a launch file)
# Replace 'humanoid.urdf.xacro' with your actual model file
# ros2 launch your_robot_launch_package robot_state_publisher_launch.py
# Or, if you just have a URDF file and want to quick check:
ros2 run robot_state_publisher robot_state_publisher --ros-args -p robot_description:="`xacro --inorder $(ros2 pkg prefix humanoid_description)/share/humanoid_description/urdf/humanoid.urdf.xacro`"
```
*Note: The `xacro` command needs to be executed to process `.xacro` files into `.urdf` XML. If you have a plain `.urdf` file, you can directly pass its content.*

### 1.2. Launching RViz

Open RViz in a new terminal:

```bash
rviz2
```

### 1.3. Configuring RViz for Your Robot

In the RViz interface:

1.  **Add `RobotModel`**: Click the "Add" button in the "Displays" panel (bottom left), select `RobotModel`, and click "OK".
    -   In the `RobotModel` properties, ensure the `Description Source` is set to `robot_description` (the default topic name for `robot_state_publisher` output).
2.  **Set `Fixed Frame`**: In the "Global Options" section (top left), set the `Fixed Frame` to `base_link` (or whatever the base link of your humanoid robot is named in your URDF). This is crucial for RViz to establish a coordinate system.
3.  **Add `JointStatePublisher` (for testing)**: If you don't have active joint controllers yet but want to manually manipulate the robot's pose in RViz, you can run a `joint_state_publisher_gui`.
    ```bash
    ros2 run joint_state_publisher_gui joint_state_publisher_gui
    ```
    This will create sliders for each joint, allowing you to move them and see the effect on your robot model in RViz.

If your URDF is correctly parsed and published, you should see your humanoid robot model appear in the 3D view. Rotate and pan the view to inspect the model from all angles. Look for:
-   **Correct Geometry**: Does the robot look like it should? Are meshes loaded correctly?
-   **Correct Joint Origins**: Do joints rotate around the expected points?
-   **Consistent Scale**: Are all parts of the robot scaled correctly?

## 2. Simulating Your Humanoid in Gazebo

**Gazebo** provides a rich environment for simulating robots under realistic physical conditions. It uses the information from your URDF (especially `<collision>` and `<inertial>` elements) to simulate gravity, contacts, and other physical interactions.

### 2.1. Prerequisites

Ensure your URDF model is ready for Gazebo simulation. This often means ensuring:
-   All links have valid `<inertial>` properties (mass, inertia matrix).
-   All links have valid `<collision>` geometries.
-   `<gazebo>` tags are added to your URDF (or xacro) to specify Gazebo-specific properties, such as plugins for sensors, materials, and controller interfaces.

### 2.2. Launching Gazebo with Your Humanoid

You will typically use a ROS 2 launch file to bring up Gazebo with your humanoid model. This launch file will:
1.  Start the Gazebo server (`gzserver`) and client (`gzclient`).
2.  Spawn your robot model into the Gazebo world.
3.  Load and start `ros2_control` and its controllers (as discussed in Chapter 1.5).

```python
# humanoid_gazebo_launch.py (conceptual)
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from ament_index_python.packages import get_package_share_directory
import os

def generate_launch_description():
    pkg_gazebo_ros = get_package_share_directory('gazebo_ros')
    pkg_humanoid_description = get_package_share_directory('humanoid_description')
    pkg_humanoid_control_py = get_package_share_directory('humanoid_control_py')

    # Path to your robot's URDF/xacro file
    robot_description_path = os.path.join(pkg_humanoid_description, 'urdf', 'humanoid.urdf.xacro')
    robot_description_content = os.popen(f'xacro {robot_description_path}').read()

    # Launch Gazebo
    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_gazebo_ros, 'launch', 'gazebo.launch.py')
        ),
        launch_arguments={'world': 'empty.world'}.items() # Or your custom world
    )

    # Spawn the robot in Gazebo
    spawn_entity = Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        arguments=['-topic', 'robot_description', '-entity', 'humanoid_robot'],
        output='screen'
    )

    # Robot State Publisher (from Chapter 1.5)
    robot_state_publisher_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[{'robot_description': robot_description_content}],
        output='screen'
    )

    # Controller Manager and controllers (from Chapter 1.5)
    # This might involve another IncludeLaunchDescription or direct Node actions
    humanoid_controllers_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_humanoid_control_py, 'launch', 'humanoid_control.launch.py') # Example controller launch
        )
    )

    return LaunchDescription([
        gazebo,
        spawn_entity,
        robot_state_publisher_node,
        humanoid_controllers_launch, # Includes controller manager and specific controllers
    ])
```

To run this launch file:

```bash
ros2 launch humanoid_control_py humanoid_gazebo_launch.py
```

### 2.3. Verifying Simulation Behavior

Once Gazebo is running with your humanoid model:
-   **Gravity**: Does the robot fall as expected if not supported?
-   **Contacts**: Does it interact realistically with the ground and other objects?
-   **Joint Limits**: Do joints respect the limits defined in your URDF?
-   **Controller Response**: If you publish commands to your robot's joint controllers (as described in Chapter 1.5), does the robot move as expected in Gazebo?
-   **Sensor Data**: Are simulated sensors (e.g., IMU, depth camera) publishing data on their respective ROS 2 topics? You can check this using `ros2 topic list` and `ros2 topic echo`.

## Conclusion

RViz and Gazebo are indispensable tools for validating your humanoid robot models. RViz provides a visual sanity check for your URDF, ensuring the kinematic structure and appearance are correct. Gazebo takes this further by simulating physical interactions, allowing you to test controllers and observe realistic robot behavior in a dynamic environment. With these tools, you can confidently iterate on your robot's design and control strategies.
