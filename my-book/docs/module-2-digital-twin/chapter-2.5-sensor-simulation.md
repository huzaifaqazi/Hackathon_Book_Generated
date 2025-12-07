# Chapter 2.5: Sensor Simulation (LiDAR, Depth, IMU)

For a digital twin to be truly useful, it must accurately replicate the sensory input a physical robot would perceive. **Sensor simulation** is a critical component of building realistic digital twins, especially for humanoid robots that rely heavily on a diverse array of sensors for perception, localization, and navigation. In Gazebo, various plugins allow you to add virtual sensors that publish data over ROS 2 topics, mimicking their real-world counterparts.

This chapter will cover the simulation of three common types of robot sensors: LiDAR, Depth Cameras, and Inertial Measurement Units (IMUs).

## 1. LiDAR Simulation

**LiDAR (Light Detection and Ranging)** sensors measure distances to surrounding objects by emitting pulsed laser light and measuring the time it takes for the reflected light to return. They are crucial for mapping, localization (SLAM), and obstacle avoidance.

In Gazebo, LiDAR sensors are typically simulated using the `libgazebo_ros_ray_sensor.so` plugin (or sometimes `libgazebo_ros_laser.so` for older Gazebo versions). This plugin simulates a 2D or 3D laser scanner.

### Adding a LiDAR to your URDF (Conceptual)

To add a LiDAR to your humanoid's head or torso, you would define a new link (e.g., `lidar_link`) and attach a `<sensor>` element within a `<gazebo>` tag referencing that link.

```xml
<link name="lidar_link">
  <!-- Visual and Collision for the LiDAR unit -->
</link>

<joint name="head_to_lidar_joint" type="fixed">
  <parent link="head_link"/>
  <child link="lidar_link"/>
  <origin xyz="0.05 0 0.05" rpy="0 0 0"/> <!-- Position relative to head -->
</joint>

<gazebo reference="lidar_link">
  <sensor name="laser_sensor" type="ray">
    <pose>0 0 0 0 0 0</pose> <!-- Relative to lidar_link -->
    <visualize>true</visualize> <!-- Show simulated rays in Gazebo -->
    <update_rate>10.0</update_rate>
    <ray>
      <scan>
        <horizontal>
          <samples>720</samples>
          <resolution>1</resolution>
          <min_angle>-3.14</min_angle> <!-- -180 degrees -->
          <max_angle>3.14</max_angle>  <!-- +180 degrees -->
        </horizontal>
        <vertical> <!-- For a 3D LiDAR, add vertical scan properties -->
          <samples>1</samples>
          <min_angle>0</min_angle>
          <max_angle>0</max_angle>
        </vertical>
      </scan>
      <range>
        <min>0.1</min>
        <max>10.0</max>
        <resolution>0.01</resolution>
      </range>
      <noise>
        <type>gaussian</type>
        <mean>0.0</mean>
        <stddev>0.01</stddev>
      </noise>
    </ray>
    <plugin name="gazebo_ros_laser_controller" filename="libgazebo_ros_ray_sensor.so">
      <ros>
        <argument>~/out:=scan</argument>
        <namespace>/humanoid</namespace>
      </ros>
      <output_type>sensor_msgs/LaserScan</output_type>
      <frame_name>lidar_link</frame_name>
    </plugin>
  </sensor>
</gazebo>
```

-   **`<ray>`**: Defines the properties of the laser rays (horizontal/vertical samples, angles, ranges).
-   **`<plugin>`**: Specifies the Gazebo ROS plugin (`libgazebo_ros_ray_sensor.so`) that converts the simulated sensor data into a `sensor_msgs/LaserScan` (for 2D) or `sensor_msgs/PointCloud2` (for 3D) message and publishes it to a ROS 2 topic (e.g., `/humanoid/scan`).

## 2. Depth Camera Simulation

**Depth Cameras** (e.g., Intel RealSense, Microsoft Azure Kinect) provide both a standard color image and a depth map, where each pixel indicates the distance to the objects in the scene. They are vital for 3D perception, object manipulation, and environment reconstruction.

In Gazebo, depth cameras are simulated using the `libgazebo_ros_camera.so` plugin. This plugin can simulate various camera types, including RGB, depth, and RGB-D cameras.

### Adding a Depth Camera to your URDF (Conceptual)

Similar to LiDAR, you would define a `camera_link` and attach a `<sensor>` within a `<gazebo>` tag.

```xml
<link name="camera_link">
  <!-- Visual and Collision for the camera unit -->
</link>

<joint name="head_to_camera_joint" type="fixed">
  <parent link="head_link"/>
  <child link="camera_link"/>
  <origin xyz="0.05 0 0.08" rpy="0 0 0"/> <!-- Position relative to head -->
</joint>

<gazebo reference="camera_link">
  <sensor name="depth_camera_sensor" type="depth">
    <always_on>true</always_on>
    <update_rate>30.0</update_rate>
    <camera>
      <horizontal_fov>1.047</horizontal_fov> <!-- 60 degrees -->
      <image>
        <width>640</width>
        <height>480</height>
        <format>R8G8B8</format>
      </image>
      <clip>
        <near>0.1</near>
        <far>10</far>
      </clip>
      <noise>
        <type>gaussian</type>
        <mean>0.0</mean>
        <stddev>0.007</stddev>
      </noise>
    </camera>
    <plugin name="camera_controller" filename="libgazebo_ros_camera.so">
      <ros>
        <argument>rgb/image_raw:=rgb/image_raw</argument>
        <argument>rgb/camera_info:=rgb/camera_info</argument>
        <argument>depth/image_raw:=depth/image_raw</argument>
        <argument>depth/camera_info:=depth/camera_info</argument>
        <argument>depth/points:=depth/points</argument>
        <namespace>/humanoid/camera</namespace>
      </ros>
      <camera_name>depth_camera</camera_name>
      <frame_name>camera_link</frame_name>
      <hack_baseline>0.07</hack_baseline> <!-- Baseline between RGB and Depth sensors -->
    </plugin>
  </sensor>
</gazebo>
```

-   **`<sensor type="depth">`**: Specifies a depth camera.
-   **`<camera>`**: Defines camera intrinsics (FOV, resolution, clipping planes).
-   **`<plugin>`**: `libgazebo_ros_camera.so` publishes `sensor_msgs/Image` (RGB and Depth) and `sensor_msgs/PointCloud2` to topics like `/humanoid/camera/rgb/image_raw` and `/humanoid/camera/depth/points`.

## 3. IMU (Inertial Measurement Unit) Simulation

An **IMU** measures linear acceleration and angular velocity. It is fundamental for robot state estimation, balance control, and navigation, providing crucial data about the robot's orientation and motion.

In Gazebo, IMUs are simulated using the `libgazebo_ros_imu_sensor.so` plugin.

### Adding an IMU to your URDF (Conceptual)

Typically, an IMU is placed in the robot's base or torso link.

```xml
<link name="imu_link">
  <!-- Visual and Collision for the IMU unit, often simplified or omitted -->
</link>

<joint name="torso_to_imu_joint" type="fixed">
  <parent link="torso_link"/>
  <child link="imu_link"/>
  <origin xyz="0 0 0" rpy="0 0 0"/> <!-- Centered in torso -->
</joint>

<gazebo reference="imu_link">
  <sensor name="imu_sensor" type="imu">
    <always_on>true</always_on>
    <update_rate>100.0</update_rate>
    <visualize>false</visualize>
    <imu>
      <orientation>
        <x>
          <noise type="gaussian">
            <mean>0.0</mean>
            <stddev>2e-4</stddev>
            <bias_mean>0.0</bias_mean>
            <bias_stddev>0.0000075</bias_stddev>
          </noise>
        </x>
        <!-- Similar noise definitions for y and z -->
      </orientation>
      <angular_velocity>
        <x>
          <noise type="gaussian">
            <mean>0.0</mean>
            <stddev>2e-4</stddev>
            <bias_mean>0.0</bias_mean>
            <bias_stddev>0.0000075</bias_stddev>
          </noise>
        </x>
        <!-- Similar noise definitions for y and z -->
      </angular_velocity>
      <linear_acceleration>
        <x>
          <noise type="gaussian">
            <mean>0.0</mean>
            <stddev>1.7e-2</stddev>
            <bias_mean>0.1</bias_mean>
            <bias_stddev>0.001</bias_stddev>
          </noise>
        </x>
        <!-- Similar noise definitions for y and z -->
      </linear_acceleration>
    </imu>
    <plugin name="imu_plugin" filename="libgazebo_ros_imu_sensor.so">
      <ros>
        <argument>~/out:=imu</argument>
        <namespace>/humanoid/imu</namespace>
      </ros>
      <frame_name>imu_link</frame_name>
      <initial_orientation_as_reference>false</initial_orientation_as_reference>
    </plugin>
  </sensor>
</gazebo>
```

-   **`<sensor type="imu">`**: Specifies an IMU sensor.
-   **`<imu>`**: Defines IMU-specific properties like sensor noise for orientation, angular velocity, and linear acceleration. This is crucial for realistic sensor data.
-   **`<plugin>`**: `libgazebo_ros_imu_sensor.so` publishes `sensor_msgs/Imu` messages to topics like `/humanoid/imu/imu`.

## Conclusion

By carefully integrating LiDAR, depth camera, and IMU sensor plugins into your humanoid URDF, you can create a highly realistic digital twin in Gazebo. These simulated sensors provide essential data streams over ROS 2 topics, allowing you to develop and test perception, localization, and control algorithms just as you would with a physical robot. Accurate sensor simulation is a foundational element for bridging the reality gap and enabling successful deployment of AI-powered robots.
