# Contact Information

> **As a** BaSyx AAS Web UI user  
> **I want to** visualize Contact Information Submodels in a table view  
> **so that** I can quickly find and access contact details for manufacturers, suppliers, and support.

## Semantic ID

This plugin is activated when a Submodel has the following semantic ID:

- **V1.0**: `https://admin-shell.io/zvei/nameplate/1/0/ContactInformations`

## Feature Overview

The Contact Information plugin provides a clean, tabular visualization of contact information stored in Asset Administration Shells. It presents contact details in an organized table format, making it easy to find phone numbers, email addresses, and other contact information.

```{figure} ./images/contact_information.png
---
width: 100%
alt: Contact Information Plugin
name: contact_information_plugin
---
Contact Information Plugin
```

## Key Features

- **Table View**: All contacts displayed in a clear, sortable table
- **Multiple Contact Types**: Support for various contact roles (manufacturer, supplier, support, etc.)
- **Complete Contact Details**:
  - Names and roles
  - Phone and fax numbers
  - Email addresses
  - Physical addresses
  - Websites
  - Department information
- **Search and Filter**: Quickly find specific contacts
- **Copy to Clipboard**: Easy copying of email addresses and phone numbers

## Usage

1. Navigate to a Submodel with the Contact Information semantic ID in the AAS Treeview
2. Open the **Visualization** tab
3. The plugin displays all contact information in a table view
4. Use the search bar to filter contacts
5. Click on email addresses to open your email client
6. Click on phone numbers to initiate calls (on supported devices)
7. Click on website links to open them in a new browser tab

```{figure} ./images/contact_information_detail.png
---
width: 80%
alt: Contact Information Detail View
name: contact_information_detail
---
Detailed Contact Information View
```

## Supported Contact Information

The plugin displays the following information for each contact:

- **Contact Type**: Role or function (e.g., Technical Support, Sales, Service)
- **Company Name**: Organization name
- **Department**: Specific department or division
- **Contact Person**: Name and title
- **Street Address**: Complete postal address
- **City/Region**: Location information
- **Postal Code**: ZIP/postal code
- **Country**: Country name
- **Phone Numbers**: Multiple phone numbers with labels
- **Fax Numbers**: Fax contact information
- **Email Addresses**: Email contacts with roles
- **Website**: Company or department website URLs
- **Additional Information**: Notes or special instructions

## References

- [IDTA Contact Information V1.0 Specification](https://industrialdigitaltwin.org/wp-content/uploads/2022/10/IDTA-02002-1-0_Submodel_ContactInformation.pdf)
