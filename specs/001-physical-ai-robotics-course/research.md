# Research & Decisions: Physical AI & Humanoid Robotics Course

**Branch**: `001-physical-ai-robotics-course` | **Date**: 2025-12-06 | **Plan**: specs/001-physical-ai-robotics-course/plan.md

## Research Approach

The course will adopt a research-concurrent method. Robotics references, hardware specifications, physics simulation details, and AI/embodied intelligence papers will be collected and integrated while developing each section of the course. This ensures that the content remains up-to-date and reflects current best practices and technologies.

## Decisions Needing Documentation / Research Areas

This section outlines key decisions and areas requiring further research to inform the course content and infrastructure.

### 1. ROS 2 Version Selection

-   **Decision**: To be determined based on a trade-off analysis between stability and the availability of new features relevant to humanoid robotics. ROS 2 Humble (LTS) offers long-term support and stability, while Iron provides the latest features and improvements.
-   **Rationale**: The choice will balance pedagogical needs (ensuring students learn relevant, stable tools) with access to cutting-edge capabilities.
-   **Alternatives Considered**: ROS 2 Humble Hawksbill (LTS), ROS 2 Iron Irwini (latest).

### 2. Gazebo vs Unity for Simulation Fidelity

-   **Decision**: Gazebo will be used for physics-realistic simulation, while Unity will be utilized for high-fidelity visualization and Human-Robot Interaction (HRI) aspects.
-   **Rationale**: Gazebo excels in physics accuracy for robotics, which is crucial for embodied AI. Unity provides superior visual rendering and a more robust environment for complex HRI development.
-   **Alternatives Considered**: Exclusive use of Gazebo, exclusive use of Unity (e.g., Unity Robotics Hub).

### 3. Isaac Sim Local vs Cloud Deployment

-   **Decision**: Provide guidance for both local and cloud deployment options for Isaac Sim, highlighting the cost, performance, and latency trade-offs for students.
-   **Rationale**: Accommodate diverse student resources. Local deployment offers immediate access and potentially lower latency for those with capable hardware. Cloud deployment provides scalability and accessibility for students without high-end local machines, but introduces cost and potential latency.
-   **Alternatives Considered**: Mandate only local deployment, mandate only cloud deployment.

### 4. Jetson Model Choice (Orin Nano vs NX)

-   **Decision**: Focus on Jetson Orin Nano for its budget-friendliness and accessibility, while discussing the performance benefits and advanced capabilities of the Orin NX for those with higher budgets.
-   **Rationale**: Maximize student accessibility to hardware while acknowledging performance scalability. Orin Nano is an entry point, Orin NX for more demanding tasks.
-   **Alternatives Considered**: Mandate Orin NX only, provide options for older Jetson models.

### 5. Humanoid Robot Selection (Physical Hardware)

-   **Decision**: Utilize "proxy robot" or abstract humanoid models for core concepts, with optional reference to commercially available platforms like Unitree G1 or OP3 to discuss real-world considerations. The emphasis will be on simulated environments where these concepts can be readily applied.
-   **Rationale**: Avoid proprietary robot dependencies to keep the course accessible and affordable. Simulators reduce the need for physical hardware for foundational learning.
-   **Alternatives Considered**: Mandate a specific physical robot, focus solely on a single simulated robot.

### 6. Physical Lab vs Cloud-Native Lab (for Capstone/Advanced Modules)

-   **Decision**: Design the course primarily around cloud-native simulation labs (e.g., Isaac Sim in cloud, ROS 2 in cloud VMs) to minimize CapEx for students, while offering suggestions for physical lab setups for institutions or advanced students.
-   **Rationale**: Cloud-native labs reduce the financial barrier for students and provide a consistent development environment. Physical labs offer invaluable hands-on experience but incur significant costs and setup complexity.
-   **Alternatives Considered**: Mandate a physical lab environment, ignore physical lab possibilities.

### 7. Sensor Suite (RealSense vs LiDAR Options)

-   **Decision**: Cover a range of common sensor types (e.g., depth cameras like RealSense, various LiDAR options) within the simulation context, focusing on their data output and how it integrates into ROS 2 for SLAM and perception tasks.
-   **Rationale**: Expose students to diverse sensor data types and their processing without requiring specific physical hardware. Discussion of trade-offs (cost vs. SLAM quality, range) will be included.
-   **Alternatives Considered**: Focus on a single sensor type (e.g., only LiDAR), omit detailed sensor discussion.

### 8. Voice Interface Selection

-   **Decision**: Utilize Whisper (small/medium models) for voice command extraction, ensuring it runs effectively within Jetson compute limits. Explore existing ROS 2 packages or develop simple interfaces for integration.
-   **Rationale**: Whisper offers robust speech-to-text capabilities and is well-suited for edge devices like Jetson. The choice will prioritize performance on target hardware.
-   **Alternatives Considered**: Other speech-to-text APIs (potentially proprietary), more complex ASR models.
