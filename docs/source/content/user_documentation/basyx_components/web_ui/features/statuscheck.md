# Status Checks and Error Notifications

## User Story and Use Case

>As AAS Web UI user
>I want to see if the Asset Administration Shells registered in the AAS Registry are available.
>I also want to know if an error occurred during the use of the AAS Web UI and what caused the error.

The UI provides a feature to periodically check the status of the Asset Administration Shells registered in the AAS Registry. The status of the Asset Administration Shells is displayed in the AAS List in the left panel of the application. If an error occurs during the use of the AAS Web UI, the user is informed about the error and the cause of the error.

## Feature Overview

```{figure} ./images/aas_status.png
---
figclass: margin
alt: AAS Status Indicator
name: aas_status
---
AAS Status Indicator
```

### Status Checks

If an Asset Administration Shell or a Submodel is not available, the user is informed about the issue through a status indicator in the AAS List on the left side of the application. The indicator can automatically appear/disappear when the periodic status check discovers a change in the status of the Asset Administration Shells or Submodels. The user can also manually trigger the status check by clicking on the refresh button in the AAS List. The periodical check is performed every 60 seconds.

```{figure} ./images/disable_statuschecks.png
---
figclass: margin
alt: Disable Status Checks
name: disable_statuschecks
---
Disable Status Checks
```

```{tip}
You are also able to deactivate the status checks under the **AUTO SYNC** menu in the top right corner of the application.
```

### Error Notifications

If an error occurs during the use of the AAS Web UI, the user is informed about the error and the error message is displayed in a red snackbar at the top of the application. The snackbar will dissapear after 60 seconds or if the user clicks on the close button. The snackbar will also display network errors.

If there is an error description provided by the server, it will also be displayed in the snackbar under the error message.

```{figure} ./images/error_message.png
---
width: 100%
alt: Error Notifications
name: error_message
---
```
