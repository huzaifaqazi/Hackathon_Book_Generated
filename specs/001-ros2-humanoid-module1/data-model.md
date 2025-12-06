# Data Model: Physical AI & Humanoid Robotics Course

**Feature Branch**: `001-ros2-humanoid-module1`
**Created**: 2025-12-06
**Status**: Draft

## Entities

#### Entity: Book
- **Description**: The entire collection of educational content.
- **Attributes**:
    - `Title`: "Physical AI & Humanoid Robotics"
    - `Theme`: "Embodied Intelligence and AI Systems in the Physical World"
    - `Goal`: "Teach students to control humanoid robots (simulated + limited physical) using ROS 2, Gazebo, Unity, NVIDIA Isaac, and Vision-Language-Action systems."
    - `Modules`: List of Module entities.
    - `TargetAudience`: ["Students with basic Python/AI knowledge entering robotics", "Educators evaluating a robotics-heavy curriculum"]
- **Relationships**: Contains Modules.

#### Entity: Module
- **Description**: A self-contained unit of the book, covering a specific topic.
- **Attributes**:
    - `Title`: "The Robotic Nervous System (ROS 2)" for Module 1.
    - `Chapters`: List of Chapter entities.
- **Relationships**: Belongs to a Book, Contains Chapters.

#### Entity: Chapter
- **Description**: A specific section within a module, focusing on a sub-topic.
- **Attributes**:
    - `Title`: e.g., "Introduction to ROS 2 and Humanoid Control", "Nodes, Topics, Services, and Actions".
    - `Content`: Markdown/MDX text, code blocks, diagrams.
    - `Length`: 800-1500 words (constraint).
    - `Diagrams`: Mermaid or SVG format (constraint).
- **Relationships**: Belongs to a Module.

#### Entity: SpecKitPlusPrompt
- **Description**: A structured input used by Spec-Kit Plus to generate content.
- **Attributes**:
    - `Type`: e.g., "chapter-generation", "code-block", "diagram-generation".
    - `Parameters`: Specific inputs for content generation.
    - `OutputFormat`: Markdown/MDX.
- **Relationships**: Generates Chapter Content.

#### Entity: CodeBlock
- **Description**: Verified code snippets embedded within chapters.
- **Attributes**:
    - `Language`: e.g., Python, Bash.
    - `Content`: Source code.
    - `VerificationStatus`: Verified (run-tested or syntactically correct).
- **Relationships**: Belongs to a Chapter.

#### Entity: Diagram
- **Description**: Visual representations within chapters.
- **Attributes**:
    - `Format`: Mermaid or SVG.
    - `Content`: Diagram definition.
- **Relationships**: Belongs to a Chapter.
