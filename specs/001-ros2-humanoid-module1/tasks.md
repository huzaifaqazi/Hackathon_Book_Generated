# Tasks: Physical AI & Humanoid Robotics Course: Module 1 - The Robotic Nervous System (ROS 2)

**Input**: Design documents from `/specs/001-ros2-humanoid-module1/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: Test tasks are included as part of the overall flow for quality assurance, not strictly TDD.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- Paths shown below assume Docusaurus project structure with content in `my-book/docs/` and project config in `my-book/`.

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic Docusaurus structure

- [x] T001 Initialize Docusaurus project (my-book) at `my-book/`
- [x] T002 Configure Docusaurus to use Classic Theme with minor customizations in `my-book/docusaurus.config.js`
- [x] T003 Configure Docusaurus for `docs/` and `blog/` folder structure in `my-book/docusaurus.config.js`
- [x] T004 Configure Docusaurus for manual `sidebars.js` in `my-book/docusaurus.config.js`
- [x] T005 Enable MDX support in Docusaurus configuration in `my-book/docusaurus.config.js`
- [x] T006 Set up Git repository and initial commit for Docusaurus project
- [x] T007 Install project dependencies (`npm install`) in `my-book/package.json`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T008 [P] Define core Spec-Kit Plus prompts for chapter generation in `.specify/prompts/chapter_template.md` (or similar)
- [x] T009 [P] Define core Spec-Kit Plus prompts for code block generation in `.specify/prompts/code_block_template.md` (or similar)
- [x] T010 [P] Define core Spec-Kit Plus prompts for diagram generation in `.specify/prompts/diagram_template.md` (or similar)
- [x] T011 [P] Define core Spec-Kit Plus prompts for example generation in `.specify/prompts/example_template.md` (or similar)
- [x] T012 Configure GitHub Actions workflow for Docusaurus build and deployment to GitHub Pages in `.github/workflows/deploy.yml`
- [x] T013 Create initial `sidebars.js` configuration in `my-book/sidebars.js` with placeholders for modules/chapters
- [x] T014 Document Spec-Kit Plus to Chapter Content Generation Contract in `specs/001-ros2-humanoid-module1/contracts/spec-kit-plus-to-chapter-content-generation.md`
- [x] T015 Document Claude Code Content Refinement Contract in `specs/001-ros2-humanoid-module1/contracts/claude-code-content-refinement.md`
- [x] T016 Document Docusaurus Content Ingestion Contract in `specs/001-ros2-humanoid-module1/contracts/docusaurus-content-ingestion.md`
- [x] T017 Document GitHub Pages Deployment Contract in `specs/001-ros2-humanoid-module1/contracts/github-pages-deployment.md`

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Student learning ROS 2 fundamentals [US1] (Priority: P1) 🎯 MVP

**Goal**: Student understands core ROS 2 concepts for humanoid control and builds a basic `rclpy` package.
**Independent Test**: Student successfully completes Chapter 1.1, 1.2, and 1.3 assignments.

### Implementation for User Story 1

- [x] T018 [P] [US1] Generate Chapter 1.1: Introduction to ROS 2 and Humanoid Control content using Spec-Kit Plus in `my-book/docs/module1/ch1.1.mdx`
- [x] T019 [P] [US1] Generate Chapter 1.2: Nodes, Topics, Services, and Actions content using Spec-Kit Plus in `my-book/docs/module1/ch1.2.mdx`
- [x] T020 [P] [US1] Generate Chapter 1.3: Building ROS 2 Python Packages with rclpy content using Spec-Kit Plus in `my-book/docs/module1/ch1.3.mdx`
- [x] T021 [US1] Refine Chapter 1.1 content using Claude Code for clarity and accuracy in `my-book/docs/module1/ch1.1.mdx`
- [x] T022 [US1] Refine Chapter 1.2 content using Claude Code for clarity and accuracy in `my-book/docs/module1/ch1.2.mdx`
- [x] T023 [US1] Refine Chapter 1.3 content using Claude Code for clarity and accuracy in `my-book/docs/module1/ch1.3.mdx`
- [x] T024 [US1] Add necessary Python code examples for Chapter 1.3, verified against ROS 2 Humble, in `my-book/docs/module1/ch1.3.mdx`
- [x] T025 [US1] Integrate assignment instructions for Chapter 1.1, 1.2, 1.3 into their respective MDX files
- [x] T026 [US1] Update `sidebars.js` to include Chapter 1.1, 1.2, and 1.3

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - Student modeling and validating humanoid robots [US2] (Priority: P1)

**Goal**: Student learns to model humanoid robots using URDF and validates them in RViz/Gazebo.
**Independent Test**: Student successfully completes Chapter 1.4 and 1.6 assignments.

### Implementation for User Story 2

- [x] T027 [P] [US2] Generate Chapter 1.4: Humanoid Modeling with URDF content using Spec-Kit Plus in `my-book/docs/module1/ch1.4.mdx`
- [x] T028 [P] [US2] Generate Chapter 1.6: Validating Models in RViz and Gazebo content using Spec-Kit Plus in `my-book/docs/module1/ch1.6.mdx`
- [x] T029 [US2] Refine Chapter 1.4 content using Claude Code for clarity and accuracy in `my-book/docs/module1/ch1.4.mdx`
- [x] T030 [US2] Refine Chapter 1.6 content using Claude Code for clarity and accuracy in `my-book/docs/module1/ch1.6.mdx`
- [x] T031 [US2] Add necessary URDF examples for Chapter 1.4, verified for RViz/Gazebo, in `my-book/docs/module1/ch1.4.mdx`
- [x] T032 [US2] Add necessary instructions for RViz/Gazebo validation in Chapter 1.6 in `my-book/docs/module1/ch1.6.mdx`
- [x] T033 [US2] Integrate assignment instructions for Chapter 1.4, 1.6 into their respective MDX files
- [x] T034 [US2] Update `sidebars.js` to include Chapter 1.4 and 1.6

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Student controlling humanoid robots with ROS 2 [US3] (Priority: P2)

**Goal**: Student implements ROS 2 controllers, understands inter-node communication, and completes a mini-project.
**Independent Test**: Student successfully completes Chapter 1.5 and 1.7, submitting a working humanoid ROS controller mini-project.

### Implementation for User Story 3

- [ ] T035 [P] [US3] Generate Chapter 1.5: Launching Controllers and Inter-node Communication content using Spec-Kit Plus in `my-book/docs/module1/ch1.5.mdx`
- [ ] T036 [P] [US3] Generate Chapter 1.7: Assignment + Mini Project (Humanoid ROS Controller) content using Spec-Kit Plus in `my-book/docs/module1/ch1.7.mdx`
- [x] T037 [US3] Refine Chapter 1.5 content using Claude Code for clarity and accuracy in `my-book/docs/module1/ch1.5.mdx`
- [x] T038 [US3] Refine Chapter 1.7 content using Claude Code for clarity and accuracy in `my-book/docs/module1/ch1.7.mdx`
- [x] T039 [US3] Add necessary Python code examples for Chapter 1.5, verified against ROS 2 Humble, in `my-book/docs/module1/ch1.5.mdx`
- [x] T040 [US3] Integrate mini-project instructions for Chapter 1.7 into `my-book/docs/module1/ch1.7.mdx`
- [x] T041 [US3] Update `sidebars.js` to include Chapter 1.5 and 1.7

**Checkpoint**: All user stories should now be independently functional

---

## Final Phase: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [x] T042 Ensure all Docusaurus `npm run build` checks pass without warnings or errors.
- [x] T043 Run Docusaurus link checker to ensure no broken links or images.
- [x] T044 Verify GitHub Pages deployment correctly renders all docs, sidebars, assets, and images.
- [x] T045 Conduct a final review of all chapters for clarity, accuracy, and consistency.
- [x] T046 Ensure all code snippets in all chapters run successfully on target environments (workstation + Jetson).
- [x] T047 Verify that all Spec-Kit Plus expansions used produce structurally consistent chapters.

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3)
- **Polish (Final Phase)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P1)**: Can start after Foundational (Phase 2) - May integrate with US1 but should be independently testable
- **User Story 3 (P2)**: Can start after Foundational (Phase 2) - May integrate with US1/US2 but should be independently testable

### Within Each User Story

- Tests (if included) MUST be written and FAIL before implementation
- Models before services
- Services before endpoints
- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes, all user stories can start in parallel (if team capacity allows)
- All tests for a user story marked [P] can run in parallel
- Models within a story marked [P] can run in parallel
- Different user stories can be worked on in parallel by different team members

---

## Parallel Example: User Story 1

```bash
# Launch all tests for User Story 1 together (if tests requested):
Task: "Contract test for [endpoint] in tests/contract/test_[name].py"
Task: "Integration test for [user journey] in tests/integration/test_[name].py"

# Launch all models for User Story 1 together:
Task: "Create [Entity1] model in src/models/[entity1].py"
Task: "Create [Entity2] model in src/models/[entity2].py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Test User Story 1 independently
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 → Test independently → Deploy/Demo
4. Add User Story 3 → Test independently → Deploy/Demo
5. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1
   - Developer B: User Story 2
   - Developer C: User Story 3
3. Stories complete and integrate independently

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Verify tests fail before implementing
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence
