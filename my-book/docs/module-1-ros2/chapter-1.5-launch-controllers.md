# Chapter 1.5: Launching Controllers and Inter-node Communication

In the previous chapters, we learned about ROS 2 fundamentals, how to create Python packages, and how to define a humanoid robot using URDF. Now, we'll bring these concepts together by understanding how to launch and manage multiple ROS 2 nodes, particularly those responsible for controlling a humanoid robot's joints, and how these nodes communicate effectively.

## 1. ROS 2 Launch Files: Orchestrating Nodes

As robot systems become more complex, manually starting each node in separate terminals becomes impractical. ROS 2 **Launch Files** provide a way to define and run multiple nodes and processes simultaneously with a single command. Launch files are typically written in Python, but can also be in XML. We will focus on Python launch files for their flexibility.

A launch file allows you to:
-   Start multiple nodes.
-   Set parameters for nodes.
-   Include other launch files.
-   Remap topic names.
-   Define conditionals for node execution.

### Basic Python Launch File Structure

A Python launch file uses the `launch` and `launch_ros` packages.

```python
# my_robot_launch.py
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='humanoid_control_py',
            executable='simple_publisher',
            name='my_publisher',
            output='screen',
            emulate_tty=True, # Required for displaying stdout in terminal
        ),
        Node(
            package='humanoid_control_py',
            executable='simple_subscriber',
            name='my_subscriber',
            output='screen',
            emulate_tty=True,
        ),
        # Add more nodes as needed
    ])
```

To run this launch file:

```bash
ros2 launch humanoid_control_py my_robot_launch.py
```

### Passing Parameters

Nodes often require parameters. You can pass them directly in the launch file.

```python
# my_node_with_params_launch.py
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='my_pkg',
            executable='my_node',
            name='my_configurable_node',
            parameters=[
                {'my_parameter': 'some_value'},
                {'another_param': 1.23}
            ],
            output='screen',
            emulate_tty=True,
        ),
    ])
```

## 2. `ros2_control`: Hardware Abstraction and Controller Management

`ros2_control` is a powerful framework within ROS 2 designed for controlling robot hardware. It provides a structured way to:

-   **Interface with Hardware**: Abstract away the low-level details of communicating with motors, sensors, and other robot hardware.
-   **Manage Controllers**: Load, unload, start, and stop various types of controllers (e.g., position controllers, velocity controllers, effort controllers).
-   **Standardize Robot Control**: Provides a consistent API for different robot types and manufacturers.

For humanoid robots, `ros2_control` is invaluable for managing the numerous joints and their respective controllers.

### Key Concepts in `ros2_control`

-   **Hardware Interfaces**: These are the software components that communicate directly with your robot's physical hardware. They expose "joint states" (position, velocity, effort) and accept "joint commands."
-   **Controllers**: These are the algorithms that take desired states (e.g., a target joint position) and convert them into commands that the hardware interfaces can execute. Common controllers include `JointStateBroadcaster`, `PositionController`, `VelocityController`, `EffortController`.
-   **Controller Manager**: A central node that loads, configures, and runs controllers. It acts as an intermediary between the controllers and the hardware interfaces.

### Example: Launching `ros2_control` for a Humanoid (Conceptual)

Integrating `ros2_control` with your humanoid URDF typically involves:

1.  **Defining Transmissions in URDF/Xacro**: As discussed in Chapter 1.4, `<transmission>` tags link your robot's joints to hardware interfaces.
2.  **Controller Configuration YAML**: A YAML file specifying which controllers to load and their parameters.
3.  **Launch File**: A Python launch file that starts:
    -   The `robot_state_publisher` (to publish TF frames from URDF).
    -   The `controller_manager` node.
    -   The specific controllers (e.g., `JointStateBroadcaster`, `PositionController` for each joint).

```yaml
# controllers.yaml (example)
controller_manager:
  ros__parameters:
    update_rate: 100 # Hz

humanoid_joint_state_broadcaster:
  ros__parameters:
    type: joint_state_broadcaster/JointStateBroadcaster

left_arm_controller:
  ros__parameters:
    type: position_controllers/JointGroupPositionController
    joints:
      - left_shoulder_joint
      - left_elbow_joint
      - left_wrist_joint
```

```python
# humanoid_control_launch.py (conceptual)
from launch import LaunchDescription
from launch_ros.actions import Node
import os
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():
    # Path to your robot's URDF/xacro file
    robot_description_path = os.path.join(
        get_package_share_directory('humanoid_description'), # Assuming a humanoid_description package
        'urdf',
        'humanoid.urdf.xacro'
    )

    # Convert xacro to URDF
    robot_description_content = os.popen(f'xacro {robot_description_path}').read()

    # Robot State Publisher node
    robot_state_publisher_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[{'robot_description': robot_description_content}],
        output='screen'
    )

    # Controller Manager node
    controller_manager_node = Node(
        package='controller_manager',
        executable='ros2_control_node',
        parameters=[os.path.join(
            get_package_share_directory('humanoid_control_py'),
            'config',
            'controllers.yaml' # Your controllers config file
        )],
        output='screen'
    )

    # Load and start the controllers (e.g., joint state broadcaster, position controller)
    # You would typically use a separate action or service call within the launch file
    # to load and activate these. For simplicity, we assume they are configured in controllers.yaml
    # and started by the controller_manager.

    return LaunchDescription([
        robot_state_publisher_node,
        controller_manager_node,
        # Potentially a separate node to manually load/start controllers if not automatic
    ])
```

## 3. Inter-Node Communication for Humanoid Actions

Once controllers are launched, other ROS 2 nodes can communicate with them to command robot actions.

-   **Topics for Joint Commands**: `ros2_control` typically exposes topics (e.g., `/joint_trajectory_controller/joint_trajectory`) for commanding joint positions over time. Your high-level behavior nodes can publish to these topics.
-   **Services for Controller Management**: Services are used to load, unload, switch, and list controllers.
-   **Actions for Complex Tasks**: For more complex, long-duration tasks like walking or reaching, ROS 2 Actions are ideal. A behavior node would send a goal to an "ArmManipulation" action server, which in turn commands the underlying joint controllers.

### Example: Commanding a Joint (Conceptual)

A Python node could publish to a `JointGroupPositionController` topic to move a specific arm joint.

```python
# arm_commander_node.py (conceptual)
import rclpy
from rclpy.node import Node
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint
from builtin_interfaces.msg import Duration

class ArmCommander(Node):
    def __init__(self):
        super().__init__('arm_commander')
        self.publisher_ = self.create_publisher(JointTrajectory, '/left_arm_controller/joint_trajectory', 10)
        self.timer = self.create_timer(1.0, self.send_arm_command)

    def send_arm_command(self):
        joint_trajectory_msg = JointTrajectory()
        joint_trajectory_msg.joint_names = ['left_shoulder_joint', 'left_elbow_joint', 'left_wrist_joint']

        point = JointTrajectoryPoint()
        point.positions = [0.5, 0.2, 0.0] # Target joint positions
        point.time_from_start = Duration(sec=1, nanosec=0) # Reach in 1 second
        joint_trajectory_msg.points.append(point)

        self.publisher_.publish(joint_trajectory_msg)
        self.get_logger().info('Sending arm command')

def main(args=None):
    rclpy.init(args=args)
    arm_commander = ArmCommander()
    rclpy.spin(arm_commander)
    arm_commander.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

This node, when run, would publish desired joint positions to the `left_arm_controller`, making the simulated humanoid arm move.

## Conclusion

ROS 2 launch files provide the necessary infrastructure to bring up a complex humanoid robot system. Combined with `ros2_control` for managing joint controllers, and the various inter-node communication mechanisms (Topics, Services, Actions), you have a powerful toolkit to orchestrate your humanoid's behavior. The next step is to visualize and validate these models and their movements in simulation environments like RViz and Gazebo.
