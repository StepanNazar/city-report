# City Report - Gemini AI Root Configuration

## 1. Project Overview

This is a monorepo for the **City Report** application. The project consists of two main parts:

- **Backend:** A Python API built with Flask.
- **Frontend:** An Angular single-page application.

This file contains global rules and workflows. For technology-specific guidelines, **you MUST refer to the `GEMINI.md` file located in the respective sub-directory** (`api/GEMINI.md` or `angular-app/GEMINI.md`).

## 2. General Software Engineering Principles

All code, in both the frontend and backend, MUST adhere to these fundamental principles:

- **YAGNI (You Ain't Gonna Need It):** Do not add functionality or code until it is actively required. Avoid speculative features.
- **DRY (Don't Repeat Yourself):** Avoid duplicating code. Create reusable functions, components, or services instead. Look for opportunities to refactor common logic into the `api/blueprints/common/` directory for the backend.
- **KISS (Keep It Simple, Stupid):** Prefer simple, clear, and straightforward solutions. Avoid unnecessary complexity.
- **SOLID:** Your object-oriented and component designs should follow SOLID principles (Single Responsibility, Open/Closed, Liskov Substitution, Interface Segregation, Dependency Inversion).

## 3. The "10x Developer" Workflow

To ensure speed and quality, you MUST use the following workflow, which is supported by custom commands.

### **The Workflow: Plan -> Test -> Implement -> Check**

1. **Plan (`/plan`):**

   - **All significant tasks MUST start with this command.**
   - First, fully understand the user's request. Then, ask for relevant files and create a detailed, step-by-step implementation plan.
   - The plan is your blueprint for action. Do not proceed without user approval of the plan.

1. **Test (`/test:new` and `/test:fix`):**

   - This is a Test-Driven Development (TDD) project.
   - After the plan is approved, use `/test:new` to write a failing test that captures the requirements of the feature or bug fix.
   - Confirm with the user that the test fails as expected.
   - Next, use `/test:fix` and provide the failing test's details to write the application code that makes the test pass.

1. **Implement (`/implement`):**

   - This command is an alternative for smaller tasks where a full TDD cycle might be overkill.
   - Use it to execute a pre-approved plan directly. You must still perform a self-review of your changes.

1. **Check (`/check-standards`):**

   - **Before finishing your work or committing code, you MUST run this command.**
   - It executes the linters (`ruff`, `ng lint`) for the entire project to ensure code quality and consistency.

## 4. Directory-Specific Instructions

- **Backend Development:** When your task involves the Python API, you **MUST** read and adhere to the rules in `api/GEMINI.md`.
- **Frontend Development:** When your task involves the Angular UI, you **MUST** read and adhere to the rules in `angular-app/GEMINI.md`.

## 5. Strict UI/UX Adherence

- All frontend development, including component creation, styling, and layout changes, **MUST** strictly follow the detailed guidelines in the `angular-app/UI_STYLE_GUIDE.md` file.
- Before starting any UI task, you **MUST** read and internalize the rules in that guide. Any deviation is not permitted.
