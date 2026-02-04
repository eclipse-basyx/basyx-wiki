# Contact Information

> **As a** BaSyx AAS Web UI user  
> **I want to** visualize Contact Information Submodels in a table view  
> **so that** I can quickly find and access contact details for manufacturers, suppliers, and support.

## Semantic ID

This plugin is activated when a Submodel has the following semantic ID:

- **V1.0**: `https://admin-shell.io/zvei/nameplate/1/0/ContactInformations`

## Feature Overview

The Contact Information plugin provides a structured visualization of contact information stored in Asset Administration Shells. It presents multiple contacts in expandable panels, with the first contact automatically opened for quick access. Each contact's details are organized clearly, making it easy to find phone numbers, email addresses, and other contact information.

```{figure} ./images/contact_information.png
---
width: 100%
alt: Contact Information Plugin
name: contact_information_plugin
---
Contact Information Plugin
```

## Key Features

- **Expansion Panel View**: Each contact displayed in a collapsible panel for organized navigation
- **Multiple Contacts Support**: Visualize multiple contacts per Submodel with automatic expansion of the first contact
- **vCard Download**: Export contact information as a vCard file for easy import into contact management systems and address books
- **Multiple Contact Types**: Support for various contact roles (administrative, technical, commercial, etc.)
- **Complete Contact Details**:
  - Company and department information
  - Contact person names and titles
  - Phone and fax numbers with availability times
  - Email addresses
  - Physical addresses and postal information
  - Websites and IP communication channels
  - Language and timezone information
- **Direct Communication**: Click on email addresses and phone numbers to initiate communication

## Usage

1. Navigate to a Submodel with the Contact Information semantic ID in the AAS Treeview
2. Open the **Visualization** tab
3. The plugin displays all contacts in expandable panels, with the first contact automatically opened
4. Click on panel headers to expand or collapse individual contacts
5. Use the vCard download button to export contact information for import into your address book
6. Click on email addresses to open your email client
7. Click on phone numbers to initiate calls (on supported devices)
8. Click on website links to open them in a new browser tab

## Supported Contact Information

The plugin displays the following information for each contact based on the ZVEI Nameplate specification:

### Basic Information

- **Role of Contact Person**: Type of contact (administrative, technical, commercial, hazardous goods, etc.)
- **Company**: Organization name
- **Department**: Specific department or division
- **Language**: Supported languages (ISO 639-1)
- **Time Zone**: Operating timezone (ISO 8601)

### Contact Person Details

- **Name of Contact**: Full name
- **First Name**: Given name
- **Middle Names**: Additional names
- **Title**: Professional title
- **Academic Title**: Academic degree or title

### Address Information

- **Street**: Street address
- **City/Town**: City or town name
- **Zipcode**: Postal code
- **State/County**: State or county
- **National Code**: Country code (ISO 3166-1)
- **PO Box**: Post office box number
- **Zipcode of PO Box**: Postal code for PO box

### Communication Channels

- **Phone**: Telephone number with type (office, mobile, home) and available times
- **Fax**: Fax number with type
- **Email**: Email address with type and optional public key for encryption
- **IP Communication**: Website URLs, type of communication, and available times
- **Additional Link**: Additional web addresses

### Additional Details

- **Further Details of Contact**: Additional notes or instructions
- **Available Time**: Operating hours and availability schedule

## References

- [IDTA Contact Information V1.0 Specification](https://industrialdigitaltwin.org/wp-content/uploads/2022/10/IDTA-02002-1-0_Submodel_ContactInformation.pdf)
