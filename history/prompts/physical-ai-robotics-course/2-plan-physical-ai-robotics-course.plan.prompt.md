---
id: 2
title: Plan Physical AI Robotics Course
stage: plan
date: 2025-12-06
surface: agent
model: gemini-1.5-pro
feature: physical-ai-robotics-course
branch: 001-physical-ai-robotics-course
user: user
command: /sp.plan

Create:
- Architecture sketch: full course infrastructure linking ROS 2, Gazebo/Unity, NVIDIA Isaac, Jetson edge kits, humanoid/robot hardware, and cloud-based simulation options.
- Section structure: organize Modules 1–4 into clear parts (Foundations, Simulation, Perception, VLA) with subsections for weekly lessons, lab activities, hardware requirements, and assessment strategy.
- Research approach: research-concurrent method—collect robotics references, hardware specs, physics simulation details, and AI/embodied intelligence papers while writing each section.
- Quality validation: accuracy checks for robotics formulas, ROS 2 terminology, Isaac workflows, hardware constraints, and pedagogical clarity.

Decisions needing documentation:
- ROS 2 version selection (Humble vs Iron): tradeoff between stability and new features.
- Gazebo vs Unity for simulation fidelity: physics realism vs visualization and HRI.
- Isaac Sim local vs cloud deployment: cost vs performance vs latency.
- Jetson model choice (Orin Nano vs NX): performance vs budget.
- Humanoid robot selection (Unitree G1 vs OP3 vs proxy robot): cost vs realism vs accessibility.
- Physical lab vs cloud-native lab: CapEx vs OpEx and student hardware constraints.
- Sensor suite (RealSense vs LiDAR options): cost vs SLAM quality.
- Voice interface selection: Whisper performance vs Jetson compute limits.

Testing strategy:
- ROS 2 acceptance tests: node communication, topic traffic, service/action correctness.
- Gazebo/Unity validation: stable physics simulation, correct URDF/SDF loading, sensor data streaming.
- Isaac Sim pipeline tests: synthetic data generation, VSLAM stability, navigation path correctness.
- VLA tests: full pipeline Voice → LLM Plan → ROS Actions with deterministic behavior.
- Hardware tests: Jetson deployment load testing, camera calibration, IMU validation, network latency checks.
- Course validation: weekly outcomes must match learning objectives and run error-free on required hardware.

Technical details:
- Use research-concurrent approach (research while writing sections; integrate robotics papers, Isaac/ROS 2 docs, embodied intelligence research as needed).
- Follow APA citation style as mandated in the Constitution.
- Organize by phases:
  Phase 1 — Research: Gather robotics foundations, embodied intelligence, humanoid design references.
  Phase 2 — Foundation: Define ROS 2 architecture, humanoid kinematics, simulation environment.
  Phase 3 — Analysis: Compare simulation tools, hardware tiers, AI integration choices.
  Phase 4 — Synthesis: Build unified Physical AI course blueprint, create weekly plan, assessments, and lab infrastructure.
labels: ["plan", "feature-planning"]
links:
  spec: specs/001-physical-ai-robotics-course/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/001-physical-ai-robotics-course/plan.md
  - specs/001-physical-ai-robotics-course/research.md
  - specs/001-physical-ai-robotics-course/data-model.md
  - specs/001-physical-ai-robotics-course/quickstart.md
  - specs/001-physical-ai-robotics-course/contracts/
  - GEMINI.md
tests:
null
---

## Prompt

/sp.plan

Create:
- Architecture sketch: full course infrastructure linking ROS 2, Gazebo/Unity, NVIDIA Isaac, Jetson edge kits, humanoid/robot hardware, and cloud-based simulation options.
- Section structure: organize Modules 1–4 into clear parts (Foundations, Simulation, Perception, VLA) with subsections for weekly lessons, lab activities, hardware requirements, and assessment strategy.
- Research approach: research-concurrent method—collect robotics references, hardware specs, physics simulation details, and AI/embodied intelligence papers while writing each section.
- Quality validation: accuracy checks for robotics formulas, ROS 2 terminology, Isaac workflows, hardware constraints, and pedagogical clarity.

Decisions needing documentation:
- ROS 2 version selection (Humble vs Iron): tradeoff between stability and new features.
- Gazebo vs Unity for simulation fidelity: physics realism vs visualization and HRI.
- Isaac Sim local vs cloud deployment: cost vs performance vs latency.
- Jetson model choice (Orin Nano vs NX): performance vs budget.
- Humanoid robot selection (Unitree G1 vs OP3 vs proxy robot): cost vs realism vs accessibility.
- Physical lab vs cloud-native lab: CapEx vs OpEx and student hardware constraints.
- Sensor suite (RealSense vs LiDAR options): cost vs SLAM quality.
- Voice interface selection: Whisper performance vs Jetson compute limits.

Testing strategy:
- ROS 2 acceptance tests: node communication, topic traffic, service/action correctness.
- Gazebo/Unity validation: stable physics simulation, correct URDF/SDF loading, sensor data streaming.
- Isaac Sim pipeline tests: synthetic data generation, VSLAM stability, navigation path correctness.
- VLA tests: full pipeline Voice → LLM Plan → ROS Actions with deterministic behavior.
- Hardware tests: Jetson deployment load testing, camera calibration, IMU validation, network latency checks.
- Course validation: weekly outcomes must match learning objectives and run error-free on required hardware.

Technical details:
- Use research-concurrent approach (research while writing sections; integrate robotics papers, Isaac/ROS 2 docs, embodied intelligence research as needed).
- Follow APA citation style as mandated in the Constitution.
- Organize by phases:
  Phase 1 — Research: Gather robotics foundations, embodied intelligence, humanoid design references.
  Phase 2 — Foundation: Define ROS 2 architecture, humanoid kinematics, simulation environment.
  Phase 3 — Analysis: Compare simulation tools, hardware tiers, AI integration choices.
  Phase 4 — Synthesis: Build unified Physical AI course blueprint, create weekly plan, assessments, and lab infrastructure.

## Response snapshot

Completed implementation planning workflow, generated plan artifacts, and updated agent context.

## Outcome

- ✅ Impact: Generated a detailed implementation plan, documented key research decisions, outlined course structure as a data model, and created a quickstart guide for the "Physical AI & Humanoid Robotics Course." Agent context was updated with new technologies.
- 🧪 Tests: No direct tests were executed, but the plan includes a comprehensive testing strategy for the course content.
- 📁 Files: specs/001-physical-ai-robotics-course/plan.md, specs/001-physical-ai-robotics-course/research.md, specs/001-physical-ai-robotics-course/data-model.md, specs/001-physical-ai-robotics-course/quickstart.md, specs/001-physical-ai-robotics-course/contracts/, GEMINI.md
- 🔁 Next prompts: The next step is to proceed with `/sp.tasks`.
- 🧠 Reflection: The planning phase successfully translated the high-level specification into actionable artifacts. The process highlighted the importance of early identification of research areas and decisions. The `update-agent-context.ps1` script proved useful for dynamically updating the agent's knowledge base.

## Evaluation notes (flywheel)

- Failure modes observed: None in this phase after resolving previous issues with command parsing.
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): N/A
