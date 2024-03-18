# Environment Variables
Instead of using .properties file to configure the BaSyx components such as aas-server, registry etc., a user can also use environment variable for configuration. All parameters which are defined in the BaSyx[Context, Docker, MongoDB, ...]Configuration.java in this package **basyx.components.lib/src/main/java/org/eclipse/basyx/components/configuration/** . There are general rules when using environment variables:

* Once environment variables are set, then the settings in the .properties file will be overwritten.
* When using environment variables, it is not allowed to use "." in your parameters (such as basyx_aas.server) and DO NOT mix upper and lower case letters(such as BaSyx_aas_server).
* Always put the prefix of this component configuration at the begin of an environment variable and write it in lower case.
The tables below show how to configure BaSyx components using environment variables. The first column is the variable names which are defined as Strings in BaSyx*Configuration.java files. The second column show how to write them as environment variables. Third column shows an example.

## BaSyxContextConfiguration.java
When configuring a BaSyx HTTP server using BaSyx context, always put the prefix "basyxcontext_" at begin of an environment variable.

| Configuration using Environment variables 	|                                    	|                                             	|
|:-----------------------------------------:	|:----------------------------------:	|:-------------------------------------------:	|
|               Variable name               	| Written as an environment variable 	|                   Example                   	|
| contextPath                               	| basyxcontext_contextpath           	| basyxcontext_contextpath=basys.sdk          	|
| contextDocPath                            	| basyxcontext_contextdocpath        	| basyxcontext_contextdocpath=java.io.tempdir 	|
| contextHostname                           	| basyxcontext_contexthostname       	| basyxcontext_contexthostname=localhost      	|
| contextPort                               	| basyxcontext_contextport           	| basyxcontext_contextport=4000               	|

## BaSyxDockerConfiguration.java
When configuring a BaSyx Docker container, always put the prefix "basyxdocker_" at begin of an environment variable.

| Configuration using Environment variables 	|                                    	|                                             	|
|:-----------------------------------------:	|:----------------------------------:	|:-------------------------------------------:	|
|               Variable name               	| Written as an environment variable 	|                   Example                   	|
| BASYX_HOST_PORT                           	| basyxdocker_basyx_host_port        	| basyxdocker_basyx_host_port=4000            	|
| BASYX_CONTAINER_PORT                      	| basyxdocker_basyx_container_port   	| basyxdocker_basyx_container_port=4000       	|
| BASYX_IMAGE_NAME                          	| basyxdocker_basyx_image_name       	| basyxdocker_basyx_image_name=aasserver      	|
| BASYX_CONTAINER_NAME                      	| basyxdocker_basyx_container_name   	| basyxdocker_basyx_container_name=aas-server 	|

## BaSyxMongoDBConfiguration.java
When configuring BaSyx application using Mongo DB backend, always put the prefix "basyxmongodb_" at begin of an environment variable.

| Configuration using Environment variables 	|                                    	|                                                            	|
|:-----------------------------------------:	|:----------------------------------:	|:----------------------------------------------------------:	|
|               Variable name               	| Written as an environment variable 	|                           Example                          	|
| dbname                                    	| basyxmongodb_dbname                	| basyxmongodb_dbname=admin                                  	|
| dbconnectionstring                        	| basyxmongodb_dbconnectionstring    	| basyxmongodb_dbconnectionstring=mongodb://127.0.0.1:27017/ 	|
| dbcollectionRegistry                      	| basyxmongodb_dbcollectioregistry   	| basyxmongodb_dbcollectioregistry=basyxregistry             	|
| dbcollectionAAS                           	| basyxmongodb_dbcollectionaas       	| basyxmongodb_dbcollectionaas=basyxaas                      	|
| dbcollectionSubmodels                     	| basyxmongodb_dbcollectionsubmodels 	| basyxmongodb_dbcollectionsubmodels=basyxsubmodel           	|

## BaSyxMqttConfiguration.java
When configuring BaSyx MQTT, always put the prefix "basyxmqtt_" at begin of an environment variable.

| Configuration using Environment variables 	|                                    	|                                         	|
|:-----------------------------------------:	|:----------------------------------:	|:---------------------------------------:	|
|               Variable name               	| Written as an environment variable 	|                 Example                 	|
| user                                      	| basyxmqtt_user                     	| basyxmqtt_user=                         	|
| pass                                      	| basyxmqtt_pass                     	| basyxmqtt_pass=                         	|
| server                                    	| basyxmqtt_server                   	| basyxmqtt_server=http://localhost:1883/ 	|
| qos                                       	| basyxmqtt_qos                      	| basyxmqtt_qos=1                         	|

## BaSyxSQLConfiguration.java
When configuring BaSyx SQL, always put the prefix "basyxsql_" at begin of an environment variable.

| Configuration using Environment variables 	|                                    	|                                             	|
|:-----------------------------------------:	|:----------------------------------:	|:-------------------------------------------:	|
|               Variable name               	| Written as an environment variable 	|                   Example                   	|
| dbuser                                    	| basyxsql_dbuser                    	| basyxsql_dbuser=postgres                    	|
| dbpass                                    	| basyxsql_dbpass                    	| basyxsql_dbpass=admin                       	|
| dburl                                     	| basyxsql_dburl                     	| basyxsql_dburl=//localhost/basyx-directory? 	|
| sqlDriver                                 	| basyxsql_sqldriver                 	| basyxsql_sqldriver=org.postgresql.Driver    	|
| sqlPrefix                                 	| basyxsql_sqlprefix                 	| basyxsql_sqlprefix=jdbc:postgresql:         	|

## BaSyxSecurityConfiguration.java
When configuring BaSyx application using the authorization feature backend, always put the prefix "basyxsecurity_" at begin of an environment variable.

|                          Configuration using Environment variables                          |                                                                                                           |
|:-------------------------------------------------------------------------------------------:|:---------------------------------------------------------------------------------------------------------:|
|                                        Variable name                                        |                                     Written as an environment variable                                    |
| authorization.strategy                                                                      | basyxsecurity_authorization_strategy                                                                      |
| authorization.strategy.jwtBearerTokenAuthenticationConfigurationProvider                    | basyxsecurity_authorization_strategy_jwtbearertokenauthenticationconfigurationprovider                    |
| authorization.strategy.jwtBearerTokenAuthenticationConfigurationProvider.keycloak.serverUrl | basyxsecurity_authorization_strategy_jwtbearertokenauthenticationconfigurationprovider_keycloak_serverurl |
| authorization.strategy.jwtBearerTokenAuthenticationConfigurationProvider.keycloak.realm     | basyxsecurity_authorization_strategy_jwtbearertokenauthenticationconfigurationprovider_keycloak_realm     |
| authorization.strategy.jwtBearerTokenAuthenticationConfigurationProvider.audience           | basyxsecurity_authorization_strategy_jwtbearertokenauthenticationconfigurationprovider_audience           |
| authorization.strategy.simpleRbac.rulesFilePath                                             | basyxsecurity_authorization_strategy_simplerbac_rulesfilepath                                             |
| authorization.strategy.simpleRbac.subjectInformationProvider                                | basyxsecurity_authorization_strategy_simplerbac_subjectinformationprovider                                |
| authorization.strategy.simpleRbac.roleAuthenticator                                         | basyxsecurity_authorization_strategy_simplerbac_roleauthenticator                                         |
| authorization.strategy.grantedAuthority.subjectInformationProvider                          | basyxsecurity_authorization_strategy_grantedauthority_subjectinformationprovider                          |
| authorization.strategy.grantedAuthority.grantedAuthorityAuthenticator                       | basyxsecurity_authorization_strategy_grantedauthority_grantedauthorityauthenticator                       |
| authorization.strategy.custom.authorizersProvider                                           | basyxsecurity_authorization_strategy_custom_authorizersprovider                                           |
| authorization.strategy.custom.subjectInformationProvider                                    | basyxsecurity_authorization_strategy_custom_subjectinformationprovider                                    |

|                                                                                                    Example                                                                                                    |
|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------:|
| basyxsecurity_authorization_strategy=SimpleRbac                                                                                                                                                               |
| basyxsecurity_authorization_strategy_jwtbearertokenauthenticationconfigurationprovider=org.eclipse.basyx.components.security.authorization.internal.KeycloakJwtBearerTokenAuthenticationConfigurationProvider |
| basyxsecurity_authorization_strategy_jwtbearertokenauthenticationconfigurationprovider_keycloak_serverurl=http://localhost:9005                                                                               |
| basyxsecurity_authorization_strategy_jwtbearertokenauthenticationconfigurationprovider_keycloak_realm=basyx-demo                                                                                              |
| basyxsecurity_authorization_strategy_jwtbearertokenauthenticationconfigurationprovider_audience=aas-server                                                                                                    |
| basyxsecurity_authorization_strategy_simplerbac_rulesfilepath=/rbac_rules.json                                                                                                                                |
| basyxsecurity_authorization_strategy_simplerbac_subjectinformationprovider=org.eclipse.basyx.extensions.shared.authorization.internal.JWTAuthenticationContextProvider                                        |
| basyxsecurity_authorization_strategy_simplerbac_roleauthenticator=org.eclipse.basyx.extensions.shared.authorization.internal.KeycloakRoleAuthenticator                                                        |
| basyxsecurity_authorization_strategy_grantedauthority_subjectinformationprovider=org.eclipse.basyx.extensions.shared.authorization.internal.AuthenticationContextProvider                                     |
| basyxsecurity_authorization_strategy_grantedauthority_grantedauthorityauthenticator=org.eclipse.basyx.extensions.shared.authorization.internal.AuthenticationGrantedAuthorityAuthenticator                    |

## Configuring OTS Component BaSyx AAS Server
When configuring the OTS component BaSyx AAS-Server with environment variables, always put the prefix "basyxaas_" at begin.

| Configuration using Environment variables |                                    |                                                                                                                          |
|:-----------------------------------------:|:----------------------------------:|:------------------------------------------------------------------------------------------------------------------------:|
|               Variable name               | Written as an environment variable |                                                          Example                                                         |
| registry.path                             | basyxaas_registry_path             | basyxaas_registry_path=                                                                                                  |
| aas.externalurl                           | basyxaas_aas_externalurl           | basyxaas_aas_externalurl=http://192.168.178.33:4000                                                                      |
| aas.backend                               | basyxaas_aas_backend               | basyxaas_aas_backend=InMemory                                                                                            |
| aas.source                                | basyxaas_aas_source                | basyxaas_aas_source=                                                                                                     |
| aas.events                                | basyxaas_aas_events                | basyxaas_aas_events=NONE                                                                                                 |
| tokenEndpoint                             | basyxaas_tokenEndpoint             | basyxaas_tokenEndpoint=http://127.0.0.1:9006/auth/realms/basyx-demo/protocol/openid-connect/token                        |
| clientId                                  | basyxaas_clientId                  | basyxaas_clientId=basyx-demo                                                                                             |
| clientSecret                              | basyxaas_clientSecret              | basyxaas_clientSecret=SomeKindOfSecret                                                                                   |
| clientScopes                              | basyxaas_clientScopes              | basyxaas_clientScopes=["urn:org.eclipse.basyx:scope:aas-registry:read","urn:org.eclipse.basyx:scope:aas-registry:write"] |


## Configuring OTS Component BaSyx AAS Registry
When configuring the OTS component BaSyx AAS Registry with environment variables, always put the prefix "basyxregistry_" at begin.

| Configuration using Environment variables |                                    |                                         |
|:-----------------------------------------:|:----------------------------------:|:---------------------------------------:|
|               Variable name               | Written as an environment variable |                 Example                 |
| registry.backend                          | basyxregistry_registry_backend     | basyxregistry_registry_backend=InMemory |