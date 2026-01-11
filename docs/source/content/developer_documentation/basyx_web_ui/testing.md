# Testing & Quality Assurance

This section describes how testing is set up in the **BaSyx AAS Web UI**, how to run tests locally, and what is expected from contributors when adding or changing code.

The Web UI is a frontend application, so the project currently focuses on **high-value unit tests** (especially for utilities). Broader testing (components, stores, E2E) may be expanded over time.

## Testing Philosophy

What is tested today

* **Utilities** (`utils`): tests are considered mandatory
* **Composables**: tests are encouraged when logic is non-trivial

Many composables contain AAS-related logic. Over time, parts of this logic may move into the BaSyx TypeScript SDK, which follows a more strict, SDK-style testing approach.

What is not set up (yet)

* End-to-end tests (E2E)
* Visual regression tests
* System tests against real BaSyx infrastructures
* A dedicated test strategy for stores and UI components

```{note}
The current test focus reflects a pragmatic tradeoff: this repository is a UI application (not an SDK), and the most critical correctness risks are concentrated in reusable utility logic.
```

## Tooling

The project uses:

* **Vitest** as the unit test framework
* **@vue/test-utils** for Vue-related test utilities (as needed)
* **@vitest/ui** for interactive test runs
* **@vitest/coverage-istanbul** for coverage reports

The Vitest configuration is defined in `vitest.config.mts` and reuses the Vite configuration.

Key settings:

* `environment: 'jsdom'`
* `globals: true`
* Coverage provider: Istanbul
* Reporters: `text`, `json`, `html`

Coverage output directory:

* `./coverage`

## Test Location and Naming

Tests are located under:

```
src/tests/
  utils/
  composables/
```

Conventions:

* Tests are named after the file they test
* File naming uses the `<file-name>.tests.ts` suffix

Example:

```
src/tests/utils/IDUtils.tests.ts
```

## Running Tests

From the `aas-web-ui/` directory:

### Run all tests

```bash
yarn test
```

### Run tests in watch mode

```bash
yarn test:watch
```

### Run tests with UI

```bash
yarn test:ui
```

### Run coverage

```bash
yarn test:coverage
```

This generates coverage reports in:

* `coverage/` (HTML, JSON, and text)

## CI and Build Integration

Tests are executed as part of the production build checks:

* `prebuild` runs
  * `yarn lint:check`
  * `vitest run`
  * `vue-tsc --noEmit`

No minimum coverage threshold is enforced in CI at the moment.

```{note}
Coverage is currently collected for local insight rather than as a strict quality gate.
```

## Writing Tests

### Utilities (Required)

Utility functions should be tested with deterministic, focused unit tests.

A typical pattern in the repository is:

* Prepare input data sets
* Execute the function under test
* Assert predictable outputs and invariants

Example patterns include property-based style iterations (e.g., generating multiple IDs and validating a regex), as used in existing test files.

### Composables (Recommended)

Composable tests are recommended when:

* The composable contains meaningful data transformation logic
* The composable implements non-trivial fallback behavior
* The composable performs validation or mapping between AAS types

When a composable depends on Pinia, initialize Pinia explicitly:

```ts
import { createPinia, setActivePinia } from 'pinia';

const pinia = createPinia();
setActivePinia(pinia);
```

### Mocking and External Calls

Unit tests must not depend on:

* Real backend services
* External infrastructures
* Live authentication flows

At the moment, backend access is not a primary testing focus in this repository. As backend communication is increasingly handled by the BaSyx TypeScript SDK, testing of API behavior will primarily happen at the SDK level.

## Common Pitfalls

### Alias Imports

The project uses `@/` alias imports. If a test fails due to module resolution issues, ensure:

* The test is executed via the standard scripts (`yarn test`, `yarn test:watch`, etc.)
* The Vite/Vitest configuration is used (do not run Vitest with custom flags that bypass config)

## Summary

* Unit tests are run via Vitest (jsdom)
* Tests live in `src/tests/`
* Utilities must be tested
* Composable tests are encouraged for non-trivial logic
* No E2E or visual regression setup exists yet
* Coverage reports are generated locally but not enforced in CI