# Chapter 1.4: Humanoid Modeling with URDF

To effectively control and simulate humanoid robots in ROS 2, we need a standardized way to describe their physical and kinematic properties. This is where **URDF (Unified Robot Description Format)** comes into play. URDF is an XML-based file format used in ROS to describe all elements of a robot, including its visual appearance, collision properties, kinematic structure, and dynamics.

## 1. What is URDF?

URDF defines a robot as a tree-like structure of **links** (rigid bodies) connected by **joints**. It's a fundamental concept for:

-   **Visualization**: Displaying the robot in tools like RViz.
-   **Kinematics/Dynamics**: Performing calculations for robot motion and forces.
-   **Simulation**: Providing a model for physics engines in simulators like Gazebo.
-   **Control**: Defining the structure that `ros2_control` interfaces with.

While URDF is excellent for defining the robot's structure, it has some limitations, particularly for simulation (e.g., no explicit support for loops in the kinematic chain, no collision detection between links defined in the same URDF). For more advanced simulation descriptions, **SDF (Simulation Description Format)** is often used, particularly by Gazebo. However, URDF remains a widely used format, and tools exist to convert URDF to SDF.

## 2. Basic URDF Structure

A URDF file starts with a `<robot>` tag, which contains `<link>` and `<joint>` elements.

```xml
<?xml version="1.0"?>
<robot name="humanoid_robot">

  <!-- Define Links here -->
  <link name="base_link">
    ...
  </link>

  <!-- Define Joints here -->
  <joint name="base_to_torso_joint" type="revolute">
    ...
  </joint>

</robot>
```

## 3. Links: The Robot's Body Segments

A `<link>` element describes a rigid body segment of the robot. Key components within a link include:

-   **`<visual>`**: Defines the visual appearance of the link.
    -   `<geometry>`: Shape (box, cylinder, sphere, mesh). For humanoids, often a `<mesh>` pointing to a `.dae` (COLLADA) or `.stl` file.
    -   `<material>`: Color and texture.
-   **`<collision>`**: Defines the collision properties of the link. This is crucial for physics simulation. Often uses simpler geometry than visual for computational efficiency.
-   **`<inertial>`**: Defines the mass, center of mass, and inertia matrix of the link. Essential for realistic physics simulation.

**Example Link (Simplified):**

```xml
<link name="torso_link">
  <visual>
    <geometry>
      <box size="0.2 0.4 0.6"/>
    </geometry>
    <material name="blue">
      <color rgba="0 0 0.8 1"/>
    </material>
  </visual>
  <collision>
    <geometry>
      <box size="0.2 0.4 0.6"/>
    </geometry>
  </collision>
  <inertial>
    <mass value="10.0"/>
    <inertia ixx="1.0" ixy="0.0" ixz="0.0" iyy="1.0" iyz="0.0" izz="1.0"/>
  </inertial>
</link>
```

## 4. Joints: Connecting Links

A `<joint>` element describes how two links are connected and their relative motion.

-   **`name`**: Unique identifier for the joint.
-   **`type`**: Specifies the joint's movement. Common types for humanoids:
    -   `revolute`: Rotational joint with a limited range (e.g., elbow, knee).
    -   `continuous`: Rotational joint with unlimited range (e.g., wheel, not common for humanoids).
    -   `prismatic`: Translational joint with a limited range (e.g., linear actuator, not common for humanoids).
    -   `fixed`: No motion between links (e.g., connecting two rigid parts of a hand).
-   **`<parent link="link_name"/>`**: The link that the joint is attached to.
-   **`<child link="link_name"/>`**: The link that moves relative to the parent.
-   **`<origin xyz="x y z" rpy="roll pitch yaw"/>`**: Defines the joint's position and orientation relative to the parent link's origin.
-   **`<axis xyz="x y z"/>`**: Defines the axis of rotation for revolute/continuous joints or translation for prismatic joints.
-   **`<limit lower="val" upper="val" effort="val" velocity="val"/>`**: Defines the joint's movement limits, maximum effort, and maximum velocity. Crucial for realistic humanoid movement and control.
-   **`<dynamics friction="val" damping="val"/>`**: Defines friction and damping properties for physics simulation.

**Example Joint (Simplified Revolute):**

```xml
<joint name="torso_to_head_joint" type="revolute">
  <parent link="torso_link"/>
  <child link="head_link"/>
  <origin xyz="0 0 0.3" rpy="0 0 0"/> <!-- Head origin 0.3m above torso origin -->
  <axis xyz="0 0 1"/> <!-- Rotates around Z-axis -->
  <limit lower="-1.57" upper="1.57" effort="100" velocity="10"/> <!-- +/- 90 degrees -->
</joint>
```

## 5. Transmissions: Connecting Joints to Actuators

For robots controlled by `ros2_control`, the `<transmission>` tag (often defined in a separate `xacro` file or included within the URDF) maps joints to actuators. This is essential for simulating and controlling the physical motors that drive the robot's joints.

```xml
<transmission name="torso_to_head_trans">
  <type>transmission_interface/SimpleTransmission</type>
  <joint name="torso_to_head_joint">
    <hardwareInterface>hardware_interface/PositionJointInterface</hardwareInterface>
  </joint>
  <actuator name="head_motor">
    <hardwareInterface>hardware_interface/PositionJointInterface</hardwareInterface>
    <mechanicalReduction>1</mechanicalReduction>
  </actuator>
</transmission>
```

-   **`type`**: Specifies the type of transmission (e.g., `SimpleTransmission` for a 1:1 mapping).
-   **`<joint>`**: References the joint being controlled.
-   **`<hardwareInterface>`**: Specifies how the joint is controlled (e.g., position, velocity, effort).
-   **`<actuator>`**: Represents the physical motor.

## 6. Xacro: Simplifying URDF

Writing complex URDF files can be tedious and repetitive. **Xacro (XML Macros)** is an XML macro language that allows you to use variables, mathematical expressions, and conditional logic within your URDF, making it more modular and readable. ROS 2 tools automatically parse xacro files into standard URDF.

**Example Xacro usage (conceptual):**

```xml
<!-- my_humanoid.xacro -->
<?xml version="1.0"?>
<robot name="humanoid_robot" xmlns:xacro="http://ros.org/xacro">

  <xacro:property name="PI" value="3.14159"/>
  <xacro:property name="TORSO_MASS" value="10.0"/>

  <xacro:macro name="standard_joint" params="name parent child axis_xyz">
    <joint name="${name}" type="revolute">
      <parent link="${parent}"/>
      <child link="${child}"/>
      <origin xyz="0 0 0" rpy="0 0 0"/>
      <axis xyz="${axis_xyz}"/>
      <limit lower="-${PI/2}" upper="${PI/2}" effort="100" velocity="10"/>
    </joint>
  </xacro:macro>

  <link name="base_link"/>

  <link name="torso_link">
    <inertial>
      <mass value="${TORSO_MASS}"/>
      ...
    </inertial>
    ...
  </link>

  <xacro:standard_joint name="base_to_torso_joint" parent="base_link" child="torso_link" axis_xyz="0 0 1"/>
  <!-- More links and joints -->

</robot>
```

In this example, `xacro:property` defines constants, and `xacro:macro` allows us to define reusable joint structures. This greatly simplifies the creation of humanoid models with many similar joints.

## Conclusion

Understanding URDF (and optionally Xacro) is fundamental for defining your humanoid robot's physical characteristics, enabling its accurate visualization, simulation, and control within the ROS 2 ecosystem. In the next chapter, we'll dive into building actual ROS 2 Python packages that interact with these models.
