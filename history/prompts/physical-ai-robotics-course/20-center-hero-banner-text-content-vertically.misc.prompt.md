---
phr_id: 20
phr_title: Center Hero Banner Text Content Vertically
phr_stage: misc
phr_date: 2025-12-12
phr_surface: agent
phr_model: 
phr_feature: physical-ai-robotics-course
phr_branch: 001-physical-ai-robotics-course
phr_user: 
phr_command: adjust the margin from top set in center of page of   "Physical AI & Humanoid Robotics Course
Teaching Embodied Intelligence and AI Systems in the Physical World"
phr_labels: []
phr_links: []
phr_files_yaml:
  - my-book/src/pages/index.tsx
  - my-book/src/pages/index.module.css
phr_tests_yaml: []
---

## Prompt

```text
adjust the margin from top set in center of page of   "Physical AI & Humanoid Robotics Course
Teaching Embodied Intelligence and AI Systems in the Physical World"
```

## Response

Modified `src/pages/index.tsx` to add a new class to the text content column and updated `src/pages/index.module.css` to vertically center its content, also ensuring the hero banner is `100vh`.

## Outcome

The hero banner text content is now vertically centered.
