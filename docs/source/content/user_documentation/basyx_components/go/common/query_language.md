# Query Language

BaSyx Go supports the [AAS Query Language defined by IDTA-01002 v3.2](https://industrialdigitaltwin.io/aas-specifications/IDTA-01002/v3.2/query-language.html) for selecting repository resources and Registry descriptors and filtering fragments inside returned objects. This page covers the BaSyx Go extensions and deviations from the standard. Use the component's Swagger UI to check endpoint availability, URL parameters, and general request and response shapes. Use this page for the runtime-specific query grammar and semantics.

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

Each `$filters` entry requires both `$fragment` and `$condition`. The standard defines only those members. BaSyx Go additionally supports a Boolean `$match` extension for row-local fragment filtering. This flag is distinct from the logical `$match` expression used inside `$condition`:

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
IDTA-01002 v3.2 defines `$select: "id"` as a projection that returns identifiers. BaSyx Go does not implement this projection and rejects the standardized string form. Omit `$select` in query requests. Although the runtime accepts a non-standard array form, it does not project the response and should not be relied on. `$filters` serve a different purpose: they conditionally retain or prune supported fragments.
```

For example, query a local AAS Repository for shells whose `idShort` is `MotorAAS`:

```bash
curl -sS -X POST 'http://localhost:8084/query/shells?limit=1' -H 'Content-Type: application/json' -d '{"$condition":{"$eq":[{"$field":"$aas#idShort"},{"$strVal":"MotorAAS"}]}}'
```

A successful response uses the endpoint's normal paging envelope:

```json
{
  "paging_metadata": {},
  "result": [
    {
      "modelType": "AssetAdministrationShell",
      "id": "urn:example:aas:motor",
      "idShort": "MotorAAS",
      "assetInformation": { "assetKind": "Instance" }
    }
  ]
}
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

### Field Paths

A field reference uses `$field` and separates its model selector from its field with `#`:

```text
$aas#assetInformation.globalAssetId
$sm#semanticId.keys[].value
$sme#value
$sme.Metrics.Temperature#value
$aasdesc#submodelDescriptors[].idShort
$smdesc#endpoints[0].protocolinformation.href
$cd#idShort
```

Use dots for nested object members. For supported list paths, `[]` addresses any entry and `[0]`, `[1]`, and so on address one zero-based position. The part between `$sme.` and `#` is the dot-separated `idShort` path of the element and may also contain list selectors. Omitting that path, as in `$sme#value`, searches matching Submodel Elements recursively across the relevant Submodel Element hierarchy. `$sme.Metrics.Temperature#value` targets the explicit path.

Field names and roots are case-sensitive. For descriptor endpoint URLs, the query token is `protocolinformation.href` with a lowercase `i`, even though the regular AAS JSON property is `protocolInformation`. The accepted paths are an explicit subset of the model, so a field that exists in an AAS JSON document is not automatically queryable.

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

The language also provides explicit cast and date-part expressions:

| Expression | Accepted operand |
| --- | --- |
| `$strCast`, `$numCast`, `$boolCast`, `$hexCast` | Any valid value expression |
| `$dateTimeCast` | A string-valued expression, including a field, string literal, or `$strCast` |
| `$timeCast` | A string-valued or date-time expression |
| `$year`, `$month`, `$dayOfMonth`, `$dayOfWeek` | A date-time expression, such as `$dateTimeVal` or `$dateTimeCast` |

For example:

```json
{
  "$lt": [
    { "$numCast": { "$field": "$sme.Temperature#value" } },
    { "$numVal": 48 }
  ]
}
```

With the default `general.enableImplicitCasts: true`, BaSyx can convert a field operand to the type of the other operand where the conversion is supported. Explicit casts make the intended interpretation clear and remain useful when values such as Property `value` are stored as text. The public query language has no null or list literal and no membership operator.

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

Direct children of a logical `$match` are limited to comparison expressions, string expressions, or another `$match`. They cannot be arbitrary `$and`, `$or`, `$not`, or `$boolean` expressions.

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

### Fragment Paths

`$fragment` identifies a part of the returned representation, while `$field` identifies a scalar value used by a condition. The two therefore use different allowed path sets: a valid `$field` path is not automatically a valid `$fragment` path.

In the table below, `[i]` means either a wildcard `[]` or one non-negative index such as `[0]`.

| Root | Supported fragment forms |
| --- | --- |
| `$aas` | `#idShort`; `#assetInformation.assetType`; `#assetInformation.globalAssetId`; `#assetInformation.specificAssetIds[i]`, optionally followed by `.externalSubjectId` or `.externalSubjectId.keys[i]`; `#submodels[i]`, optionally followed by `.keys[i]` |
| `$sm` | `#id`, `#idShort`; `#semanticId` or `#semanticId.keys[i]`; `#supplementalSemanticIds` or `#supplementalSemanticIds[i]`, with optional `.keys[i]` |
| `$sme` | `$sme` or `$sme.<idShortPath>` for an element; either form may select `#idShort`, `#value`, `#valueType`, `#language`, `#semanticId`, `#semanticId.keys[i]`, `#supplementalSemanticIds` or `#supplementalSemanticIds[i]`, with optional `.keys[i]` |
| `$cd` | `#idShort` |
| `$aasdesc` | `#idShort`, `#description`, `#displayName`, `#extension`, `#administration`, `#assetKind`, `#assetType`, `#globalAssetId`; `#specificAssetIds[i]` forms as above; `#endpoints[i]`; `#submodelDescriptors[i]`, optionally followed by `.idShort`, `.semanticId`, `.semanticId.keys[i]`, `.supplementalSemanticIds` or `.supplementalSemanticIds[i]` with optional `.keys[i]`, or `.endpoints[i]` |
| `$smdesc` | `#idShort`; `#semanticId` or `#semanticId.keys[i]`; `#supplementalSemanticIds` or `#supplementalSemanticIds[i]`, with optional `.keys[i]`; `#endpoints[i]` |

The selected root must also be valid for the query endpoint.

### Fragment Filters

`$fragment` identifies a supported field, object, or list within the returned parent. Its `$condition` determines whether that fragment remains visible. It does not determine whether the parent is included in `result`.

When the filter's Boolean `$match` is omitted or `false`, its condition is evaluated at parent scope. If any relevant nested entry satisfies the condition, the complete fragment is preserved. For a Submodel with ten `supplementalSemanticIds`, if one has the requested key value, all ten remain in the response.

When the BaSyx-specific `$match` flag is `true`, the condition is evaluated against each current fragment row. Only matching rows remain. With the same ten references, the response retains only those whose own data satisfies the condition. If no row matches, the fragment is empty or omitted as appropriate for that representation, but the parent can still remain in `result` because parent selection is controlled by the top-level `$condition`.

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

The query language provides no caller-controlled sort expression. Results use the endpoint's server-defined cursor order. Clients should not rely on another ordering.

## Limits

BaSyx Go accepts at most 64 JSON container nesting levels and 8192 JSON tokens in a query. Queries that exceed either complexity limit are rejected with `400 Bad Request`.

## Authorization Filters

When runtime authorization supplies an ABAC query filter, BaSyx combines the caller's top-level condition with the authorization condition using `AND`. A caller can narrow the visible result set but cannot broaden it beyond the policy. On a fragment that both the policy and caller filter, both restrictions must hold, so caller filters cannot recover rows hidden by ABAC.

ABAC formulas and filters use the same condition and field syntax, with additional policy-only attribute expressions. See [Runtime Security](security) for authorization outcomes and resource filtering. The access policy, not the request, remains the upper bound on visible parent resources and fragments.

## See Also

- [Pagination](pagination) for cursor handling.
- [Runtime Security](security) for OIDC, ABAC, and authorization filters.
- [Swagger UI and OpenAPI](swagger) for endpoint schemas and availability in the running component.
