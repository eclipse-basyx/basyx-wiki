# BaSyx Configuration Service Developer Documentation

This documentation describes the internal architecture and extension points of the BaSyx Configuration Service.

The service is implemented as a small ordered sequence runner. It connects to PostgreSQL, prepares the BaSyx schema-version table, uploads the base schema when needed, and applies explicitly registered SQL patches.

## Documentation

- [Architecture Overview](architecture.md)
- [Execution Flow](execution-flow.md)
- [Sequences](sequences.md)
- [Creating Custom Sequences](custom-sequences.md)
- [Patches](patches.md)
- [Database Patch Structure](database-patch-structure.md)
- [Release Advisor](release-advisor.md)
- [Extensibility Guidelines](extensibility.md)

```{toctree}
:hidden:
:maxdepth: 1

architecture
execution-flow
sequences
custom-sequences
patches
database-patch-structure
release-advisor
extensibility
```
