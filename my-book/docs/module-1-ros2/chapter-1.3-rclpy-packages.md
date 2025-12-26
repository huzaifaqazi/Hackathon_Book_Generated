# Chapter 1.3: Building ROS 2 Python Packages with rclpy

In ROS 2, all code is organized into **packages**. A package is a directory that contains source code, build scripts, configuration files, and other resources that together provide a specific piece of functionality. For Python-based ROS 2 applications, we use `rclpy`, the Python client library for ROS 2.

This chapter will guide you through creating your first ROS 2 Python package, defining a simple node, and establishing basic communication using topics.

## 1. Creating a ROS 2 Package

The `ros2 pkg create` command is used to create a new ROS 2 package. For Python packages, we specify the `--build-type ament_python`.

First, ensure you are in your ROS 2 workspace `src` directory (e.g., `~/ros2_ws/src`). If you don't have a workspace, create one:

```bash
mkdir -p ~/ros2_ws/src
cd ~/ros2_ws/src
```

Now, create the package:

```bash
ros2 pkg create --build-type ament_python humanoid_control_py
```

This command creates a directory `humanoid_control_py` with a basic structure:

```
humanoid_control_py/
├── package.xml
├── setup.py
├── setup.cfg
├── resource/
└── humanoid_control_py/  # Python module directory
    └── __init__.py
```

-   **`package.xml`**: Contains metadata about the package (name, description, version, maintainer, dependencies).
-   **`setup.py`**: A standard Python `setuptools` file, crucial for defining how your Python code is installed and what executables (nodes) it provides.
-   **`setup.cfg`**: Configuration file for `setuptools`.
-   **`resource/`**: Can contain various resources, often used for marking installable files.
-   **`humanoid_control_py/`**: This is your main Python module directory, where your Python source files will reside.

## 2. Defining Dependencies in `package.xml`

Open `package.xml` and add `rclpy` as a dependency. You'll typically find placeholder comments; ensure `rclpy` is listed under `<depend>` tags:

```xml
<package format="3">
  ...
  <depend>rclpy</depend>
  ...
</package>
```

Also, ensure the `setup.py` and `setup.cfg` are correctly configured. By default, `ros2 pkg create` sets up a minimal `setup.py` and `setup.cfg` for Python packages.

## 3. Creating a Simple ROS 2 Node (Publisher)

Navigate into your package's Python module directory:

```bash
cd ~/ros2_ws/src/humanoid_control_py/humanoid_control_py
```

Create a new Python file, e.g., `simple_publisher.py`, that publishes a simple message to a topic. We'll use the `std_msgs.msg.String` message type.

```python
# simple_publisher.py
import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class SimplePublisher(Node):

    def __init__(self):
        super().__init__('simple_publisher')
        self.publisher_ = self.create_publisher(String, 'humanoid_chatter', 10)
        timer_period = 0.5  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.i = 0

    def timer_callback(self):
        msg = String()
        msg.data = 'Hello from Humanoid ROS 2! %d' % self.i
        self.publisher_.publish(msg)
        self.get_logger().info('Publishing: "%s"' % msg.data)
        self.i += 1

def main(args=None):
    rclpy.init(args=args) # Initialize ROS 2 communication
    simple_publisher = SimplePublisher() # Create the node
    rclpy.spin(simple_publisher) # Keep the node alive until Ctrl+C
    simple_publisher.destroy_node() # Destroy the node explicitly
    rclpy.shutdown() # Shut down ROS 2 communication

if __name__ == '__main__':
    main()
```

## 4. Registering the Node as an Executable

For ROS 2 to be able to find and run your node, you need to register it in your `setup.py` file. Open `~/ros2_ws/src/humanoid_control_py/setup.py` and modify the `entry_points` dictionary within `setuptools.setup()` to include your executable:

```python
from setuptools import find_packages, setup

package_name = 'humanoid_control_py'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name + '/resource', ['resource/humanoid_control_py']),
        ('share/' + package_name, ['launch/simple_launch.py']), # Example for launch files later
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='your_name', # Replace with your name
    maintainer_email='your_email@example.com', # Replace with your email
    description='A basic ROS 2 Python package for humanoid control concepts',
    license='Apache-2.0', # Or your chosen license
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'simple_publisher = humanoid_control_py.simple_publisher:main',
        ],
    },
)
```

**Important**: Make sure to replace `your_name` and `your_email@example.com` with your actual details.

## 5. Building Your Package

After modifying `setup.py`, you need to build your workspace. Navigate to the root of your ROS 2 workspace (`~/ros2_ws/`) and run `colcon build`:

```bash
cd ~/ros2_ws/
colcon build --packages-select humanoid_control_py
```

After a successful build, source your workspace to make the new package available:

```bash
source install/setup.bash
```

## 6. Running Your Node

Now you can run your `simple_publisher` node:

```bash
ros2 run humanoid_control_py simple_publisher
```

You should see messages being published to the console. To verify that messages are indeed being published to a topic, open a new terminal (and remember to source your workspace again: `source ~/ros2_ws/install/setup.bash`) and run:

```bash
ros2 topic list
ros2 topic echo /humanoid_chatter
```

You should see `/humanoid_chatter` in the list of topics and the messages published by your node echoing in the terminal.

## 7. Creating a Simple ROS 2 Node (Subscriber)

To demonstrate communication, let's create a simple subscriber node in the same `humanoid_control_py` Python module directory (`~/ros2_ws/src/humanoid_control_py/humanoid_control_py`). Create a new Python file, e.g., `simple_subscriber.py`:

```python
# simple_subscriber.py
import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class SimpleSubscriber(Node):

    def __init__(self):
        super().__init__('simple_subscriber')
        self.subscription = self.create_subscription(
            String,
            'humanoid_chatter',
            self.listener_callback,
            10)
        self.subscription  # prevent unused variable warning

    def listener_callback(self, msg):
        self.get_logger().info('I heard: "%s"' % msg.data)

def main(args=None):
    rclpy.init(args=args)
    simple_subscriber = SimpleSubscriber()
    rclpy.spin(simple_subscriber)
    simple_subscriber.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

## 8. Registering the Subscriber Node

Update `~/ros2_ws/src/humanoid_control_py/setup.py` again to register the new `simple_subscriber`:

```python
...
    entry_points={
        'console_scripts': [
            'simple_publisher = humanoid_control_py.simple_publisher:main',
            'simple_subscriber = humanoid_control_py.simple_subscriber:main', # Add this line
        ],
    },
)
```

## 9. Rebuild and Run Subscriber

Rebuild your package and source your workspace:

```bash
cd ~/ros2_ws/
colcon build --packages-select humanoid_control_py
source install/setup.bash
```

Now, run both nodes in separate terminals (remember to source in each new terminal):

**Terminal 1 (Publisher):**
```bash
ros2 run humanoid_control_py simple_publisher
```

**Terminal 2 (Subscriber):**
```bash
ros2 run humanoid_control_py simple_subscriber
```

You should now see the messages published by `simple_publisher` being received and echoed by `simple_subscriber`.

This foundational understanding of ROS 2 package creation and topic-based communication using `rclpy` is critical for developing more complex humanoid control systems, which we will delve into in the following chapters.
