# Creating Custom Sequences

Custom sequences can be added when the Configuration Service needs a new deterministic startup step.

## Step 1: Implement the Interface

Create a type that implements `Execute(int) (int, error)` and `GetDescription(int) string`.

```go
package steps

import "fmt"

type ExampleSequence struct {
    ctx *ExecutionContext
}

func NewExampleSequence(ctx *ExecutionContext) *ExampleSequence {
    return &ExampleSequence{ctx: ctx}
}

func (es *ExampleSequence) Execute(stepIndex int) (int, error) {
    if es.ctx == nil || es.ctx.DB == nil {
        return 1, fmt.Errorf("BASYXCFG-EXAMPLE-NODB: database connection is not initialized")
    }

    // Execute deterministic startup work here.

    return 0, nil
}

func (es *ExampleSequence) GetDescription(stepIndex int) string {
    return fmt.Sprintf("[Step %d] Running example sequence", stepIndex)
}
```

## Step 2: Register the Sequence

Register the sequence in `cmd/basyxconfigurationservice/main.go` in the required order.

```go
schemInit.Register(steps.NewDatabaseConnection(execCtx, configPath))
schemInit.Register(steps.NewSystemTable(execCtx))
schemInit.Register(steps.NewSchemaUpload(execCtx, databaseSchema))
schemInit.Register(steps.NewExampleSequence(execCtx))
```

## Best Practices

- Keep each sequence focused on one responsibility.
- Return BaSyx-style error codes with the `BASYXCFG` prefix.
- Validate required context state at the beginning of `Execute`.
- Use deterministic ordering and avoid hidden side effects.
- Use PostgreSQL advisory locking for schema-changing operations.
- Use explicit transactions for operations that must be atomic.
- Keep sequence functions small enough to remain easy to review.

## Common Pitfalls

- Registering a sequence before its dependencies are available.
- Updating database schema without versioning the change as a patch.
- Performing long-running runtime operations in the startup initializer.
- Adding non-idempotent SQL to restartable initialization paths.

