# Quickstart Guide: Setting Up the AI/Spec-Driven Book Project

This guide provides a rapid setup for contributing to the "Physical AI & Humanoid Robotics" book project.

## 1. Prerequisites

Before you begin, ensure you have the following installed:

- **Node.js**: LTS version (e.g., v18.x or v20.x).
- **Git**: Latest version.
- **GitHub Account**: Required for repository access and deployment.
- **Spec-Kit Plus CLI**: Install globally (`npm install -g spec-kit-plus-cli`).
- **Claude Code Access**: Ensure you have configured access to Claude Code for content generation (e.g., API key setup).

## 2. Project Setup

1.  **Clone the Repository**:
    ```bash
    git clone https://github.com/your-org/ai-native-book.git
    cd ai-native-book
    ```

2.  **Install Docusaurus Dependencies**:
    ```bash
    npm install
    ```

3.  **Create a New Feature Branch (Example)**:
    ```bash
    /sp.specify "Your new chapter idea"
    # Follow prompts to create a new spec and branch.
    # For this module, you might checkout an existing module branch.
    git checkout 001-ros2-humanoid-module1
    ```

## 3. Content Creation Workflow

1.  **Generate Chapter Content (via Spec-Kit Plus)**:
    Use Spec-Kit Plus prompts to scaffold new chapters or sections.
    ```bash
    # Example: Generate a new chapter
    /sp.generate chapter "Introduction to ROS 2" --template chapter-template
    ```

2.  **Refine with Claude Code**:
    Use Claude Code to expand, refine, or proofread generated content. Integrate code blocks and diagrams as needed.

3.  **Build and Preview Locally**:
    ```bash
    npm start
    ```
    Open your browser to `http://localhost:3000` to see your changes.

## 4. Deployment (for Project Maintainers)

1.  **Build the Docusaurus Site**:
    ```bash
    npm run build
    ```

2.  **Deploy to GitHub Pages**:
    ```bash
    npm run deploy
    ```
    (This assumes the `gh-pages` branch deployment is configured.)

## 5. Testing

- Run `npm run build` to check for build errors.
- Check for broken links: (specific Docusaurus command will be added here after research).

## 6. Next Steps

- Consult `docs/your-chapter/spec.md` for detailed requirements.
- Refer to the project's `constitution.md` for governance.
