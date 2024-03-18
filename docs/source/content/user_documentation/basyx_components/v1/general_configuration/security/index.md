# Security(HTTPS)
By default, the AAS server component uses plain *Hypertext Transfer Protocol* (HTTP) to communicate with clients. HTTP is unprotected against network attacks, which allows an adversary to read and manipulate any communication to and from the AAS server. However, the AAS server also supports the secure variant of HTTP named [HTTPS](./https.md). In the linked subpage, you can find more information about HTTPS, and how to set it up and configure it with V1 Java BaSyx OTS components and the Java SDK.

## Access Control
Overview By default, all clients can access all data within the main [BaSyx OTS components](../index.md). In the Java SDK of BaSyx V1, there exist multiple options for defining access restrictions on specific clients. There are mainly two strategies. Additionally, it is possible to implement, configure and load a custom implementation for access control. See also more [details](../security/authorization.md) about these strategies.

* GrantedAuthoriy: Configure read/write access for clients
* SimpleRbac: Configure individual roles and detailed rules for accessing e.g. individual submodel elements
The implementation for this access control is based on [OAuth2](https://oauth.net/2/) with [Json Web Tokens (JWT)](https://jwt.io/introduction) as access tokens and has been tested with [KeyCloak](https://www.keycloak.org), an open-source software that provides, together with lots of additional functionality, the server for authenticating the clients.

![Overview over Access Control Setup with default BaSyx V1 Java SDK implementation](./images/BaSyx.Security.Overview.png)

In principle, a client authenticates at the authentication server and gets a JWT in return (1). This token is signed by the token provider and contains information the AASServer or AASRegistry can use to authorize client requests in the future. The information inside the JWT includes e.g. the client id, an expiration date and in case of the SimpleRbac strategy the role(s) of the user. By validating the JWT, the AASServer or AASRegistry authorize client requests (2). Currently, the client implementation in the Java BaSyx SDK can only use client credentials to authenticate at the authentication server.

## Setup
In order to run your own setup, you need to configure a KeyCloak server instance, the used OTS components and then use authenticated clients that access the OTS component with a valid token. A full example with introductions on how to run it can be found in the [example repository](https://github.com/eclipse-basyx/basyx-java-examples/tree/main/basyx.examples/src/main/java/org/eclipse/basyx/examples/scenarios/authorization/combined).

For the authentication server, KeyCloak needs to be configured and started. General instructions on how to do this can be found [here](../../../scenarios/authorization.md) and in its extensive [documentation](https://www.keycloak.org/docs/latest/server_admin/#configuring-authentication_server_administration_guide). Depending on the component and the strategy, there is a different configuration at the BaSyx component for the [AASServer](../aas-server/features/authorization.md) or the [Registry](../registry/features/authorization.md). In addition, there is a detailed overview over the two main [authorization strategies](../security/authorization.md).


```{toctree}
:maxdepth: 1

authorization
https
```