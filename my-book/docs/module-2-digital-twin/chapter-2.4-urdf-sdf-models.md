# Chapter 2.4: Creating Humanoid URDF/SDF Models

In Module 1, we introduced URDF as the fundamental format for describing robot kinematics. For digital twins in environments like Gazebo and Unity, further refinement and specific considerations are necessary when creating humanoid URDF (Unified Robot Description Format) and SDF (Simulation Description Format) models to ensure accurate simulation and visualization.

## 1. URDF vs. SDF: A Deeper Dive for Simulation

While URDF is widely used in ROS for robot descriptions, **SDF (Simulation Description Format)** is often preferred by physics simulators like Gazebo. SDF offers a more comprehensive way to describe worlds and models, including:

-   **World Definition**: SDF can describe entire environments, including static objects, dynamic objects, and environmental properties (lights, ground plane). URDF is limited to a single robot.
-   **Joint Loops**: SDF natively supports joint loops, which are common in more complex robot designs (e.g., parallel manipulators, certain humanoid leg designs). URDF is strictly a tree structure.
-   **Physics Properties**: SDF provides more explicit and granular control over physics properties like friction, damping, and collision parameters directly within the model definition.
-   **Nested Models**: SDF supports nested models, allowing you to compose complex simulations from simpler, reusable components.

However, URDF remains prevalent in the ROS ecosystem, and many tools (like `xacro` and `ros_to_sdf`) exist to convert URDF models to SDF for use in Gazebo. For this course, we'll primarily focus on creating robust URDF models, understanding that they will be implicitly converted or enhanced for simulation.

## 2. Refining Humanoid URDF for Digital Twins

When creating URDF models for digital twins, consider the following refinements beyond basic kinematic descriptions:

### 2.1. Accurate Inertial Properties

The `<inertial>` tag in each link is critical for realistic physics simulation.

-   **Mass (`<mass>` tag)**: Accurately estimate or measure the mass of each link. Incorrect masses will lead to unrealistic gravitational effects and dynamics.
-   **Inertia Matrix (`<inertia>` tags)**: The inertia tensor (`ixx`, `ixy`, `ixz`, `iyy`, `iyz`, `izz`) describes how mass is distributed around a link's center of mass. This is vital for simulating rotational dynamics. Use CAD software or estimation techniques to get these values as accurately as possible.
-   **Center of Mass (`<origin>` within `<inertial>`)**: The origin of the inertial frame should correspond to the link's center of mass. This often differs from the link's geometric center.

### 2.2. Detailed Collision Geometries

As discussed in Chapter 2.2, collision geometries are distinct from visual geometries and are used by the physics engine.

-   **Simplicity vs. Accuracy**: Use the simplest possible shapes (boxes, spheres, cylinders) that accurately approximate the physical bounds of each link. Overly complex collision meshes significantly increase computation time.
-   **Joint Limits & Interpenetration**: Ensure your collision models prevent links from interpenetrating in physically impossible ways, especially at joint limits.
-   **Material Properties**: In `<collision>` (or sometimes directly in `<gazebo>` extensions to URDF), define material properties like `<friction>` (`mu`, `mu2`) and `<restitution>` for realistic contact behavior.

### 2.3. Visual Properties for Realism

While Unity will handle high-fidelity rendering, accurate visual descriptions in URDF are still important for tools like RViz and for basic visual correctness in Gazebo.

-   **Meshes**: Use `.dae` (COLLADA) or `.stl` files for complex geometries. Ensure correct scaling and origin in your CAD software before export.
-   **Textures and Materials**: While URDF `<material>` tags support basic colors, you might need Gazebo-specific extensions or Unity's material system for advanced textures and shaders.

### 2.4. `ros2_control` Integration

Ensure your URDF includes the necessary `<transmission>` tags for each joint that will be controlled by `ros2_control`. This maps your robot's mechanical structure to the software interfaces. Refer back to Chapter 1.5 for details.

## 3. Gazebo-Specific Extensions to URDF

To fully leverage Gazebo's capabilities, you often add `<gazebo>` tags within your URDF or Xacro file. These tags are ignored by ROS tools but are parsed by Gazebo.

### 3.1. Physics Properties (`<gazebo reference="link_name">`)

You can specify additional physics properties for individual links:

```xml
<gazebo reference="base_link">
  <mu1>0.2</mu1>  <!-- Friction coefficient for link surface -->
  <mu2>0.2</mu2>
  <kp>1000000.0</kp> <!-- Contact stiffness -->
  <kd>1.0</kd>    <!-- Contact damping -->
  <maxVel>0.1</maxVel>
  <minDepth>0.001</minDepth>
</gazebo>
```

### 3.2. Sensor Plugins (`<gazebo reference="link_name">`)

You can attach simulated sensors directly to links using Gazebo plugins. We'll cover this in more detail in the next chapter.

```xml
<gazebo reference="head_link">
  <sensor name="camera" type="camera">
    <always_on>true</always_on>
    <update_rate>30.0</update_rate>
    <camera>
      <horizontal_fov>1.047</horizontal_fov>
      <image>
        <width>640</width>
        <height>480</height>
        <format>R8G8B8</format>
      </image>
      <clip>
        <near>0.1</near>
        <far>100</far>
      </clip>
    </camera>
    <plugin name="camera_controller" filename="libgazebo_ros_camera.so">
      <ros>
        <namespace>/humanoid</namespace>
        <argument>camera/image_raw:=image</argument>
        <argument>camera/camera_info:=camera_info</argument>
      </ros>
      <camera_name>head_camera</camera_name>
      <frame_name>head_camera_link</frame_name>
    </plugin>
  </sensor>
</gazebo>
```

### 3.3. Controller Plugins (`<gazebo>`)

A crucial plugin for integrating `ros2_control` with Gazebo is `libgazebo_ros2_control.so`. This plugin should be added to your top-level `<robot>` tag or a base link.

```xml
<gazebo>
  <plugin name="gazebo_ros2_control" filename="libgazebo_ros2_control.so">
    <parameters>robot_controllers.yaml</parameters>
  </plugin>
</gazebo>
```

This plugin reads controller configurations (from the specified YAML file, e.g., `robot_controllers.yaml`) and exposes the hardware interfaces to `ros2_control`.

## 4. Modeling Workflow

A typical workflow for humanoid model creation and refinement for digital twins involves:

1.  **CAD Design**: Design your humanoid robot in a CAD software (e.g., SolidWorks, Fusion 360).
2.  **Export Meshes**: Export visual and collision meshes (e.g., `.stl`, `.dae`).
3.  **Calculate Inertial Properties**: Use CAD tools to calculate mass, center of mass, and inertia matrix for each link.
4.  **Initial URDF**: Create a basic URDF with links, joints, and initial visual properties.
5.  **Add `ros2_control` Transmissions**: Include `<transmission>` tags.
6.  **Add Gazebo Extensions**: Augment the URDF with `<gazebo>` tags for physics properties, sensor plugins, and the `gazebo_ros2_control` plugin.
7.  **Xacro for Modularity**: Use Xacro to manage complexity and reusability, especially for repetitive structures like fingers or complex legs.
8.  **Validation**: Continuously validate your model in RViz (visuals, kinematics) and Gazebo (physics, control, sensors).

## Conclusion

Creating accurate and well-defined URDF/SDF models is the cornerstone of effective digital twins for humanoid robots. By carefully defining inertial, collision, and visual properties, and integrating Gazebo-specific extensions, you can build a realistic simulated counterpart that accurately reflects the physical robot's behavior, enabling robust testing and development.
