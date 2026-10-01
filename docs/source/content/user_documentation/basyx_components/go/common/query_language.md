# Query Language

BaSyx Go query endpoints use a shared JSON query language to select repository resources and Registry descriptors and to filter fragments inside returned objects. This page describes the behavior released in BaSyx Go v1.1.0. Use the component's Swagger UI for the exact endpoint request and response schemas.

## Supported Endpoints

| Component | Endpoint | Returned object | Valid field roots |
| --- | --- | --- | --- |
| AAS Repository | `POST /query/shells` | Asset Administration Shell | `$aas` |
| AAS Environment | `POST /query/shells` | Asset Administration Shell | `$aas`, plus referenced local `$sm` and `$sme` data |
| Submodel Repository and AAS Environment | `POST /query/submodels` | Submodel | `$sm`, `$sme` |
| AAS Registry, Digital Twin Registry, and AAS Environment | `POST /query/shell-descriptors` | AAS Descriptor | `$aasdesc`; embedded Submodel Descriptors use `submodelDescriptors[]` paths |
| Submodel Registry and AAS Environment | `POST /query/submodel-descriptors` | Submodel Descriptor | `$smdesc` |
| Concept Description Repository and AAS Environment | `POST /query/concept-descriptions` | Concept Description | `$cd` |

The standalone AAS Repository rejects `$sm` and `$sme` fields on `/query/shells` with `400 Bad Request`. Only the AAS Environment follows the candidate AAS's model references into locally stored Submodels and Submodel Elements. Registry roots address descriptors, not Repository resources: `$aasdesc` is not interchangeable with `$aas`, and `$smdesc` is not interchangeable with `$sm`.

The Digital Twin Registry exposes the same `/query/shell-descriptors` language as the standalone AAS Registry API. Query support is not a DTR-specific extension.

## Query Structure

Every request requires a top-level `$condition`. It determines which parent objects appear in `result`. Optional `$filters` entries control fragments inside those returned objects.

```json
{
  "$condition": {
    "$eq": [
      { "$field": "$aas#idShort" },
      { "$strVal": "MotorAAS" }
    ]
  }
}
```

Each `$filters` entry requires both `$fragment` and `$condition` and may set the Boolean `$match` flag:

```json
{
  "$condition": { "$boolean": true },
  "$filters": [
    {
      "$fragment": "$sm#supplementalSemanticIds[]",
      "$match": true,
      "$condition": {
        "$eq": [
          { "$field": "$sm#supplementalSemanticIds[].keys[].value" },
          { "$strVal": "urn:example:semantic:public" }
        ]
      }
    }
  ]
}
```

Unknown members, a missing `$condition`, malformed expressions, unsupported field paths, and roots that are invalid for the endpoint result in `400 Bad Request`.

```{note}
The v1.1.0 runtime accepts a `$select` member in the shared query model, but it does not apply `$select` as a response projection. Use `$filters` to control supported result fragments.
```

## Fields

### Field Roots

The root identifies the model being addressed:

| Root | Refers to |
| --- | --- |
| `$aas` | An Asset Administration Shell |
| `$sm` | A Submodel |
| `$sme` | A Submodel Element |
| `$aasdesc` | An AAS Descriptor, including paths into its embedded Submodel Descriptors |
| `$smdesc` | A Submodel Descriptor |
| `$cd` | A Concept Description |

`$bd` also exists in the shared grammar for Basic Discovery authorization filters, but v1.1.0 does not expose a public Basic Discovery query-language endpoint.

### Field Paths

A field reference uses `$field` and separates its model selector from its field with `#`:

```text
$aas#assetInformation.globalAssetId
$sm#semanticId.keys[].value
$sme.Metrics.Temperature#value
$aasdesc#submodelDescriptors[].idShort
$smdesc#endpoints[0].protocolinformation.href
$cd#idShort
```

Use dots for nested object members. For supported list paths, `[]` addresses any entry and `[0]`, `[1]`, and so on address one zero-based position. The part between `$sme.` and `#` is the dot-separated `idShort` path of the element. It may also contain list selectors. Field names and roots are case-sensitive. The accepted paths are an explicit subset of the model, so a field that exists in an AAS JSON document is not automatically queryable. Consult the endpoint's v1.1.0 Swagger schema and use the patterns above rather than arbitrary JSON paths.

### Values and Types

Values are typed expressions rather than bare JSON scalars:

| Expression | Value |
| --- | --- |
| `{ "$strVal": "Motor" }` | String |
| `{ "$numVal": 48 }` | Number |
| `{ "$boolean": true }` | Boolean; it can also be a complete condition |
| `{ "$dateTimeVal": "2026-01-15T10:30:00Z" }` | RFC 3339 date-time |
| `{ "$timeVal": "10:30:00Z" }` | RFC 3339 full-time |
| `{ "$hexVal": "16#FF" }` | Uppercase hexadecimal literal |

The language also provides explicit `$strCast`, `$numCast`, `$boolCast`, `$dateTimeCast`, `$timeCast`, and `$hexCast` wrappers. `$year`, `$month`, `$dayOfMonth`, and `$dayOfWeek` extract a numeric part from a date-time expression. For example:

```json
{
  "$lt": [
    { "$numCast": { "$field": "$sme.Temperature#value" } },
    { "$numVal": 48 }
  ]
}
```

With the default `general.enableImplicitCasts: true`, BaSyx can convert a field operand to the type of the other operand where the conversion is supported. Explicit casts make the intended interpretation clear and remain useful when values such as Property `value` are stored as text. The public query language has no null or list literal and no membership operator in v1.1.0.

## Conditions and Operators

Every expression object contains exactly one operator.

### Comparison and String Operators

| Operators | Meaning | Operands |
| --- | --- | --- |
| `$eq`, `$ne` | Equal, not equal | Exactly two compatible values; booleans are supported |
| `$gt`, `$ge`, `$lt`, `$le` | Greater than, greater than or equal, less than, less than or equal | Exactly two compatible ordered values |
| `$contains` | Contains | Exactly two string expressions |
| `$starts-with`, `$ends-with` | Starts or ends with | Exactly two string expressions |
| `$regex` | Matches a regular expression | Exactly two string expressions |

String matching is case-sensitive. Field-to-field comparisons and field-to-field string operations are not supported. Use a field and an appropriately typed literal or cast in normal API queries.

### Logical Operators

| Operator | Shape | Meaning |
| --- | --- | --- |
| `$and` | Array of at least two conditions | All child conditions must hold |
| `$or` | Array of at least two conditions | At least one child condition must hold |
| `$not` | One condition | Negates the child condition |
| `$match` | Array of at least one match expression | All child predicates must hold in one shared list or hierarchy scope |
| `$boolean` | `true` or `false` | Constant condition |

`$match` is not simply another spelling of `$and`. It correlates predicates that address nested data. The separate Boolean `$match` inside a fragment filter has a different purpose, described below.

## Querying Nested Data

### Parent Selection

A condition on a wildcard list path is existential: the parent qualifies when at least one relevant nested entry satisfies that predicate. The parent resource is returned once, not once per matching child. A top-level condition selects parents but does not remove their non-matching nested content.

Predicates inside `$and` have independent nested scopes. They may therefore be satisfied by different list entries or, in an AAS Environment hierarchy query, different referenced Submodels. Use the logical `$match` operator when the predicates must describe the same entry or hierarchy branch.

For example, this AAS Environment query requires one referenced `CarbonFootprint` Submodel to contain a matching element value:

```json
{
  "$condition": {
    "$match": [
      {
        "$eq": [
          { "$field": "$sm#idShort" },
          { "$strVal": "CarbonFootprint" }
        ]
      },
      {
        "$lt": [
          { "$numCast": { "$field": "$sme.AggregatedCarbonFootprint#value" } },
          { "$numVal": 48 }
        ]
      }
    ]
  }
}
```

With `$and` instead, one referenced Submodel could satisfy the `idShort` condition while another supplies the matching element.

### Fragments and Fragment Filters

`$fragment` identifies a supported field, object, or list within the returned parent. Its `$condition` determines whether that fragment remains visible. It does not determine whether the parent is included in `result`.

When the filter's Boolean `$match` is omitted or `false`, its condition is evaluated at parent scope. If any relevant nested entry satisfies the condition, the complete fragment is preserved. For a Submodel with ten `supplementalSemanticIds`, if one has the requested key value, all ten remain in the response.

When the filter sets `$match: true`, the condition is evaluated against each current fragment row. Only matching rows remain. With the same ten references, the response retains only those whose own data satisfies the condition. If no row matches, the fragment is empty or omitted as appropriate for that representation, but the parent can still remain in `result` because parent selection is controlled by the top-level `$condition`.

Multiple filters for the same fragment are combined with `AND`. Filters for different fragments are applied independently. Explicit indices restrict filtering to the selected position. Unselected siblings remain unchanged.

### MultiLanguageProperty Entries

For a `MultiLanguageProperty`, `$sme.<path>#value` addresses language-string text and `$sme.<path>#language` addresses the language. With `$and`, the text and language predicates may be satisfied by different entries. Put both predicates in a logical `$match` when they must refer to the same language-string entry. The top-level condition still returns the complete property. Use a fragment filter only when returned nested data should also be reduced.

## More Examples

Combine conditions with `$and`:

```json
{
  "$condition": {
    "$and": [
      {
        "$starts-with": [
          { "$field": "$sm#idShort" },
          { "$strVal": "Motor" }
        ]
      },
      {
        "$eq": [
          { "$field": "$sme.Status#value" },
          { "$strVal": "READY" }
        ]
      }
    ]
  }
}
```

Select AAS Descriptors by an embedded Submodel Descriptor field:

```json
{
  "$condition": {
    "$eq": [
      { "$field": "$aasdesc#submodelDescriptors[].idShort" },
      { "$strVal": "Nameplate" }
    ]
  }
}
```

The first request is valid for `/query/submodels`. The second is valid for `/query/shell-descriptors`. A field root valid for one endpoint is not automatically valid for another.

## Results and Pagination

Successful query responses contain the endpoint's top-level objects in `result` and continuation information in `paging_metadata`. Each matching top-level resource appears once even when several nested entries match. Fragment filters and runtime authorization may remove fields or nested entries from each returned representation.

Query endpoints accept `limit` and `cursor` as URL query parameters. Omit the cursor for the first page, then send the returned opaque cursor with the same request body and `limit` for the next page. See [Pagination](pagination) for the shared response and cursor rules.

v1.1.0 provides no caller-controlled sort expression. Results use the endpoint's server-defined cursor order. Clients should not rely on another ordering.

## Authorization Filters

When runtime authorization supplies an ABAC query filter, BaSyx combines the caller's top-level condition with the authorization condition using `AND`. A caller can narrow the visible result set but cannot broaden it beyond the policy. On a fragment that both the policy and caller filter, both restrictions must hold, so caller filters cannot recover rows hidden by ABAC.

ABAC formulas and filters use the same condition and field syntax, with additional policy-only attribute expressions. See [Runtime Security](security) for authorization outcomes and resource filtering. The access policy, not the request, remains the upper bound on visible parent resources and fragments.

## See Also

- [Pagination](pagination) for cursor handling.
- [Runtime Security](security) for OIDC, ABAC, and authorization filters.
- [Swagger UI and OpenAPI](swagger) for endpoint schemas and availability in the running component.
