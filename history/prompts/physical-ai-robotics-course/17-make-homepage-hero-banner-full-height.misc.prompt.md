---
phr_id: 17
phr_title: Make Homepage Hero Banner Full Height
phr_stage: misc
phr_date: 2025-12-12
phr_surface: agent
phr_model: 
phr_feature: physical-ai-robotics-course
phr_branch: 001-physical-ai-robotics-course
phr_user: 
phr_command: make the height of full page of header hero banner page
phr_labels: []
phr_links: []
phr_files_yaml:
  - my-book/src/pages/index.module.css
phr_tests_yaml: []
---

## Prompt

```text
make the height of full page of header  hero banner page
```

## Response

Modified `src/pages/index.module.css` to set `min-height: 100vh` for the `.heroBanner` class.

## Outcome

Homepage hero banner now takes full viewport height.
