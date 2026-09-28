# Navigation and control regression tests

Add focused tests that render Medarcy's real application shell and exercise the controls most likely to reveal React hook or context failures.

1. Set up Vitest with a browser-like test environment and React Testing Library, plus a `test` script. Keep this test-only setup separate from the production application.
2. Render the shell inside a real TanStack Router context, rather than mocking navigation hooks. Assert that workspace links and recent sessions render, navigation changes the visible page title, and the navigation drawer opens and closes.
3. Exercise the global search results, profile dropdown, and Clinical Review confirmation dialog. Assert that each interaction remains usable and that no invalid-hook, missing-context, or uncaught render errors occur; fail tests on unexpected React console errors.
4. Run the new tests and verify the preview still loads on desktop and mobile without errors. Do not add backend behavior or change the clinical sample content.

## Technical approach

Use Vitest, jsdom, `@testing-library/react`, and `@testing-library/user-event`. Test the actual router-backed components and accessibility-facing controls, with lightweight mocks only for unrelated browser APIs where needed. Keep tests deterministic and runnable through `bunx vitest run`.
