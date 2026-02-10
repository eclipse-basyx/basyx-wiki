# Configuration

BaSyx is configured via *Environment Variables* in the docker-compose file.

## Configuration via Environment Variables

### Server Configuration
Variable Name      | Default | Description
-------------------|---------|---------------------------------------------------------------------------------------------------------------------------
SERVER_HOST        | 0.0.0.0    | Sets the server`s <b>internal</b> Host
SERVER_PORT        | 5004    | Sets the server`s <b>internal</b> Port
SERVER_CONTEXTPATH | /       | Sets the base (context) Path of the server. If set to /myServer the server is listening to http://localhost:5004/myServer/*

### PostgreSQL Configuration
Variable Name                   | Default     | Description
--------------------------------|-------------|------------------------------------------------------------------
POSTGRES_HOST                   | db          | The <b>IP-Address</b> or <b>Hostname</b> of the PostgreSQL server
POSTGRES_PORT                   | 5432        | The Port of the PostgreSQL Server
POSTGRES_DBNAME                 | basyxTestDB | The Database to use by BaSyx
POSTGRES_USER                   | admin       | Username of the Database User
POSTGRES_PASSWORD               | admin123    | Password of the Database User
POSTGRES_MAXOPENCONNECTIONS     | 50          | Maximum Allowed open Connections
POSTGRES_MAXIDLECONNECTIONS     | 50          | Maximum Allowed Idle Connections
POSTGRES_CONNMAXLIFETIMEMINUTES | 5           | Lifetime of a single Connection in minutes

### CORS Configuration
Variable Name         | Default                                | Description
----------------------|----------------------------------------|------------
CORS_ALLOWEDORIGINS   | --                                     | A comma-separated list of allowed origins. If set to `*` all origins are allowed. (NOTE: This is important for <b>Front-End Applications</b> like the <b>BaSyx AAS Web UI</b>)
CORS_ALLOWEDMETHODS   | GET, POST, PUT, PATCH, DELETE, OPTIONS | Allowed HTTP Methods
CORS_ALLOWEDHEADERS   | --                                     | Allowed Headers
CORS_ALLOWCREDENTIALS | false                                  | Whether to allow credentials (like Cookies, Authorization Headers or TLS Client Certificates)

### ABAC Configuration (Not yet available for Registry of Infrastructures)
Variable Name                  | Default | Description
-------------------------------|----------------------------------|----
ABAC_ENABLED                   | false | Enable/Disable the ABAC Feature
ABAC_ENABLEDEBUGERRORRESPONSES | false | Enable/Disable additional Debugging Information on the console and in HTTP Responses (<b>Do not use this in production, this may leak confidential information in plain-text</b>)
ABAC_MODELPATH                 | config/access_rules/access-rules.json | (Docker Internal-) Path to the ABAC Rules.
OIDC_TRUSTLISTPATH | -- | Path to a JSON File containing trusted OIDC Issuers. See [here](https://github.com/eclipse-basyx/basyx-go-components/blob/main/cmd/aasregistryservice/config/trustlist.json)


## Configuration via Configuration File
Alternatively, BaSyx Go Components can also be configured via a Configuration File in yaml format.
To do so, create a file named `config.yaml` and mount it to the Container Path /config/config.yaml.

Here is an example configuration file providing all possible configuration options:

```yaml
server:
    host: 0.0.0.0
    port: 5004
    contextPath: /

postgres:
    host: db
    port: 5432
    dbname: basyxTestDB
    user: admin
    password: admin123
    maxOpenConnections: 50
    maxIdleConnections: 50
    connMaxLifetimeMinutes: 5

cors:
    allowedOrigins: "*"
    allowedMethods:
        - GET
        - POST
        - PUT
        - PATCH
        - DELETE
        - OPTIONS
    allowedHeaders: "*"
    allowCredentials: false

abac:
    enabled: false
    enableDebugErrorResponses: false
    modelPath: config/access_rules/access-rules.json

oidc:
    trustListPath: ""
```