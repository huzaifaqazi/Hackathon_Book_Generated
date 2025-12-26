# Chapter 1.2: Nodes, Topics, Services, and Actions

In ROS 2, effective communication between different parts of a robot's software system is paramount. This communication is facilitated by a set of fundamental concepts: **Nodes**, **Topics**, **Services**, and **Actions**. Understanding these building blocks is crucial for developing any ROS 2 application, especially for complex systems like humanoid robots.

## 1. Nodes: The Executable Units

At the heart of a ROS 2 system are **Nodes**. A node is essentially an executable process that performs a specific, focused task. Think of a node as a single, self-contained program responsible for one piece of functionality.

**Examples in Humanoid Robotics:**
-   A node to read data from a depth camera.
-   A node to calculate inverse kinematics for an arm.
-   A node to control the joint positions of the robot's left leg.
-   A node to interpret voice commands.

**Key Characteristics:**
-   **Modularity**: Nodes encourage breaking down complex robot software into smaller, manageable, and reusable components.
-   **Isolation**: Each node typically runs as an independent process, providing fault isolation. If one node crashes, it ideally doesn't bring down the entire robot system.
-   **Concurrency**: Multiple nodes can run concurrently, allowing the robot to perform various tasks simultaneously.

## 2. Topics: Asynchronous Data Streaming

**Topics** are the primary mechanism for asynchronous, one-way streaming of data in ROS 2. They operate on a publish/subscribe model, where nodes can publish messages to a topic, and other nodes can subscribe to that topic to receive those messages.

**How it Works:**
-   **Publisher**: A node that sends messages to a topic.
-   **Subscriber**: A node that receives messages from a topic.
-   **Message Type**: All messages published on a given topic must conform to a specific message type (e.g., `sensor_msgs/msg/Image` for camera data, `geometry_msgs/msg/Twist` for velocity commands).

**Examples in Humanoid Robotics:**
-   A camera node publishes images to `/camera/image_raw` topic.
-   A LiDAR node publishes point clouds to `/scan` topic.
-   A navigation stack publishes velocity commands (e.g., `cmd_vel`) to control the robot's base.
-   A joint state publisher node publishes the current positions of all robot joints to `/joint_states`.
-   A behavior node subscribes to `/joint_states` to monitor the robot's pose.

**Key Features:**
-   **Loose Coupling**: Publishers and subscribers don't need to know about each other directly. They only need to agree on the topic name and message type.
-   **Broadcast**: Messages published on a topic are received by all active subscribers to that topic.
-   **Real-time Data**: Ideal for continuous streams of data like sensor readings, joint states, or velocity commands.

## 3. Services: Synchronous Request/Response

**Services** provide a mechanism for synchronous, two-way communication in ROS 2, following a request/response model. A client node sends a request to a service, and a server node performs an action and sends back a response.

**How it Works:**
-   **Client**: A node that sends a request and waits for a response.
-   **Server**: A node that receives a request, processes it, and sends a response.
-   **Service Type**: Both request and response messages for a service must conform to a predefined service type.

**Examples in Humanoid Robotics:**
-   A client node requests a humanoid's current pose from a "pose_estimator" service.
-   A client node asks a "reset_robot" service to move the robot to a home position.
-   A client node queries a "motion_planner" service to compute a safe trajectory to a target.

**Key Features:**
-   **Synchronous**: The client blocks and waits for the server's response.
-   **Reliable**: Designed for operations that need a confirmed outcome.
-   **Discrete Tasks**: Best suited for single, well-defined operations rather than continuous data streams.

## 4. Actions: Asynchronous Goal-Based Tasks

**Actions** are a higher-level communication mechanism in ROS 2, designed for long-running, goal-based tasks that may require feedback during execution and the ability to be cancelled. They combine aspects of both Topics and Services.

**How it Works:**
-   **Action Client**: Sends a goal request, can receive continuous feedback, and gets a final result. Can also cancel the goal.
-   **Action Server**: Receives a goal, provides continuous feedback as it executes, and sends a final result upon completion. Can also preempt (cancel) an active goal.
-   **Action Type**: Defines the structure for the Goal, Feedback, and Result messages.

**Examples in Humanoid Robotics:**
-   An action client sends a goal to a "walk" action server to move the humanoid to a specific coordinate. The client can receive feedback on the humanoid's progress (e.g., current position, remaining distance) and cancel the walk if needed.
-   An action client sends a goal to a "pick_and_place" action server to manipulate an object. Feedback could include the current state of the gripper or detected object.

**Key Features:**
-   **Asynchronous (non-blocking client)**: The client doesn't block while waiting for the result; it can do other work and check for feedback.
-   **Feedback**: Provides continuous updates on the progress of a long-running task.
-   **Preemptable**: Goals can be cancelled by the client before completion.
-   **Long-running Tasks**: Ideal for complex behaviors like navigation, manipulation, or performing sequences of operations.

## Summary

| Feature   | Communication Pattern     | Use Case                                     | Examples                                                                     |
| :-------- | :------------------------ | :------------------------------------------- | :--------------------------------------------------------------------------- |
| **Nodes** | Executable unit           | Encapsulate specific functionality           | Camera driver, joint controller, navigation planner                          |
| **Topics**| Asynchronous, one-way     | Continuous data streams                      | Sensor data, joint states, velocity commands                                 |
| **Services**| Synchronous, request/response | Discrete, confirmed operations               | Reset robot pose, query current state, trigger a specific function             |
| **Actions**| Asynchronous, goal-based  | Long-running tasks with feedback and preemption | Humanoid walking to a target, complex manipulation sequence                  |

In the next chapter, we will learn how to implement these communication mechanisms by building our own ROS 2 Python packages using `rclpy`.
