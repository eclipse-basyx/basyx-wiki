This example shows the enrichment of AAS data loaded from an aasx file with a dynamically created Submodel. Its code is available on [GitHub](https://github.com/eclipse-basyx/basyx-java-examples/tree/main/basyx.examples/src/main/java/org/eclipse/basyx/examples/scenarios/staticdynamic)


The following components are used:

* [Registry Component](../user_documentation/basyx_components/registry/index.md)
* [AAS Server Component](../user_documentation/basyx_components/aas-server/index.md)



![StaticDynamicScenario.png](./images/799px-StaticDynamicScenario.png)

In the first step an AAS-Server and a Registry-Server is started by the methodes `startAASServer()` and `startRegistry()`.

Then the AASXPackageManager is used to load example AASs/SMs from an .aasx file into a Set of AASBundle objects. 

```java
// Load Bundles from .aasx file
AASXPackageManager packageManager = new AASXPackageManager("aasx/01_Festo.aasx");
Set<AASBundle> bundles = packageManager.retrieveAASBundles();
```

A new Submodel is added to one of the bundles. The correct bundle is found by the idShort of its AAS.

```java
// Get the correct Bundle from the Set
AASBundle bundle = findBundle(bundles, AAS_ID_SHORT);
 
// Add the new SubModel to the Bundle
bundle.getSubmodels().add(sm);
```

These bundles are then uploaded to the server using the AASBundleIntegrator.

```java
// Load the new Bundles to the Server
AASBundleHelper.integrate(new AASAggregatorProxy(SERVER_URL), bundles);
```

The last step is to register the newly uploaded AAS/SM objects. This is done by a separate method `registerBundles()`. It iterates over a given Set of bundles and registers all contained AASs/SMs.

```java
// Get a RegistryProxy and register all Objects contained in the Bundles
AASRegistryProxy proxy = new AASRegistryProxy(REGISTRY_URL);
registerBundles(bundles, proxy, SERVER_URL);
```


An example of how to execute and use the scenario can be found in [TestStaticDynamicScenario](https://git.eclipse.org/r/plugins/gitiles/basyx/basyx/+/master/examples/basys.examples/src/test/java/org/eclipse/basyx/examples/scenarios/staticdynamic/).