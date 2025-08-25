[Back: Results Visualization](../results_visualization.md) | [Back to Overview](../index.md)

# Extending Validation

## Adding New Schemas

To validate against additional standards or templates, place your JSON schema files in the `/schema/` directory of the Test Orchestrator project.  
If you want to use external schemas, update the schema links in the `getPredefinedLinks()` method in the code.  
Any schema with a matching `SemanticId` will be automatically considered during validation.

---

## Extending Validation Rules

You can modify or extend the validation logic by editing the `SMEComparator` and `RecursionFunc` classes in the source code.  
For example, to add new qualifier types, custom multiplicity rules, or domain-specific checks, add your logic to these utility classes.

---

## Listening to Custom Event Topics

If you need to process additional submodel events (beyond creation, update, or deletion), you can edit the `subscribeToMqtt()` method in the `MqttSubscriber` class.  
Add your MQTT topics there to enable automated validation for your specific workflow.

---

## Example Workflow: Custom Validation

1. Add your new schema to the `/schema/` folder.
2. Edit the validation logic in `SMEComparator` or `RecursionFunc` to introduce your new rules.
3. (Optional) Update the MQTT subscriber to listen for additional events.
4. Upload a submodel as usual—the orchestrator will validate it against your custom logic and schemas.
5. View the test results in the `TestResults` submodel via the repository API.

---

[Back: Results Visualization](../results_visualization.md) | [Next: MongoDB Integration](mongodbintegration.md)