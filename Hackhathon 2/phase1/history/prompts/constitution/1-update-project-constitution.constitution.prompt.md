---
id: 1
title: Update-project-constitution
stage: constitution
date: 2026-01-02
surface: agent
model: Claude Sonnet 4.5
feature: none
branch: master
user: user
command: /sp.constitution
labels: ["constitution", "spec-driven-development", "governance"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - .specify/memory/constitution.md
tests: []
---

## Prompt

```
You are an autonomous Product Architect and Software Agent operating under Spec-Kit Plus rules.

CORE PRINCIPLES
1. Spec-Driven Development ONLY.
   - Follow: Constitution → Spec → Plan → Tasks → Implementation.
   - Never write implementation code before specification approval.

2. No manual coding by the user.
   - You must generate, modify, and refactor all code yourself.

3. Clean Architecture & Clean Code are mandatory.
   - Single Responsibility Principle
   - Clear naming
   - No dead code
   - Readable for junior developers

4. Python Project Standards
   - Python 3.11
   - In-memory storage ONLY
   - CLI-based interaction ONLY

5. Folder Structure Rules
   - `/src` → application source code
   - `/specs/history` → all specification versions
   - Root → README.md, CLAUDE.md

6. Tooling
   - Use `uv` for environment and dependency management
   - Standard library only unless explicitly approved

7. Output Expectations
   - Each phase must be runnable
   - All required features must be demonstrated via CLI
   - No persistence beyond runtime

8. Transparency
   - Show plans and task breakdowns
   - Save specification changes in `/specs/history`

FAILURE CONDITIONS
- Writing code without an approved spec
- Skipping phases
- Asking the user to write code
- Violating project structure

GOAL
Execute Phase I of "The Evolution of Todo" faithfully using Spec-Kit Plus.
```

## Response snapshot

Updated the project constitution file (.specify/memory/constitution.md) with the core principles specified by the user, including Spec-Driven Development, No Manual Coding by User, Clean Architecture & Clean Code, Python Project Standards, Folder Structure Rules, Tooling Requirements, Output Expectations, and Development Workflow. The constitution is now properly configured for the "The Evolution of Todo" project with version 1.0.0.

## Outcome

- ✅ Impact: Created initial project constitution with all required principles
- 🧪 Tests: N/A
- 📁 Files: Updated .specify/memory/constitution.md with new constitution
- 🔁 Next prompts: Ready to proceed with spec creation using /sp.specify
- 🧠 Reflection: Constitution now properly enforces Spec-Driven Development workflow

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): PASS - All constitution requirements met
- Prompt variant (if applicable): Initial constitution setup
- Next experiment (smallest change to try): Create feature specification using /sp.specify