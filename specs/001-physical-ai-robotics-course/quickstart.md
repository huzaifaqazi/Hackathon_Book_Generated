# Quickstart Guide: Physical AI & Humanoid Robotics Course

**Branch**: `001-physical-ai-robotics-course` | **Date**: 2025-12-06 | **Plan**: specs/001-physical-ai-robotics-course/plan.md

This quickstart guide provides essential information to get students set up for the "Physical AI & Humanoid Robotics Course," covering prerequisites, software installation, and initial environment configuration.

## 1. Course Overview

This course introduces students to the exciting field of embodied intelligence by teaching them how to control humanoid robots using modern robotics and AI tools. You will learn about ROS 2 for robot control, create digital twins in Gazebo and Unity, leverage NVIDIA Isaac Sim for advanced perception, and build Vision-Language-Action (VLA) systems.

## 2. Prerequisites

To get the most out of this course, students should have:

-   **Basic Python Programming**: Familiarity with Python syntax, data structures, and object-oriented programming concepts.
-   **Basic AI/ML Concepts**: Understanding of fundamental AI/ML principles, including supervised learning, neural networks, and basic data handling.
-   **Linear Algebra Fundamentals**: Basic understanding of vectors, matrices, and transformations will be beneficial for robotics.
-   **Linux Command Line Familiarity**: Comfort with basic Linux commands is essential as the course primarily runs on Ubuntu.

## 3. Hardware Requirements (Tiered)

To accommodate various budgets and performance needs, hardware requirements are tiered:

### Basic Tier (Minimum Recommended)

-   **Operating System**: Ubuntu 22.04 LTS (Native installation or WSL2 with GPU passthrough for Windows users).
-   **Processor**: Quad-core CPU (e.g., Intel i5 / AMD Ryzen 5 equivalent or better).
-   **RAM**: 16 GB RAM.
-   **GPU (for Isaac Sim)**: NVIDIA RTX 3050 (8GB VRAM) or equivalent. Performance may be limited.
-   **Edge Device**: NVIDIA Jetson Nano (for basic ROS 2 deployment exercises).
-   **Disk Space**: 100 GB Free SSD space.

### Recommended Tier (Optimal Experience)

-   **Operating System**: Ubuntu 22.04 LTS (Native installation recommended).
-   **Processor**: Hexa-core CPU (e.g., Intel i7 / AMD Ryzen 7 equivalent or better).
-   **RAM**: 32 GB RAM.
-   **GPU (for Isaac Sim)**: NVIDIA RTX 4070 Ti (12GB VRAM) or better.
-   **Edge Device**: NVIDIA Jetson Orin Nano (for Isaac ROS and VLA exercises).
-   **Disk Space**: 200 GB Free SSD space.

### Advanced Tier (Cloud-Native & High Performance)

-   **Operating System**: Ubuntu 22.04 LTS (Native or cloud VM).
-   **Processor**: High-performance multi-core CPU.
-   **RAM**: 64 GB RAM or more.
-   **GPU (for Isaac Sim)**: NVIDIA RTX 4090 or cloud GPU instance (e.g., NVIDIA A100).
-   **Edge Device**: NVIDIA Jetson Orin NX (for maximum performance on edge exercises).
-   **Disk Space**: 500 GB Free NVMe SSD space.

## 4. Software Setup

All software installations will be performed on **Ubuntu 22.04 LTS**.

### 4.1. ROS 2 Installation

Install ROS 2 Humble Hawksbill or Iron Irwini. Follow the official ROS 2 documentation for your chosen distribution:

-   [ROS 2 Humble Installation Guide](https://docs.ros.org/en/humble/Installation.html)
-   [ROS 2 Iron Installation Guide](https://docs.ros.org/en/iron/Installation.html)

**Note**: The course primarily uses Python (rclpy) for ROS 2 development.

### 4.2. Gazebo Simulation

Gazebo Garden or Fortress will be used. Install it via ROS 2 dependencies or as a standalone package:

-   [Gazebo Installation Guide](https://gazebosim.org/docs/garden/install_ubuntu)

### 4.3. Unity for HRI (Optional, Recommended)

For high-fidelity Human-Robot Interaction (HRI) visualization, Unity will be used. Install Unity Hub and Unity 2022 LTS:

-   [Unity Hub and Editor Installation](https://docs.unity3d.com/Manual/GettingStartedInstallingHub.html)
-   Install the Unity Robotics Hub package from the Unity Asset Store or GitHub.

### 4.4. NVIDIA Isaac Sim

NVIDIA Isaac Sim 4.x+ is required for photorealistic simulation and synthetic data generation. Installation requires an NVIDIA GPU (refer to hardware requirements).

-   [NVIDIA Isaac Sim Documentation](https://docs.omniverse.nvidia.com/app_isaacsim/app_isaacsim/install_quickstart.html)

### 4.5. NVIDIA Isaac ROS

Isaac ROS modules will be integrated with ROS 2. These require a Jetson Orin device for optimal performance but can be tested on compatible desktop GPUs.

-   [NVIDIA Isaac ROS Documentation](https://nvidia-isaac-ros.github.io/index.html)

### 4.6. Python Environment Setup

It is highly recommended to use a virtual environment (e.g., `venv` or `conda`) for Python dependencies.

```bash
# Example: Create and activate a Python virtual environment
python3 -m venv ~/physical_ai_robotics_venv
source ~/physical_ai_robotics_venv/bin/activate

# Install common Python packages (e.g., rclpy, numpy, scipy)
pip install rclpy numpy scipy
```

### 4.7. Whisper

For VLA modules, install the OpenAI Whisper model and its dependencies. Small or medium models are sufficient.

```bash
pip install -U openai-whisper
```

## 5. Course Repository

Clone the course repository to access all materials, code examples, and assignments:

```bash
git clone [COURSE_REPOSITORY_URL]
cd [COURSE_REPOSITORY_DIRECTORY]
```

## 6. Support

If you encounter any issues during setup, please refer to the course's dedicated support channels or FAQ.
