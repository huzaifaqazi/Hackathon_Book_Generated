# Chapter 2.6: Building Interactive Scenes in Gazebo/Unity

The effectiveness of a humanoid digital twin is significantly enhanced by the complexity and interactivity of its environment. Robots don't operate in a vacuum; they navigate, manipulate objects, and interact with dynamic elements. This chapter focuses on creating rich, interactive scenes in both Gazebo and Unity, enabling more realistic and challenging simulation scenarios for your humanoid robot.

## 1. Scene Construction in Gazebo

Gazebo worlds are defined using SDF (Simulation Description Format) files (as briefly introduced in Chapter 2.2). These XML files allow you to place models, define lighting, set physics properties, and include plugins to create dynamic environments.

### 1.1. Static and Dynamic Models

-   **Static Models**: Objects that do not move or interact physically (e.g., walls, furniture, terrain features). They are defined with `<static>true</static>`.
-   **Dynamic Models**: Objects that can move and interact physically with the robot (e.g., blocks, balls, doors, other robots). They are defined with `<static>false</static>` (or by default if not specified).

You can use pre-existing models from the Gazebo Model Database or import custom 3D models (e.g., `.dae`, `.stl`).

### 1.2. Adding Models to a World File

To include models in your Gazebo world, use the `<include>` tag within the `<world>` element of your `.world` file.

```xml
<sdf version="1.7">
  <world name="humanoid_lab">
    <include>
      <uri>model://sun</uri>
    </include>
    <include>
      <uri>model://ground_plane</uri>
    </include>

    <!-- Include a table -->
    <include>
      <uri>model://table</uri>
      <name>my_table</name>
      <pose>1 0 0 0 0 0</pose>
    </include>

    <!-- Include a box that the robot can interact with -->
    <include>
      <uri>model://box</uri>
      <name>my_box</name>
      <pose>1 0.5 0.8 0 0 0</pose>
    </include>

    <!-- Custom model (assuming it's in a package accessible to Gazebo) -->
    <include>
      <uri>model://my_custom_obstacle</uri>
      <name>custom_obstacle_1</name>
      <pose>-1 -1 0 0 0 0</pose>
    </include>

    <!-- Your humanoid robot would be spawned separately via ROS 2 launch file -->

    ... (other world properties)
  </world>
</sdf>
```

### 1.3. Custom Models

For custom obstacles, furniture, or interactive elements:

1.  **Create 3D Model**: Use CAD software (Blender, SolidWorks) to create a 3D model.
2.  **Export Meshes**: Export as `.stl` (for collision) and `.dae` (COLLADA for visual).
3.  **Create Model Directory**: Organize your model files (`model.sdf`, `model.config`, meshes, textures) in a structured directory.
4.  **Make Model Discoverable**: Place your model directory where Gazebo can find it (e.g., in `~/.gazebo/models` or within a ROS 2 package's `share` directory, then set `GAZEBO_MODEL_PATH`).

### 1.4. Dynamic Scene Elements via ROS 2

You can dynamically add or remove models from a Gazebo simulation using ROS 2 services. The `gazebo_ros` package provides services like `/spawn_entity` to add models from URDF/SDF strings. This is useful for tasks where objects appear or disappear.

## 2. Interactive Scene Design in Unity

Unity's visual editor and component-based architecture make it intuitive to build rich, interactive 3D scenes.

### 2.1. Importing Assets

-   **3D Models**: Import `.fbx`, `.obj`, `.blend`, or `.dae` files for environments, furniture, and objects. Unity can handle complex meshes and apply materials.
-   **Textures and Materials**: Apply realistic textures and create custom materials (e.g., PBR materials) to enhance visual fidelity.
-   **Terrain**: Use Unity's built-in Terrain Editor to create landscapes with heights, textures, and foliage.

### 2.2. Creating Interactive Objects

-   **Physics Components**: Add `Rigidbody` components to objects you want to interact physically. Add `Collider` components (Box Collider, Sphere Collider, Mesh Collider) to define their collision bounds.
-   **Scripts for Behavior**: Attach C# scripts to GameObjects to define their behavior:
    -   **Triggers**: Use `OnTriggerEnter`, `OnTriggerExit` to detect when the robot enters/leaves an area (e.g., entering a designated zone).
    -   **Interactive Elements**: Implement logic for doors that open, buttons that can be pressed, or objects that respond to the robot's manipulation.
-   **Lighting and Post-Processing**:
    -   **Lights**: Use various light sources (directional, point, spot) to create realistic illumination.
    -   **Post-Processing Stack**: Apply effects like Bloom, Ambient Occlusion, Depth of Field, and Color Grading to achieve photorealistic rendering.

### 2.3. Connecting Interactive Elements to ROS 2

For interactive scenes in Unity, you'll often need to communicate events back to your ROS 2 control system.

-   **Publishing Events**: If a virtual button is pressed in Unity, a script can publish a custom ROS 2 message (e.g., `std_msgs/msg/Bool` or a custom service call) to inform your robot's behavior controller.
-   **Subscribing to Robot State**: Unity can subscribe to the robot's pose from ROS 2 to update its visual representation in the Unity scene, especially if the primary physics simulation is in Gazebo.
-   **Feedback Mechanisms**: When the robot performs an action (e.g., picks up an object), Unity can play an animation, particle effect, or update a UI element.

### 2.4. Example: Simple Interactive Button in Unity

1.  **Create a 3D Cube**: Representing a button. Add a `BoxCollider` (set as Trigger) and a `Rigidbody`.
2.  **Attach Script**: Create a C# script (e.g., `RosButtonPublisher.cs`):

    ```csharp
    using UnityEngine;
    using RosMessageTypes.Std; // Assuming you have std_msgs generated
    using Unity.Robotics.ROSTCPConnector; // From Unity Robotics Hub

    public class RosButtonPublisher : MonoBehaviour
    {
        ROSConnection ros;
        public string topicName = "/humanoid/button_pressed";
        public bool isPressed = false;

        void Start()
        {
            ros = ROSConnection.Get = new ROSConnection("127.0.0.1", 50000, "Unity", topicName);
            ros.RegisterPublisher<BoolMsg>(topicName);
        }

        void OnTriggerEnter(Collider other)
        {
            if (other.CompareTag("RobotHand")) // Assuming robot hand has this tag
            {
                isPressed = true;
                ros.Publish(topicName, new BoolMsg(true));
                Debug.Log("Button Pressed!");
            }
        }

        void OnTriggerExit(Collider other)
        {
            if (other.CompareTag("RobotHand"))
            {
                isPressed = false;
                ros.Publish(topicName, new BoolMsg(false));
                Debug.Log("Button Released!");
            }
        }
    }
    ```
3.  **Tag Robot Hand**: Ensure your humanoid robot's hand collider in Unity has the tag "RobotHand".

Now, when the simulated robot's hand touches the button in Unity, a `BoolMsg` will be published to `/humanoid/button_pressed` via ROS 2.

## Conclusion

Building interactive scenes is a crucial step towards creating engaging and functional digital twins for humanoid robots. Whether leveraging Gazebo's physics and model database or Unity's visual fidelity and HRI tools, the ability to create rich environments with interactive elements allows for more comprehensive testing, training, and demonstration of complex robotic behaviors.
