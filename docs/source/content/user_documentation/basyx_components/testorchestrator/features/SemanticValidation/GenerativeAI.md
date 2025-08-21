## Semanctic Validation with Generative AI

The user can also use **Generative AI** to validate the **semantics of Property Submodel Elements**. This feature checks whether the units used for `Property` elements are semantically appropriate. If not, the AI suggests alternative units.

To enable this feature, the user must provide the following three pieces of information:

- **Model Name**: The name of the LLM model to use  
- **API Key**: The key used to authenticate requests to the LLM  
- **API Endpoint**: The URL endpoint to send semantic validation queries

All of this information must be saved in a file named `llm_config.txt` located in the `config` directory.

```{figure} ./images/llm_config.PNG
---
width: 100%
alt: LLM Config File Example
name: llm_config
---
