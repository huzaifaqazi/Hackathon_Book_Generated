# Implementation Plan: Physical AI & Humanoid Robotics Course

**Branch**: `001-physical-ai-robotics-course` | **Date**: 2025-12-06 | **Spec**: specs/001-physical-ai-robotics-course/spec.md
**Input**: Feature specification from `/specs/001-physical-ai-robotics-course/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

The feature is to create a comprehensive course on "Physical AI & Humanoid Robotics," covering ROS 2, digital twins (Gazebo/Unity), NVIDIA Isaac Sim (perception), and Vision-Language-Action (VLA) systems. The course will teach students to control humanoid robots, utilizing simulated and limited physical hardware, with a focus on practical application and adherence to strict technical standards.

## Technical Context

**Language/Version**: Python (no C++)  
**Primary Dependencies**: ROS 2 (Humble/Iron), Gazebo (Garden/Fortress), Unity, NVIDIA Isaac Sim (4.x+), NVIDIA Isaac ROS, Whisper, LLMs (GPT, Claude)  
**Storage**: N/A (Course content, not a system with persistent storage needs)  
**Testing**: ROS 2 acceptance tests, Gazebo/Unity validation, Isaac Sim pipeline tests, VLA full pipeline tests, Hardware tests, Course validation.  
**Target Platform**: Ubuntu 22.04 (workstation + Jetson Orin)
**Project Type**: Courseware/Documentation  
**Performance Goals**:
-   Digital twin simulations: Stable physics simulation at 60 FPS
-   Isaac Sim: Runs on RTX workstation (RTX 4070 Ti+ with 12GB VRAM minimum)
-   Isaac ROS: Runs on Jetson Orin
-   Whisper: Performance within Jetson compute limits  
**Constraints**:
-   ROS 2 Humble or Iron only
-   Only Python (no C++)
-   URDF validated in RViz/Gazebo
-   Exercises run on workstation + Jetson
-   Gazebo Garden/Fortress only
-   Unity scenes < 200k polygons
-   ROS 2 naming conventions
-   Simulations must run on Ubuntu 22.04
-   Isaac Sim 4.x+
-   Minimum GPU: RTX 4070 Ti (12GB VRAM)
-   Isaac ROS must run on Jetson Orin
-   All formats USD or ROS 2 compatible
-   Whisper small/medium only
-   Limited API usage for LLMs
-   Deterministic + logged planning for VLA
-   Only simple tasks allowed for VLA
-   Markdown specs (Spec-Kit Plus compatible)
-   Standard robotics terminology
-   Mermaid or SVG diagrams
-   Course fits 13-week quarter
-   No proprietary robot dependency (optional Unitree)  
**Scale/Scope**: 4 core modules, 1 course-level module, 13-week quarter structure, covering control, simulation, perception, VLA for humanoid robotics.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

-   **Core Principle I: Specification-first writing workflow**: The spec was created using `/sp.specify`. This plan is derived from the spec. **Pass.**
-   **Core Principle II: Consistency across chapters**: The plan emphasizes section structure and quality validation for pedagogical clarity. **Pass.**
-   **Core Principle III: Technical accuracy**: The plan includes quality validation for robotics formulas, ROS 2 terminology, Isaac workflows, and hardware constraints. **Pass.**
-   **Core Principle IV: Clear instructional writing**: The plan aims for pedagogical clarity. **Pass.**
-   **Core Principle V: Modular, reusable, and maintainable content architecture**: The plan outlines organizing modules into clear parts and subsections. **Pass.**

-   **Standard 1: Spec-Kit Plus Origination**: The spec was created using Spec-Kit Plus. The plan will follow it. **Pass.**
-   **Standard 2: Docusaurus Documentation**: The course goal is to generate content for a book which will likely use Docusaurus. The constraint mentions "Markdown specs (Spec-Kit Plus compatible)" which aligns with Docusaurus. **Pass.**
-   **Standard 3: Logical Hierarchy**: The plan explicitly mentions organizing Modules 1–4 into clear parts with subsections. **Pass.**
-   **Standard 4: Verified Code Examples**: The plan includes testing strategies that imply verification of code examples. **Pass.**
-   **Standard 5: GitHub Pages Deployment**: Not directly applicable to the plan itself, but a consideration for the final course delivery. **Pass.**
-   **Standard 6: Claude Code Assistance Guidelines**: Implicitly followed as the agent. **Pass.**

-   **Constraint 1: Book length**: The course has 4 modules + 1 course-level module, each with chapters. This will likely fit the 8-12 chapter constraint. **Pass.**
-   **Constraint 2: Chapter word count**: This is a detail for content creation, not the planning phase. **N/A (for now).**
-   **Constraint 3: Diagram format**: The spec constraint mentions Mermaid or SVG diagrams. The plan will adhere to this. **Pass.**
-   **Constraint 4: Source repository access**: The course materials are assumed to be in a GitHub repository. **Pass.**
-   **Constraint 5: Docusaurus content structure**: The plan implicitly supports this by creating markdown content. **Pass.**

## Project Structure

### Documentation (this feature)

```text
specs/001-physical-ai-robotics-course/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (Not directly applicable to courseware, but could contain course structure data)
├── quickstart.md        # Phase 1 output (Course introduction/setup guide)
├── contracts/           # Phase 1 output (Not applicable)
└── tasks.md             # Phase 2 output (/sp.tasks command)
```

### Source Code (repository root)

```text
my-book/
├── docs/
│   ├── module-0-overview/
│   │   ├── chapter-0.1-overview.md
│   │   ├── ...
│   ├── module-1-ros2/
│   │   ├── chapter-1.1-intro-ros2.md
│   │   ├── ...
│   ├── module-2-digital-twin/
│   │   ├── chapter-2.1-understanding-dt.md
│   │   ├── ...
│   ├── module-3-isaac/
│   │   ├── chapter-3.1-intro-isaac.md
│   │   ├── ...
│   ├── module-4-vla/
│   │   ├── chapter-4.1-intro-vla.md
│   │   ├── ...
│   └── assets/ # For images, diagrams (Mermaid, SVG)
├── blog/
├── src/
├── static/
├── docusaurus.config.ts
├── package.json
└── sidebars.ts
```

**Structure Decision**: The course content will reside within the `my-book/docs/` directory, following a modular structure for each module and chapter. Assets will be stored in `my-book/docs/assets/`.

## Complexity Tracking

N/A - No violations observed.