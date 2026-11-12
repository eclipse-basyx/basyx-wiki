# MCP Endpoint

```{warning}
The MCP endpoint is an experimental feature, available from BaSyx Go v1.1.3. Its configuration, tools, tool parameters, and results may change.
```

```{note}
The [BaSyx MCP Example](https://github.com/eclipse-basyx/basyx-go-components/tree/v1.1.3/examples/BaSyxMCPExample) runs a local AAS Environment with the MCP endpoint and writes enabled, preloaded with a drive motor AAS, and shows how to connect Claude Code and Codex. Its `secured` variant adds Keycloak sign-in, two users with different permissions, and a realm configured as described in [Example: Keycloak](#example-keycloak).
```

The AAS Environment can serve a [Model Context Protocol](https://modelcontextprotocol.io) (MCP) endpoint next to its REST API. AI agents and other MCP clients, such as Claude Code or Codex, use it to read and change Asset Administration Shells, Submodels, and Submodel Elements.

Each tool call is turned into a request to the AAS Environment API inside the same process, carrying the caller's bearer token. Authentication, ABAC and ReBAC rules, validation, conditional requests, history, and eventing therefore apply exactly as they do to REST calls. The MCP endpoint grants no access that the REST API does not grant to the same user.

The endpoint is disabled by default. When enabled, it offers only read tools unless writes are enabled explicitly.

## Enable the Endpoint

| Setting | Environment variable | Default | Purpose |
| --- | --- | --- | --- |
| `mcp.enabled` | `MCP_ENABLED` | `false` | Serves the MCP endpoint. |
| `mcp.path` | `MCP_PATH` | `/mcp` | Endpoint path below `server.contextPath`. Must start with `/`, must not be `/` or end with `/`, and must not contain `?`, `#`, `%`, `{`, `}`, `*`, or `..`. |
| `mcp.writesEnabled` | `MCP_WRITESENABLED` | `false` | Also offers the tools that create, change, and delete data. |
| `mcp.maxResultBytes` | `MCP_MAXRESULTBYTES` | `262144` | Largest API response in bytes that a tool returns to the client. Must be at least `1024`. |

For example, add the following to the `environment` of the `aas_environment` service in the [first-use setup](setup), which already sets `GENERAL_EXTERNALURL: http://localhost:8090`:

```yaml
MCP_ENABLED: "true"
MCP_WRITESENABLED: "true"
```

The public endpoint URL is the first `general.externalUrl` entry followed by `mcp.path`, for example `http://localhost:8090/mcp`. Without `general.externalUrl`, the service uses `http://localhost:<server.port><server.contextPath><mcp.path>`. Set `general.externalUrl` to the URL that clients actually use, because the secured endpoint publishes this URL as its OAuth resource identifier.

The endpoint uses the stateless Streamable HTTP transport of MCP and keeps no session state between requests.

## Connect a Client

Claude Code:

```bash
claude mcp add --transport http basyx http://localhost:8090/mcp
```

Start `claude` and run `/mcp` to see the server and its tools.

Codex:

```bash
codex mcp add basyx --url http://localhost:8090/mcp
```

Run `codex mcp list` to check the connection.

If the endpoint requires a token, the client signs in through the browser. In Claude Code, run `/mcp`, select the server, and choose *Authenticate*. In Codex, run `codex mcp login basyx`. See [Security and Sign-In](#security-and-sign-in).

MCP clients that run in the cloud, for example custom connectors on claude.ai, connect from the internet. They need an endpoint that is publicly reachable over HTTPS.

## Tools

| Tool | API call | Annotation |
| --- | --- | --- |
| `list_shells` | `GET /shells` | read-only |
| `get_shell` | `GET /shells/{id}` | read-only |
| `list_submodels` | `GET /submodels` | read-only |
| `get_submodel` | `GET /submodels/{id}` or `GET /submodels/{id}/$value` | read-only |
| `get_submodel_element` | `GET /submodels/{id}/submodel-elements/{idShortPath}` or `.../$value` | read-only |
| `get_concept_description` | `GET /concept-descriptions/{id}` | read-only |
| `query_shells` | `POST /query/shells` | read-only |
| `query_submodels` | `POST /query/submodels` | read-only |
| `create_shell` | `POST /shells` | additive |
| `create_submodel` | `POST /submodels`, optionally followed by `POST /shells/{id}/submodel-refs` | additive |
| `add_submodel_element` | `POST /submodels/{id}/submodel-elements` or `.../submodel-elements/{idShortPath}` | additive |
| `set_submodel_element_value` | `PATCH /submodels/{id}/submodel-elements/{idShortPath}/$value` | destructive |
| `delete_shell` | `DELETE /shells/{id}` | destructive |
| `delete_submodel` | `DELETE /submodels/{id}` | destructive |
| `delete_submodel_element` | `DELETE /submodels/{id}/submodel-elements/{idShortPath}` | destructive |

The write tools, from `create_shell` downwards, are listed only with `mcp.writesEnabled=true`.

Every tool carries MCP tool annotations that mark it as read-only, additive, or destructive. MCP clients combine these annotations with their own permission settings to decide when to ask the user before a tool runs. The server adds no confirmation step of its own.

- Tools take identifiers as plain text. They encode them for the API themselves.
- `get_submodel` and `get_submodel_element` return the ValueOnly representation when `valueOnly` is set. `set_submodel_element_value` takes a value in ValueOnly representation. See [Representations](../common/representations).
- `idShortPath` uses dots between idShorts and `[index]` for list items, for example `Nameplate.Address` or `Measurements[0]`.
- `list_shells` and `list_submodels` accept `limit` and `cursor` and return `paging_metadata.cursor` for the next page, as described in [Pagination](../common/pagination). They can filter by `idShort`; `list_submodels` can also filter by `semanticId`, which matches external references whose key is the given global identifier.
- `query_shells` and `query_submodels` take a [Query Language](../common/query_language) object with a `$condition`.
- `create_submodel` with `shellId` first creates the Submodel and then adds its reference to the shell. If the reference cannot be added, the new Submodel remains and the tool result says so.

## Conditional Writes with ETags

Read and write tools return the resource's `etag`. Pass it to a change or delete tool to make the request [conditional](../common/conditional_requests):

| Tool | ETag parameter |
| --- | --- |
| `set_submodel_element_value`, `delete_shell`, `delete_submodel`, `delete_submodel_element` | `etag` of the resource |
| `add_submodel_element` | `etag` of the Submodel or of the parent element |
| `create_submodel` with `shellId` | `shellEtag` of the shell, from `get_shell` |

If the resource changed in the meantime, the tool fails with HTTP `412` and the client can read it again. With `server.conditionalRequests.requireIfMatch=true`, changes of existing resources without an `etag` fail with HTTP `428`.

## Results, Errors, and Cancellation

A read whose API response exceeds `mcp.maxResultBytes` fails with a hint to request a smaller page with `limit` and `cursor`, use `valueOnly`, or read a single Submodel Element. This keeps large Submodels from filling the agent's context. A successful change whose response exceeds the limit still reports success, with status, `etag`, and location, but without the response body.

Failed calls return a tool error with the API status, the API error message, and a hint, for example `MCP-DISPATCH-HTTP404: Not Found ... Check the identifier or idShortPath`.

When a client disconnects, the API request started by its tool call is cancelled.

## Security and Sign-In

### Without Runtime Security

With `abac.enabled=false`, the MCP endpoint, like the REST API, accepts requests without authentication. Do not expose it beyond a trusted development machine, and do not enable writes on an endpoint that others can reach.

### With Runtime Security

With `abac.enabled=true`, the endpoint requires a bearer token and follows the [MCP authorization specification](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization). Configure [Runtime Security](../common/security) as for the REST API; the MCP endpoint uses the same OIDC trustlist and access rules.

- A request without a valid token receives HTTP `401` with `WWW-Authenticate: Bearer resource_metadata="<metadata URL>"`.
- The service publishes OAuth 2.0 Protected Resource Metadata (RFC 9728). Its `resource` is the endpoint URL, and its `authorization_servers` are the issuers of the OIDC trustlist.
- Every trustlist entry must have an `audience` when the MCP endpoint is enabled; otherwise the service does not start. Tokens issued for other audiences are rejected. This keeps tokens that an identity provider issued for other applications from being used at BaSyx.

```{mermaid}
sequenceDiagram
    participant C as MCP client
    participant E as AAS Environment
    participant I as Identity provider
    C->>E: MCP request without token
    E-->>C: 401 with resource_metadata URL
    C->>E: GET protected resource metadata
    E-->>C: resource and authorization_servers
    C->>I: Register client or use configured client ID
    C->>I: Authorization code flow with PKCE in the browser
    I-->>C: Access token with the BaSyx audience
    C->>E: MCP request with bearer token
    E-->>C: Tool result with the user's permissions
```

### Reverse Proxy

The metadata URL is formed by inserting `/.well-known/oauth-protected-resource` between the host and the path of the endpoint URL. It therefore lies outside the API path prefix and must be routed to the AAS Environment as well.

For example, with `general.externalUrl=https://example.org/aas` and the default `mcp.path`:

| | URL or path |
| --- | --- |
| MCP endpoint | `https://example.org/aas/mcp` |
| Public metadata URL | `https://example.org/.well-known/oauth-protected-resource/aas/mcp` |
| Metadata path served by the AAS Environment | `/.well-known/oauth-protected-resource<server.contextPath><mcp.path>` |

If the proxy forwards `/aas` unchanged to a service with `server.contextPath=/aas`, forward the metadata path unchanged too. If the proxy strips `/aas` and the service has no context path, rewrite `/.well-known/oauth-protected-resource/aas/mcp` to `/.well-known/oauth-protected-resource/mcp`.

## Identity Provider Requirements

The endpoint works with any OpenID Connect provider that the trustlist accepts. For Claude Code, Codex, and other MCP clients to sign in, the provider must:

1. Serve its endpoints over HTTPS with a certificate that the client trusts. MCP clients do not open sign-in pages over plain HTTP, even on `localhost`.
2. Publish OAuth 2.0 Authorization Server Metadata or OpenID Connect discovery.
3. Support the authorization code flow with PKCE (`S256`).
4. Let the client obtain a client ID, in one of two ways:
   - Dynamic Client Registration (RFC 7591). Clients register themselves with a loopback redirect URI such as `http://localhost:<port>/callback`.
   - A public client registered by an administrator, with `http://localhost:<port>/callback` as redirect URI. Pass its ID to the MCP client, for example `claude mcp add --transport http --client-id <id> --callback-port <port> basyx <url>`.
5. Put the trustlist `audience` into the access tokens that it issues to these clients. MCP clients send the endpoint URL as RFC 8707 `resource` parameter, but many providers ignore it, so configure the audience in the provider.

Providers without Dynamic Client Registration, for example Microsoft Entra ID, need a registered client.

### Example: Keycloak

The secured MCP example uses Keycloak with Dynamic Client Registration. The realm needs the following adjustments:

- A client scope, for example `basyx-aas-environment`, with an audience mapper for the trustlist `audience`. Add it to the realm's default client scopes so that dynamically registered clients receive it.
- The anonymous client registration policy *Trusted Hosts* lists `localhost` and `127.0.0.1`, with *Client URIs Must Match* enabled and *Host Sending Client Registration Request Must Match* disabled. Keycloak then checks the redirect URIs of a registering client, but not the host that sends the registration request.
- The anonymous client registration policy *Allowed Client Scopes* also allows `openid`. Some clients, for example Codex, request it during registration, but it is not a Keycloak client scope and is rejected otherwise.
- Users have the realm role `offline_access`, and the `offline_access` client scope maps it. Clients such as Codex request refresh tokens with this scope, and self-registered clients receive roles only through their scopes.

Keep the other anonymous registration policies, in particular *Allowed Protocol Mapper Types* and *Allowed Client Scopes*. They prevent self-registered clients from adding protocol mappers that put arbitrary claims, which ABAC rules may evaluate, into their tokens. A realm import that defines its own client scopes or registration policies replaces Keycloak's defaults, so it must list these policies explicitly.
