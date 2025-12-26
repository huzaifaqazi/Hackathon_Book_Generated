# Chapter 4.4: Natural Language → ROS 2 Action Plans

In the previous chapter, we explored how Large Language Models (LLMs) can generate high-level cognitive plans from natural language commands. The critical next step in a Vision-Language-Action (VLA) system is to translate these abstract, human-understandable plans into concrete, executable sequences of **ROS 2 actions** that a humanoid robot can perform. This involves bridging the gap between symbolic AI (LLM output) and robotic control.

This chapter will detail the process of converting natural language-driven cognitive plans into structured ROS 2 action plans, ensuring that the robot can robustly execute human instructions.

## 1. The Challenge of Plan Grounding

The output from an LLM is typically text-based, describing a sequence of actions like `pick_up(mug)` or `move_to(kitchen)`. For a robot, these are high-level abstractions. The challenge, known as **plan grounding**, is to:

1.  **Map abstract actions to robot capabilities**: `pick_up` means using specific manipulators, sensors, and low-level joint commands. `move_to` involves navigation, gait generation, and balance control.
2.  **Resolve ambiguities**: "Mug" needs to be grounded to a specific object detected by the robot's vision system. "Kitchen" needs to be grounded to a known location in the robot's map.
3.  **Handle context**: The same command might mean different things in different situations.

## 2. Architecture for Plan Translation

A dedicated **Plan Translation Module** (or **Action Grounding Module**) acts as the interface between the LLM's cognitive plan and the robot's low-level control systems. This module often sits within a ROS 2 node and interacts with other ROS 2 components.

```mermaid
graph TD
    A[LLM Cognitive Plan (Text)] --> PT[Plan Translation Module];
    PT -- Query --> P[Perception Module (Isaac ROS)];
    PT -- Query --> M[Motion Planner (Nav2)];
    PT -- Execute ROS 2 Actions --> RC[Robot Control Systems];
    RC --> HR[Humanoid Robot];
    P -- Feedback --> PT;
    M -- Feedback --> PT;
    PT -- Status/Confirmation --> LLM;
```

## 3. Designing a Plan Translation Module

This module is typically implemented as a ROS 2 Python node that:

1.  **Subscribes to LLM Plan Topic**: Receives the text-based action plan from the LLM node (which previously received transcribed voice commands).
2.  **Parses the LLM Output**: Extracts the action names and their parameters from the LLM's structured output.
3.  **Grounds Actions**: Translates abstract actions into a sequence of calls to specific ROS 2 actions, services, or topic publications.
4.  **Manages Execution Flow**: Executes actions sequentially, handles success/failure, and provides feedback to the LLM or a human operator.

### Example: Translating `pick_up(mug)`

Let's assume the LLM outputs `pick_up(mug)`. The plan translation module would:

1.  **Receive**: The text "pick_up(mug)".
2.  **Perceive**: Call the Perception Module (e.g., via a ROS 2 service `find_object(object_name='mug')`) to get the 3D pose of the nearest mug.
3.  **Plan Manipulation**: Call a Manipulation Planner (e.g., a ROS 2 action server for `MoveIt`) with the mug's pose and the robot's current state to generate a sequence of joint movements for grasping.
4.  **Execute**: Send the joint trajectory to the `JointTrajectoryController` (from Module 1) via a ROS 2 action client.
5.  **Verify**: Use force sensors or vision to confirm the mug is grasped.

## 4. Converting LLM Plan to ROS 2 Action Calls (Python Example)

Consider an LLM outputting a list of "function calls." Your Python `plan_translator_node` would parse and execute these.

```python
# plan_translator_node.py
import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from action_msgs.msg import GoalStatus
from geometry_msgs.msg import PoseStamped # For navigation goals
from manipulation_msgs.action import Pick # Example custom action type
from nav2_msgs.action import NavigateToPose # Nav2 action

class PlanTranslatorNode(Node):
    def __init__(self):
        super().__init__('plan_translator_node')
        self.llm_plan_subscription = self.create_subscription(
            String,
            '/humanoid/llm_plan',
            self.llm_plan_callback,
            10
        )
        self.get_logger().info("Plan Translator Node initialized. Waiting for LLM plans...")

        # Initialize ROS 2 Action Clients (conceptual)
        self.nav_to_pose_client = self.create_action_client(
            NavigateToPose,
            '/navigate_to_pose'
        )
        self.pick_action_client = self.create_action_client(
            Pick, # Custom action for picking
            '/humanoid/pick_object'
        )
        # Add other action clients as needed (place, say, etc.)

    def llm_plan_callback(self, msg):
        llm_plan_text = msg.data
        self.get_logger().info(f"Received LLM plan: {llm_plan_text}")
        
        # Simple parsing (can be made more robust)
        actions = self.parse_llm_plan(llm_plan_text)

        # Execute actions sequentially
        self.execute_robot_actions(actions)

    def parse_llm_plan(self, plan_text):
        # Implement logic to parse LLM text into a list of (action_name, params) tuples
        # Example: "move_to(kitchen), pick_up(mug)" -> [("move_to", "kitchen"), ("pick_up", "mug")]
        parsed_actions = []
        # For simplicity, let's assume a structured output like a JSON or Python list string from LLM
        try:
            # A more robust parser would use regex or a dedicated LLM output format
            if "move_to(kitchen)" in plan_text:
                parsed_actions.append(("move_to", "kitchen"))
            if "pick_up(mug)" in plan_text:
                parsed_actions.append(("pick_up", "mug"))
            # ... and so on for other actions
        except Exception as e:
            self.get_logger().error(f"Error parsing LLM plan: {e}")
        return parsed_actions

    def execute_robot_actions(self, actions):
        for action_name, param in actions:
            self.get_logger().info(f"Executing: {action_name} with param {param}")
            if action_name == "move_to":
                self.move_to_location(param)
            elif action_name == "pick_up":
                self.pick_up_object(param)
            # Add more action handlers
            else:
                self.get_logger().warn(f"Unknown action: {action_name}")
            
            # Optional: Add error checking and feedback mechanism here
            # If an action fails, perhaps inform the LLM or human operator

    def move_to_location(self, location_name):
        self.get_logger().info(f"Attempting to navigate to {location_name}")
        # In a real system, 'location_name' would map to a known PoseStamped
        # For this example, let's define some hardcoded poses
        if location_name == "kitchen":
            goal_pose = PoseStamped()
            goal_pose.header.frame_id = 'map'
            goal_pose.pose.position.x = 2.0
            goal_pose.pose.position.y = 1.0
            goal_pose.pose.orientation.w = 1.0
        else:
            self.get_logger().error(f"Unknown location: {location_name}")
            return

        goal_msg = NavigateToPose.Goal()
        goal_msg.pose = goal_pose

        self.nav_to_pose_client.wait_for_server()
        self.get_logger().info("Nav2 server found. Sending goal...")
        
        send_goal_future = self.nav_to_pose_client.send_goal_async(goal_msg)
        # Handle goal response (feedback and result) asynchronously
        send_goal_future.add_done_callback(self.goal_response_callback)

    def goal_response_callback(self, future):
        goal_handle = future.result()
        if not goal_handle.accepted:
            self.get_logger().error('Goal rejected :(')
            return

        self.get_logger().info('Goal accepted :)')
        get_result_future = goal_handle.get_result_async()
        get_result_future.add_done_callback(self.get_result_callback)

    def get_result_callback(self, future):
        result = future.result().result
        status = future.result().status
        if status == GoalStatus.STATUS_SUCCEEDED:
            self.get_logger().info('Navigation Succeeded! Result: {0}'.format(result))
        else:
            self.get_logger().error('Navigation Failed with status: {0}'.format(status))

    def pick_up_object(self, object_name):
        self.get_logger().info(f"Attempting to pick up {object_name}")
        # This would typically involve:
        # 1. Calling a perception service to get the object's precise pose.
        # 2. Creating a Pick.Goal() message.
        # 3. Sending the goal to the pick_action_client.
        # 4. Waiting for the result.
        # This is a placeholder for a complex manipulation pipeline.
        
        # Example of sending a custom Pick action goal
        pick_goal = Pick.Goal()
        pick_goal.object_name = object_name
        # Add target pose, gripper command, etc.
        
        self.pick_action_client.wait_for_server()
        self.get_logger().info("Pick action server found. Sending goal...")
        send_goal_future = self.pick_action_client.send_goal_async(pick_goal)
        send_goal_future.add_done_callback(self.pick_goal_response_callback)

    def pick_goal_response_callback(self, future):
        goal_handle = future.result()
        if not goal_handle.accepted:
            self.get_logger().error('Pick goal rejected :(')
            return
        self.get_logger().info('Pick goal accepted :)')
        get_result_future = goal_handle.get_result_async()
        get_result_future.add_done_callback(self.pick_get_result_callback)

    def pick_get_result_callback(self, future):
        result = future.result().result
        status = future.result().status
        if status == GoalStatus.STATUS_SUCCEEDED:
            self.get_logger().info('Pick Succeeded! Result: {0}'.format(result))
        else:
            self.get_logger().error('Pick Failed with status: {0}'.format(status))


def main(args=None):
    rclpy.init(args=args)
    plan_translator_node = PlanTranslatorNode()
    rclpy.spin(plan_translator_node)
    plan_translator_node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

This conceptual `PlanTranslatorNode` demonstrates how to:
-   Subscribe to the LLM's plan.
-   Parse the plan into actionable steps.
-   Call ROS 2 action clients (e.g., `NavigateToPose` for movement, a custom `Pick` action for manipulation).
-   Handle action responses asynchronously.

## 5. Key Considerations for Robust Plan Translation

-   **Action Granularity**: Define a clear set of low-level, atomic robotic actions that the plan translator can reliably call. These should correspond to existing ROS 2 actions or services.
-   **State Management**: The plan translator needs to know the robot's current state (location, grasped object, etc.) to validate and execute plans. This information comes from perception modules.
-   **Error Handling and Recovery**: What happens if a ROS 2 action fails? The translator should be able to:
    -   Notify the LLM for re-planning.
    -   Attempt a retry.
    -   Ask the human for clarification.
    -   Log the error.
-   **Mapping from Abstract to Concrete**: Develop a robust mechanism to map abstract LLM terms (e.g., "mug," "kitchen counter") to specific, detectable entities and locations in the robot's perception and world model.
-   **Safety Constraints**: Ensure that the plan translator enforces safety limits and prevents the robot from executing dangerous or physically impossible commands, even if suggested by the LLM.

## Conclusion

Translating natural language-driven cognitive plans from LLMs into executable ROS 2 action plans is a crucial step in building sophisticated VLA systems for humanoid robots. By developing a robust plan translation module that grounds abstract instructions into concrete robotic actions and interacts with the robot's perception and motion control systems, you can empower your humanoid to perform complex tasks based on human intent. This forms the backbone for building intelligent and responsive robotic assistants.
