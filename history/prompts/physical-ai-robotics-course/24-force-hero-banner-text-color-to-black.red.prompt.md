---
phr_id: 24
phr_title: Force Hero Banner Text Color to Black
phr_stage: red
phr_date: 2025-12-12
phr_surface: agent
phr_model: 
phr_feature: physical-ai-robotics-course
phr_branch: 001-physical-ai-robotics-course
phr_user: 
phr_command: not change
phr_labels: []
phr_links: []
phr_files_yaml:
  - my-book/src/css/custom.css
  - my-book/src/pages/index.module.css
phr_tests_yaml: []
---

## Prompt

```text
not change
```

## Response

Moved the `color: black;` rule for `.hero__title` and `.hero__subtitle` to the global `src/css/custom.css` file to increase its specificity and ensure it overrides default theme styles.

## Outcome

The hero banner text color should now correctly be black.
