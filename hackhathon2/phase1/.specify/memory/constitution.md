<!-- SYNC IMPACT REPORT:
Version change: N/A → 1.0.0
List of modified principles: None (new constitution)
Added sections: All principles based on user requirements
Removed sections: None
Templates requiring updates:
  - .specify/templates/plan-template.md ✅ updated to reflect new constitution in Constitution Check section
  - .specify/templates/spec-template.md ⚠ pending review for alignment
  - .specify/templates/tasks-template.md ⚠ pending review for alignment
Follow-up TODOs: None
-->
# The Evolution of Todo Constitution

## Core Principles

### Spec-Driven Development ONLY
Follow: Constitution → Spec → Plan → Tasks → Implementation. Never write implementation code before specification approval.

### No Manual Coding by User
The AI agent must generate, modify, and refactor all code itself. The user does not write implementation code.

### Clean Architecture & Clean Code
Single Responsibility Principle, Clear naming, No dead code, Readable for junior developers.

### Python Project Standards
Python 3.11, In-memory storage ONLY, CLI-based interaction ONLY.

### Folder Structure Rules
Use `/src` for application source code, `/specs/history` for specification versions, and Root for README.md, CLAUDE.md.

### Tooling Requirements
Use `uv` for environment and dependency management, Standard library only unless explicitly approved.

## Output Expectations
Each phase must be runnable, All required features must be demonstrated via CLI, No persistence beyond runtime.

## Development Workflow
Show plans and task breakdowns, Save specification changes in `/specs/history`, Follow Spec-Kit Plus rules.

## Governance
Constitution supersedes all other practices. Amendments require documentation and approval. All implementation must follow this constitution. Failure conditions: Writing code without approved spec, Skipping phases, Asking user to write code, Violating project structure.

**Version**: 1.0.0 | **Ratified**: 2026-01-02 | **Last Amended**: 2026-01-02