# CatenaXplorer

> **As a** participant in a Catena-X dataspace  
> **I want to** browse the AAS descriptors in the Digital Twin Registry (DTR) of my company or of a business partner  
> **so that** I can find digital twins by their asset IDs and inspect their Submodels.

The **CatenaXplorer** is a browser for **AAS descriptors** in a Catena-X Digital Twin Registry. It lists the descriptors, searches them by specific asset ID, shows their details and Submodel descriptors, and loads the Submodels behind them.

It works in one of two access modes, set by the selected infrastructure:

| Access mode | Source of the descriptors | What you can do |
| --- | --- | --- |
| **direct** | The DTR configured in the infrastructure (`digitalTwinRegistry`), typically your own | Browse and search descriptors; create, edit, duplicate and delete them; open Submodels in the Submodel viewer or editor |
| **edc** | The DTR of a business partner, reached through your Eclipse Dataspace Connector (EDC) and the [Catena-X EDC BFF](../catena_x_edc_bff.md) | Browse and search descriptors and load their Submodels; **read-only** |

---

## Requirements

- The selected infrastructure uses the **`catena-x`** infrastructure template.
- **direct**: the infrastructure has a **Digital Twin Registry** endpoint. To open Submodels, their endpoints must be reachable from the browser and belong to an origin the Web UI trusts for the infrastructure (an endpoint of the infrastructure or one of its `trustedOrigins`), and on desktop the standalone Submodel viewer and editor must be enabled (`SM_VIEWER_EDITOR`).
- **edc**: the infrastructure has `catenaX.accessMode: edc`, and the [Catena-X EDC BFF](../catena_x_edc_bff.md) is running. The BFF needs the DSP endpoints of the partners in `CX_EDC_ALLOWED_COUNTER_PARTY_ADDRESSES` and their data planes in `CX_EDC_ALLOWED_DATA_PLANE_ADDRESSES`. Partners must support DSP 2025-1 (Tractus-X EDC 0.11 or later).

The CatenaXplorer is available on desktop and mobile devices. On a phone it shows the list and the details on two tabs, **Browse** and **Details**.

```{note}
The CatenaXplorer only reads from the BFF, so it doesn't need management writes. These are needed only by the [Eclipse Dataspace Connector](eclipse_dataspace_connector.md) module.
```

---

## Accessing the CatenaXplorer

1. Select an infrastructure with the `catena-x` template.
2. Open the **Modules** menu in the navigation bar.
3. Select **CatenaXplorer**.

To make it the start page of a deployment, set `START_PAGE_ROUTE_NAME=CatenaXplorer`, as the [CatenaXplorer EDC Standalone example](https://github.com/eclipse-basyx/basyx-aas-web-ui/tree/main/examples/CatenaXplorerEdcStandalone) does.

---

## Choosing a Business Partner (edc)

In the **edc** access mode, the sidebar starts with the **Business partner** selection:

- **Configured partners**: the partners of the infrastructure (`catenaX.edc.partners`). The default partner (`defaultPartnerId`) is preselected.
- **Recently used**: partners entered by hand that were loaded successfully. They are remembered in this browser, per EDC proxy (at most 8).
- **Use another partner…**: enter the **Counterparty ID** (the BPN of the partner) and the **Counterparty DSP Address** (its DSP endpoint, e.g. `https://partner.example/api/v1/dsp`).

Selecting a partner sends no request and clears the results of the previous partner. Select **Load all descriptors** to start: the BFF requests the catalog of the partner, negotiates its Digital Twin Registry asset (`cx-taxo:DigitalTwinRegistry`) and queries the registry through the data plane of the partner. A status shows whether the partner is **Not loaded**, **Loading**, **Ready** or whether loading failed. **Reload all descriptors** loads them again.

The contract negotiation takes a few seconds the first time. The CatenaXplorer reuses the resulting transfer process for later requests to the same partner, so further pages, searches and Submodels load faster.

### Saving a Partner

After a partner entered by hand was loaded successfully, **Save partner** adds it to the configured partners of the infrastructure, optionally as the default partner. This needs editable infrastructures (`ENDPOINT_CONFIG_AVAILABLE=true`). Saved partners are stored in the browser; the partners for all users are set in `basyx-infra.yml`.

Partners can also be added, edited, removed and set as default in **Settings → Manage Infrastructures**, when editing the Catena-X infrastructure.

```{important}
The BFF only contacts partners whose DSP address starts with a prefix in `CX_EDC_ALLOWED_COUNTER_PARTY_ADDRESSES`. Adding a partner in the browser doesn't change this allowlist.
```

---

## Browsing and Searching Descriptors

The descriptor list shows the name, ID and, if the registry provides it, the time of the last change of each AAS descriptor. Further pages load while scrolling, or with **Load more**.

To find a digital twin by one of its **specific asset IDs**:

1. Choose the **asset ID key**, e.g. `manufacturerPartId` (the default), `manufacturerId`, `customerPartId`, `digitalTwinType`, `partInstanceId`, `intrinsicId`, `batchId` or `van`. Keys found in the loaded descriptors are suggested as well.
2. Enter the value in **Search asset ID** and start the search.
3. Clear the search to list all descriptors again.

The search uses the `assetIds` filter of the registry (`GET /shell-descriptors?assetIds=…`). In the **edc** access mode, load the descriptors of the partner before searching.

**Request as cURL** shows the request for the current search as a `curl` command to copy:

- **direct**: the request to the DTR. Credentials are replaced by a placeholder, e.g. `Bearer <ACCESS_TOKEN>`.
- **edc**: the request to the BFF, which adds the EDC credentials on the server.

The selected descriptor is kept in the URL (query parameter `descriptor`), so a link to the CatenaXplorer opens the same descriptor again.

---

## Descriptor Details

Selecting a descriptor shows its details. Switch between **Details** and **JSON**.

**Details** shows:

- the **Global Asset ID**, **Asset Kind**, **Asset Type** and **Description**,
- the **specific asset IDs**,
- the **Submodel Descriptors**, each with its **Semantic ID**, **Supplemental Semantic IDs** and **Endpoints**. The values of the supplemental semantic IDs are shown as markers next to the Submodel name.

### Loading Submodels

What happens with a Submodel descriptor depends on the access mode:

- **direct**: **Open Submodel** loads the Submodel from the `SUBMODEL-3.0` endpoint of the descriptor and opens it in the Submodel editor (if `ALLOW_EDITING` is enabled), otherwise in the Submodel viewer; on a phone in the visualization. The CatenaXplorer checks first that the endpoint returns a Submodel with the ID of the descriptor, so a wrong `href` can't make you edit another Submodel.
- **edc**: **Load Submodel** fetches the Submodel through the EDC and shows it below the descriptor, as a **Table** of its SubmodelElements or as **JSON**. **Reload Submodel** fetches it again. Submodels loaded through the EDC are read-only and can't be opened in the editor.

In the **edc** access mode, the endpoint of the Submodel descriptor needs complete DSP information: `subprotocol` `DSP` and a `subprotocolBody` with the asset ID and the DSP endpoint of the provider, e.g. `id=<asset ID>;dspEndpoint=https://provider.example/api/v1/dsp`. The BFF negotiates this asset and gets the Submodel from the `href` through the data plane of the provider.

```{tip}
To fetch other assets of a partner, or to send AAS and Submodels to a partner, use the **Catalog** of the [Eclipse Dataspace Connector](eclipse_dataspace_connector.md#catalog) module.
```

---

## Managing Descriptors (direct)

In the **direct** access mode, the CatenaXplorer edits the descriptors of the configured DTR:

- **Create descriptor** opens a form for a new AAS descriptor.
- The menu of a list item offers **Edit**, **Delete**, **Duplicate** and **Copy as JSON**.

The form has the following sections:

| Section | Fields |
| --- | --- |
| **Details** | ID, IdShort, Description |
| **Asset** | Asset Kind, Asset Type, Global Asset ID (can be generated) |
| **Specific Asset IDs** | Name, Value and External Subject Markers of each specific asset ID; values can be generated |
| **Submodel Descriptors** | ID, IdShort, Semantic ID, Supplemental Semantic IDs and **Endpoints** (Interface, Href, Protocol) of each Submodel descriptor |

**Duplicate** creates a copy right away, with new IDs for the AAS descriptor and its Submodel descriptors and `_copy` appended to their `idShort`.

**Delete** removes the AAS descriptor from the registry after a confirmation. The Submodels behind it are not deleted.

Changes use the AAS Registry API of the DTR (`POST`, `PUT` and `DELETE` on `/shell-descriptors`) with the authentication of the infrastructure.

---

## Troubleshooting

| Message or problem | Solution |
| --- | --- |
| *The selected Catena-X infrastructure has no Digital Twin Registry URL.* | Add the Digital Twin Registry endpoint to the infrastructure, or use the `edc` access mode. |
| *Enter an EDC counterparty ID and DSP address.* | Select a partner or enter both values under **Use another partner…**. |
| *Load descriptors for the selected business partner before searching.* | Select **Load all descriptors** first. |
| The DSP address of the partner is not allowed | Add its prefix to `CX_EDC_ALLOWED_COUNTER_PARTY_ADDRESSES` of the BFF. |
| `403 DATA_PLANE_ADDRESS_NOT_ALLOWED` | Add the data plane origin named in the error to `CX_EDC_ALLOWED_DATA_PLANE_ADDRESSES` of the BFF. |
| Loading fails with `400` for a partner | The partner probably doesn't support DSP 2025-1. |
| EDR polling timeout | The negotiation didn't finish in time. Check whether your EDC fulfills the policy of the partner's DTR asset; raise `CX_EDC_EDR_POLLING_ATTEMPTS` if negotiations are slow. |
| *This submodel descriptor has no complete DSP endpoint information.* | The partner has to add `subprotocol: DSP` and a `subprotocolBody` with `id` and `dspEndpoint` to the endpoint. |
| *The endpoint resolved to Submodel "…", but the descriptor identifies "…".* | The `href` of the Submodel descriptor points to another Submodel; correct the descriptor. |
| *The standalone Submodel viewer/editor is disabled in this deployment.* | Enable `SM_VIEWER_EDITOR` to open Submodels from the CatenaXplorer. |
| *Untrusted endpoint blocked.* | The Submodel endpoint is on an origin the infrastructure doesn't trust; add it to `trustedOrigins` of the infrastructure. |

More BFF errors are listed in [Error codes](../catena_x_edc_bff.md#error-codes).
