# Data Model (Course Structure): Physical AI & Humanoid Robotics Course

**Branch**: `001-physical-ai-robotics-course` | **Date**: 2025-12-06 | **Plan**: specs/001-physical-ai-robotics-course/plan.md

This document outlines the logical structure and entities of the "Physical AI & Humanoid Robotics Course," defining how the course content is organized and related. This is not a traditional software data model but rather a structural blueprint for the educational material.

## Entities

### 1. Course

-   **Description**: The overarching educational program.
-   **Attributes**:
    -   `Course Title`: "Physical AI & Humanoid Robotics"
    -   `Theme`: "Embodied Intelligence and AI Systems in the Physical World"
    -   `Goal`: "Teach students to control humanoid robots (simulated + limited physical) using ROS 2, Gazebo, Unity, NVIDIA Isaac, and Vision-Language-Action systems."
    -   `Target Audience`: Students with basic Python/AI knowledge, educators.
    -   `Duration`: 13-week quarter
    -   `Learning Objectives`: High-level outcomes for the entire course.
-   **Relationships**: Composed of multiple `Module` entities.

### 2. Module

-   **Description**: A major thematic unit within the course, focusing on a specific area of Physical AI and robotics.
-   **Attributes**:
    -   `Module ID`: (e.g., M0, M1, M2, M3, M4)
    -   `Module Title`: (e.g., "The Robotic Nervous System (ROS 2)")
    -   `Focus`: Key concepts and technologies covered.
    -   `Target Audience (Module-specific)`: Specific subset of students.
    -   `Success Criteria (Module-specific)`: Measurable outcomes for the module.
-   **Relationships**: Contains multiple `Chapter` entities. Linked to `Course`.

### 3. Chapter

-   **Description**: A detailed lesson or topic within a module.
-   **Attributes**:
    -   `Chapter ID`: (e.g., 1.1, 1.2, 4.7)
    -   `Chapter Title`: (e.g., "Introduction to ROS 2 and Humanoid Control")
    -   `Content`: Text, code examples, diagrams, explanations.
    -   `Learning Objectives (Chapter-specific)`: Specific outcomes for the chapter.
    -   `Assignment / Mini Project`: (If applicable) Practical exercise related to the chapter.
-   **Relationships**: Belongs to a `Module`. May link to `Code Example`, `Diagram`, `Assignment`.

### 4. Code Example

-   **Description**: Verifiable snippets or full programs demonstrating robotics concepts.
-   **Attributes**:
    -   `Code`: Source code (Python).
    -   `Context`: Explanation of the code's purpose and usage.
    -   `Verification Status`: (e.g., run-tested, syntactically correct).
-   **Relationships**: Associated with one or more `Chapter` entities.

### 5. Diagram

-   **Description**: Visual aids to explain complex systems or concepts.
-   **Attributes**:
    -   `Type`: (e.g., Mermaid, SVG).
    -   `Content`: Diagram source code or image path.
    -   `Description`: Explanation of the diagram.
-   **Relationships**: Associated with one or more `Chapter` entities.

### 6. Assignment / Mini Project

-   **Description**: Practical tasks for students to apply learned knowledge.
-   **Attributes**:
    -   `Title`: Name of the assignment.
    -   `Description`: Detailed instructions and goals.
    -   `Deliverables`: What students need to submit.
    -   `Rubric`: Assessment criteria.
-   **Relationships**: Associated with one or more `Chapter` or `Module` entities.

### 7. Hardware Requirements (Tiered)

-   **Description**: Specifications for physical computing resources needed for the course.
-   **Attributes**:
    -   `Tier`: (e.g., Basic, Recommended, Advanced)
    -   `Component`: (e.g., GPU, RAM, CPU, Jetson Model)
    -   `Specification`: (e.g., RTX 4070 Ti, 12GB VRAM, Jetson Orin Nano)
-   **Relationships**: Referenced by `Module` and `Chapter` entities.

## Relationships Overview

-   `Course` 1..N `Module`
-   `Module` 1..N `Chapter`
-   `Chapter` 0..N `Code Example`
-   `Chapter` 0..N `Diagram`
-   `Chapter` 0..1 `Assignment / Mini Project` (can also be module-level)
-   `Module` 0..1 `Assignment / Mini Project`
-   `Course` 1..1 `Hardware Requirements` (overall course, with tiered options)

## Validation Rules (Course-Level)

-   Course must contain between 8 and 12 chapters (sum of all modules).
-   Each chapter word count between 800 and 1500 words.
-   All diagrams in Mermaid or SVG format.
-   Code examples must be verified.
-   Course content must be compatible with Ubuntu 22.04 and ROS 2 Humble/Iron.
-   Isaac Sim exercises require RTX 4070 Ti (12GB VRAM minimum).
-   Isaac ROS modules require Jetson Orin.
-   All formats USD or ROS 2 compatible.
-   Whisper models: small/medium only.
-   Course fits 13-week quarter structure.
