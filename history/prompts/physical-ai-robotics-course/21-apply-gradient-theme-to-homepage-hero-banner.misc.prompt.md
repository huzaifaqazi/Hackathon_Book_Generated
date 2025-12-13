---
phr_id: 21
phr_title: Apply Gradient Theme to Homepage Hero Banner
phr_stage: misc
phr_date: 2025-12-12
phr_surface: agent
phr_model: 
phr_feature: physical-ai-robotics-course
phr_branch: 001-physical-ai-robotics-course
phr_user: 
phr_command: this theme i want #c31432->#240b36 
how to integrate  in this code --ifm-color-primary: #c31432 ;
phr_labels: []
phr_links: []
phr_files_yaml:
  - my-book/src/css/custom.css
  - my-book/src/pages/index.module.css
  - my-book/src/pages/index.tsx
phr_tests_yaml: []
---

## Prompt

```text
this theme i want #c31432->#240b36 
how to integrate  in this code --ifm-color-primary: #c31432 ;
```

## Response

Modified `src/css/custom.css` to add a secondary color, `src/pages/index.module.css` to apply a linear gradient, and `src/pages/index.tsx` to remove the default primary color class.

## Outcome

The hero banner now has a gradient background.
