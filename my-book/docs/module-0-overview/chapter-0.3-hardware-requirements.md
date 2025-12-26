# Chapter 0.3: Hardware Requirements (Tiered)

To ensure an optimal learning experience and accommodate diverse student resources, this course outlines tiered hardware requirements. These tiers guide you in selecting or utilizing computing resources that align with the demands of Physical AI and Humanoid Robotics development, ranging from foundational ROS 2 exercises to advanced NVIDIA Isaac Sim applications.

## General Considerations

-   **Operating System**: All development and exercises are based on **Ubuntu 22.04 LTS**. While Windows Subsystem for Linux (WSL2) with GPU passthrough can be used, a native Ubuntu installation is generally recommended for performance and compatibility.
-   **Internet Connection**: A stable and reasonably fast internet connection is crucial for software downloads, updates, and accessing online resources.
-   **Keyboard & Mouse**: Standard input devices are sufficient.
-   **Display**: A monitor with at least 1080p resolution is recommended for comfortable coding and simulation visualization.

## Hardware Tiers

### Basic Tier (Minimum Recommended)

This tier is suitable for foundational ROS 2 exercises and simpler Gazebo simulations. Performance in NVIDIA Isaac Sim and Unity may be limited or require reduced quality settings.

-   **Operating System**: Ubuntu 22.04 LTS (Native installation or WSL2 with GPU passthrough for Windows users).
-   **Processor**: Quad-core CPU (e.g., Intel i5 / AMD Ryzen 5 equivalent or better).
-   **RAM**: 16 GB RAM.
-   **GPU (for Isaac Sim & Unity)**: NVIDIA RTX 3050 (8GB VRAM) or equivalent. Performance may be limited, and some advanced Isaac Sim features might not run optimally.
-   **Edge Device (Optional for some exercises)**: NVIDIA Jetson Nano (for basic ROS 2 deployment exercises).
-   **Disk Space**: 100 GB Free SSD space. SSD is highly recommended over HDD for faster load times.

### Recommended Tier (Optimal Experience)

This tier offers a balanced performance for most aspects of the course, providing a smooth experience for complex Gazebo and Unity simulations, as well as efficient execution of NVIDIA Isaac Sim applications and Isaac ROS modules on edge devices.

-   **Operating System**: Ubuntu 22.04 LTS (Native installation recommended).
-   **Processor**: Hexa-core CPU (e.g., Intel i7 / AMD Ryzen 7 equivalent or better).
-   **RAM**: 32 GB RAM.
-   **GPU (for Isaac Sim & Unity)**: NVIDIA RTX 4070 Ti (12GB VRAM) or better. This GPU meets the minimum requirements for Isaac Sim 4.x+.
-   **Edge Device**: NVIDIA Jetson Orin Nano (for Isaac ROS and VLA exercises).
-   **Disk Space**: 200 GB Free SSD space.

### Advanced Tier (Cloud-Native & High Performance)

For students and institutions seeking the highest performance, especially for photorealistic simulation, large-scale synthetic data generation, and computationally intensive AI tasks, this tier provides robust capabilities. Cloud-native options are also considered here.

-   **Operating System**: Ubuntu 22.04 LTS (Native or cloud VM).
-   **Processor**: High-performance multi-core CPU (e.g., Intel i9 / AMD Ryzen 9 equivalent or server-grade CPUs).
-   **RAM**: 64 GB RAM or more.
-   **GPU (for Isaac Sim & Unity)**: NVIDIA RTX 4090 or a cloud GPU instance (e.g., NVIDIA A100, H100) with substantial VRAM.
-   **Edge Device**: NVIDIA Jetson Orin NX (for maximum performance on edge exercises).
-   **Disk Space**: 500 GB Free NVMe SSD space.

## Choosing Your Tier

Consider your budget, existing hardware, and specific learning goals when choosing a tier. While the "Recommended Tier" offers the best balance for the course, the "Basic Tier" is sufficient to follow many core concepts, and the "Advanced Tier" is for those pushing the boundaries of performance and scale. Cloud-based solutions can also provide access to high-tier resources without significant upfront hardware investment.
