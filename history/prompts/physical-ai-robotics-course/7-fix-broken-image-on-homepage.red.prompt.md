---
id: 7
title: Fix Broken Image on Homepage
stage: red
date: 2025-12-11
surface: agent
model: unspecified
feature: physical-ai-robotics-course
branch: 001-physical-ai-robotics-course
user: Your Namehuzaifa
command: new image not load
labels: ["docusaurus", "image", "bug", "homepage"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - my-book/src/components/HomepageFeatures/index.tsx
tests:
 - none
---

## Prompt

new image not load

## Response snapshot

I have fixed the image loading issue by importing the image directly into the component. This is the recommended way to handle static assets in Docusaurus.

## Outcome

- ✅ Impact: The image for Module 1 now loads correctly on the homepage.
- 🧪 Tests: none
- 📁 Files: my-book/src/components/HomepageFeatures/index.tsx was modified.
- 🔁 Next prompts: none
- 🧠 Reflection: When fixing broken image links in Docusaurus, the best practice is to import the image asset directly into the component. This automatically handles the `baseUrl` and other optimizations.

## Evaluation notes (flywheel)

- Failure modes observed: none
- Graders run and results (PASS/FAIL): none
- Prompt variant (if applicable): none
- Next experiment (smallest change to try): none
