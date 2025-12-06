<!-- Sync Impact Report -->
<!--
Version change: None --> 0.1.0
Modified principles:
- Core Principles: 5 principles added.
- Key Standards: 6 standards added.
- Constraints: 5 constraints added.
- Success Criteria: 5 criteria added.
Added sections: Key Standards, Constraints, Success Criteria.
Removed sections: None.
Templates requiring updates:
- .specify/templates/plan-template.md ⚠ pending
- .specify/templates/spec-template.md ⚠ pending
- .specify/templates/tasks-template.md ⚠ pending
- .specify/commands/sp.adr.toml ⚠ pending
- .specify/commands/sp.analyze.toml ⚠ pending
- .specify/commands/sp.checklist.toml ⚠ pending
- .specify/commands/sp.clarify.toml ⚠ pending
- .specify/commands/sp.constitution.toml ⚠ pending
- .specify/commands/sp.git.commit_pr.toml ⚠ pending
- .specify/commands/sp.implement.toml ⚠ pending
- .specify/commands/sp.phr.toml ⚠ pending
- .specify/commands/sp.plan.toml ⚠ pending
- .specify/commands/sp.specify.toml ⚠ pending
- .specify/commands/sp.tasks.toml ⚠ pending
Follow-up TODOs: None.
-->
# AI/Spec-Driven Book Creation using Docusaurus, Spec-Kit Plus, and Claude Code Constitution

## Core Principles

### I. Specification-first writing workflow
Every aspect of the book's content, structure, and technical implementation must originate from approved specifications. Spec-Kit Plus serves as the immutable source of truth for all foundational elements.

### II. Consistency across chapters
A unified voice, formatting, and structural approach must be maintained across all chapters. Centralized specifications and a shared style guide ensure a cohesive reader experience.

### III. Technical accuracy
All technical content, including AI concepts, software engineering practices, and documentation methodologies, must be rigorously verified for correctness, up-to-dateness, and practical applicability.

### IV. Clear instructional writing
Content must be written with clarity, precision, and pedagogical effectiveness in mind, making complex topics accessible and actionable for both experienced developers and students new to the field.

### V. Modular, reusable, and maintainable content architecture
Content should be structured to promote modularity, allowing for easy reuse across different sections or future editions, and designed for long-term maintainability and adaptability.

## Key Standards

### Standard 1: Spec-Kit Plus Origination
All chapters must originate from approved specs using Spec-Kit Plus.

### Standard 2: Docusaurus Documentation
Documentation must be generated with Docusaurus 3.x, adhering to MDX best practices for rich content.

### Standard 3: Logical Hierarchy
A logical hierarchy must be followed: Sections → Chapters → Subsections.

### Standard 4: Verified Code Examples
Code examples included in the book must be verified (either run-tested or syntactically correct and manually validated).

### Standard 5: GitHub Pages Deployment
Deployment must target GitHub Pages using automated continuous integration/continuous deployment (CI/CD) workflows.

### Standard 6: Claude Code Assistance Guidelines
Claude Code assistance, when utilized, must strictly adhere to provided spec constraints and actively avoid generating content that deviates from factual accuracy or established patterns ("hallucinations").

## Constraints

### Constraint 1: Book length
The book must contain between 8 and 12 chapters.

### Constraint 2: Chapter word count
Each chapter must have a word count between 800 and 1500 words.

### Constraint 3: Diagram format
All diagrams and visual aids must be in Markdown-compatible formats (e.g., Mermaid or SVG).

### Constraint 4: Source repository access
The source repository must be hosted on GitHub with public read access.

### Constraint 5: Docusaurus content structure
All book content must reside strictly within the Docusaurus `/docs` directory structure.

## Success Criteria

### Criterion 1: Successful Deployment
Complete Docusaurus site successfully deployed on GitHub Pages.

### Criterion 2: Spec-Kit Plus Adherence
All chapters generated strictly from Spec-Kit Plus specifications.

### Criterion 3: Content Consistency
Consistent style, formatting, and structure across the entire book.

### Criterion 4: No Broken Links/Images
Zero broken links/images after build.

### Criterion 5: Build & Docusaurus Checks
Site passes the `npm run build` and `npm run docusaurus` checks without errors.

## Governance
This constitution supersedes all other project practices and guidelines. Amendments to this constitution require explicit documentation of proposed changes, approval by project maintainers, and a clearly defined migration plan if impacts are significant. All pull requests and code reviews must verify compliance with the principles and standards outlined herein. Any introduced complexity must be thoroughly justified.

**Version**: 0.1.0 | **Ratified**: 2025-12-06 | **Last Amended**: 2025-12-06