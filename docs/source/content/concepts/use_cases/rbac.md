# Access Control

In industrial environments and data spaces, securing access to Digital Twins and their data is paramount. Role-Based Access Control (RBAC) provides a systematic approach to managing permissions, ensuring that users and systems can only access the information and operations they are authorized for. This is particularly crucial when dealing with sensitive industrial data, intellectual property, or when multiple organizations collaborate in a shared data space.

BaSyx implements comprehensive RBAC capabilities that integrate seamlessly with industry-standard identity providers like Keycloak. This allows organizations to define fine-grained access policies for Asset Administration Shells, Submodels, and their properties, while maintaining compatibility with existing enterprise security infrastructure.

The BaSyx ecosystem supports both static RBAC rules defined at deployment time and dynamic RBAC management, where access policies can be modified at runtime through dedicated management interfaces. This flexibility is essential for modern industrial scenarios where collaboration patterns and access requirements may evolve during the lifecycle of Digital Twins.

```{note}
Two comprehensive examples demonstrating different RBAC scenarios are available in the <a href="https://github.com/eclipse-basyx/basyx-java-server-sdk/tree/main/examples/" target="_blank">Examples on GitHub</a>:
- <a href="https://github.com/eclipse-basyx/basyx-java-server-sdk/tree/main/examples/BaSyxSecured" target="_blank">BaSyx Secured Setup</a>
- <a href="https://github.com/eclipse-basyx/basyx-java-server-sdk/tree/main/examples/BaSyxDynamicRBAC" target="_blank">BaSyx Dynamic RBAC Management</a>

Feel free to try them out yourself!
```

## RBAC Architecture in BaSyx

The following diagram illustrates how role-based access control is implemented across the BaSyx ecosystem:

```{uml} charts/rbac_architecture.puml
```

### Authentication and Authorization Flow

The sequence diagram below shows the detailed process of how users authenticate and gain access to protected resources:

```{uml} charts/rbac_sequence.puml
```

## Key RBAC Features in BaSyx

### Static RBAC Configuration

- **Pre-defined Roles**: Configure user roles and permissions at deployment time
- **Component-level Security**: Secure individual BaSyx components (AAS Repository, Submodel Registry, etc.)
- **Fine-grained Permissions**: Control access to specific AAS instances, Submodels, or properties
- **Integration with Enterprise Identity**: Seamless integration with existing LDAP, Active Directory, or OAuth providers

### Dynamic RBAC Management

- **Runtime Policy Updates**: Modify access rules without system restarts
- **Submodel-based Rule Storage**: Store RBAC rules as Submodel elements for standardized management
- **Collaborative Access Control**: Enable suppliers and partners to grant access to their Digital Twins
- **Audit Trail**: Track all permission changes and access attempts

### Security Scope Coverage

- **AAS Repository**: Control access to Asset Administration Shells
- **Submodel Repository**: Manage permissions for individual Submodels
- **Registry Services**: Secure discovery and lookup operations
- **AAS Environment**: Comprehensive protection for complete AAS environments
- **File Upload/Download**: Control AASX file operations and content access

## Industrial Use Cases

### Supply Chain Collaboration

In complex supply chains, suppliers need to share specific information about their components while protecting intellectual property. BaSyx RBAC enables:

- **Selective Data Sharing**: Grant access only to relevant properties and Submodels
- **Temporary Access**: Provide time-limited access for specific projects
- **Role-based Visibility**: Different access levels for engineers, quality inspectors, and managers
- **Dynamic Permission Grants**: Suppliers can grant access when delivering components

### Multi-tenant Manufacturing Platforms

Manufacturing platforms serving multiple customers require strict data isolation:

- **Tenant Isolation**: Ensure customers can only access their own Digital Twins
- **Service Provider Access**: Allow platform operators to maintain systems while protecting customer data
- **Cross-tenant Collaboration**: Enable controlled sharing for joint projects
- **Compliance Reporting**: Generate audit reports for regulatory requirements

## RBAC Rule Structure

BaSyx uses JSON-based RBAC rules that define the relationship between roles, actions, and target resources:

### Basic Rule Example

```json
{
  "role": "engineer",
  "action": "READ",
  "targetInformation": {
    "@type": "aas",
    "aasIds": ["urn:example:manufacturing:line1"]
  }
}
```

### Advanced Rule with Multiple Actions

```json
{
  "role": "quality_inspector",
  "action": ["READ", "EXECUTE"],
  "targetInformation": {
    "@type": "submodel",
    "aasIds": "*",
    "submodelIds": ["urn:example:quality:inspection"]
  }
}
```

## Getting Started with BaSyx Security

### 1. Basic Secured Setup

Start with the foundational security example that demonstrates:

- Keycloak integration and user management
- Basic role definitions and assignments
- Secure access to AAS Web UI
- File upload with specific permissions

### 2. Dynamic RBAC Management

Explore advanced scenarios including:

- Runtime policy management through Submodel interfaces
- Cross-organizational access control
- Dynamic permission granting in supply chain scenarios
- Audit and compliance tracking

```{include} /_external/basyx-java-server-sdk/examples/BaSyxSecured/README.md
:relative-docs: /_external/basyx-java-server-sdk/examples/BaSyxSecured
:relative-images:
```

## Advanced Topics

### Custom Authentication Providers

- Integration patterns for enterprise identity systems
- Custom JWT token validation
- Multi-factor authentication support

### Performance Considerations

- Caching strategies for permission lookups
- Scalability patterns for large-scale deployments
- Monitoring and metrics for security operations

### Compliance and Auditing

- GDPR compliance considerations
- Audit log management and retention
- Regulatory reporting capabilities

```{include} /_external/basyx-java-server-sdk/examples/BaSyxDynamicRBAC/README.md
:relative-docs: /_external/basyx-java-server-sdk/examples/BaSyxDynamicRBAC
:relative-images:
```

## Additional Resources

For more information about access control and security in BaSyx:

- [BaSyx Components Security Documentation](../../user_documentation/basyx_components/index.md)
- [AAS Repository Authorization](../../user_documentation/basyx_components/v2/aas_repository/features/authorization.md)
- [Submodel Service Authorization](../../user_documentation/basyx_components/v2/submodel_service/features/authorization.md)
- [AAS Environment Authorization](../../user_documentation/basyx_components/v2/aas_environment/features/authorization.md)
- [Security Best Practices](../../user_documentation/concepts%20and%20architecture/security.md)

