# City Report Frontend - Gemini AI Configuration

This file contains rules and guidelines for developing the Angular frontend. You **MUST** follow these rules. For global project workflows, refer to the root `GEMINI.md` file.

## 1. Core Principles & Style

- **UI Style Guide:** All UI development **MUST** strictly follow the guidelines in `UI_STYLE_GUIDE.md`. Read it before any UI work.
- **Architecture:** The application is organized into `pages` (top-level routed components), `components` (reusable UI elements), and `services` (business logic and API communication).
- **Single Responsibility:** Components and services must be small and focused on a single responsibility.
- **Keep Templates Simple:** Avoid complex logic in HTML templates. Delegate logic to the component's TypeScript class.

## 2. Angular Best Practices

- **Standalone Components:** **Always** use standalone components. Do not use NgModules. The CLI will generate standalone components by default.
- **Change Detection:** **Always** set `changeDetection: ChangeDetectionStrategy.OnPush` in the `@Component` decorator to improve performance.
- **Host Bindings:** **Do NOT** use `@HostBinding` or `@HostListener`. Place host bindings inside the `host: { ... }` property of the `@Component` decorator.
- **Control Flow:** **Always** use the new built-in control flow (`@if`, `@for`, `@switch`) instead of the old `*ngIf`, `*ngFor`, `*ngSwitch` directives.
- **Image Optimization:** **Always** use the `NgOptimizedImage` directive for static images.

## 3. State Management with Signals

- **Local State:** **Always** use Signals for managing local component state.
- **Derived State:** **Always** use `computed()` for state that is derived from other signals.
- **Immutability:** **Do NOT** use `mutate()` on signals. State changes must be immutable. Use `set()` or `update()` to change signal values, ensuring transformations are pure and predictable.
- **Inputs:** **Always** use the `input()` function for component inputs (e.g., `name = input<string>()`). Do not use the `@Input()` decorator.

## 4. TypeScript Best Practices

- **Strict Typing:** The project uses strict type checking.
- **Avoid `any`:** **Do NOT** use the `any` type. Use `unknown` when a type is uncertain and handle it safely.
- **Type Inference:** Prefer type inference for simple types where the value is obvious (e.g., `const name = 'John';`), but provide explicit types for complex objects and function signatures.

## 5. Forms

- **Reactive Forms:** **Always** prefer Reactive Forms over Template-driven forms for their explicitness and scalability.
- **Typed Forms:** Use strongly typed forms to ensure type safety.

## 6. Services & Dependency Injection

- **Singleton Services:** Use `providedIn: 'root'` for services that should be singletons.
- **Injection:** **Always** use the `inject()` function for dependency injection within your constructor. Do not rely on constructor parameter type inference alone.

## 7. Testing Best Practices

- **Frameworks:** Tests are written with **Jasmine** and run with **Karma**.
- **AAA Pattern:** Structure your tests using the Arrange-Act-Assert pattern.
- **Isolation & Mocks:** Tests **MUST** be isolated. Use spies (`spyOn`) and mock dependencies for services and child components to ensure a component is tested in isolation. Configure these in the `providers` array of `TestBed`.
- **`TestBed`:** Use `TestBed` to configure the testing environment.
- **Asynchronous Code:** Use the `async` and `fakeAsync` testing utilities to handle asynchronous operations.
- **TDD Workflow:** Follow the TDD workflow outlined in the root `GEMINI.md` using the `/test:new` and `/test:fix` custom commands. New features and bug fixes must have corresponding tests.
