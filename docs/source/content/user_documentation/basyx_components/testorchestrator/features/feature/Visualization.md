# Results Visualization

## Viewing Results

- Through the **BaSyx Submodel Repository API**
- Via the **BaSyx Web UI**, where categorized results are displayed
- As downloadable JSON files for further processing

```{figure} ./images/filteredResults.PNG
---
width: 100%
alt: filteredResults
name: filteredResults
---
```

---
All Validation results are persisted in dedicated Submodels:

- **TestResults** - for successful validations
- **UnsuccessfulTestResults** - for failed or incomplete validations
---

## Result Structure

Each result contains:

```json
{
  "ComparedSubmodelId": "...",
  "SemanticId": "...",
  "Errors": "...",
  "Warnings": "...",
  "Differences": "...",
  "Infos": "..."
}
```

## Result Categories
The results are divided into 4 different categories:

- **Errors**: This category contains all the errors that must be corrected for ensuring conformity of the submodels. This category contains the following:
  - When elements with Multiplicity `One` or `One to Many` are absent then they are present here.
  - Including elements not defined in the standardized template for a given submodel results is an error since users are not permitted to introduce arbitrary elements into predefined submodels. Thus these errors are also listed here. 
  **Exception**: Time Series and Technical Data.
- **Warnings**: This part includes the optional elements that are expected in the standardized submodels but are not added by the user. 
  - The optional elements are those elements that have Multiplicity `Zero to One` or `Zero to Many`. 
  - The use of spaces in Semantic IDs and ID Shorts is considered a poor practice, as it can lead to inconsistencies and interpretation issues. Therefore, if any spaces are detected in these fields, then that is added as a warning.
- **Differences**: The Id Short Mismatch for the same Semantic ID is recorded in this part of the result. Moreover, the value type mismatch is also displayed in this part. 
- **Infos**: This part contains all the results of the Property type Submodel Elements. 
  - When a Submodel Element has a value type mismatch or the added value does not conform to the value type, the results are added in this part. 
  - The unit mismatch of the elements is also recorded here. 
  - After querying ECLASS for a specific IRDI of a property, the ID short and preferred name mismatches are also logged in this part. 
  - The semantic validation of units by AI and the suggested units are also reported in this part.    

## Test Orchestrator Module

The Test Orchestrator uses the [Basyx AAS Web UI Module](https://github.com/eclipse-basyx/basyx-aas-web-ui/tree/main/aas-web-ui/src/pages/modules) for displaying the validation results in user-friendly manner. Navigate to the `Test Orchestrator` module to:

- View all test results and statistics.
- See the suggestions for improving the submodel. 


```{figure} ./images/Test_Orchestrator_Module.jpeg
---
width: 100%
alt: Test Orchestrator Module
name: Test_Orchestrator_Module
---
```
The validation results can be downloaded:
- For individual submodels.
- For all tested submodels as a single JSON file.

The user interface allows users to filter results by specific submodels, helping focus only on relevant data. Additionally, hovering over individual validation issues provides contextual suggestions to help resolve the problem, thereby guiding users toward improving their submodels.

```{figure} ./images/WebUI_suggestion.png
---
width: 100%
alt: Visualization of Module
name: WebUI_suggestion
---
```
