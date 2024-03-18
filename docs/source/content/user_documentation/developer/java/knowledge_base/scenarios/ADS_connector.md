# ADS Connector{Reading from and writing to PLCs with ADS interface using BaSyx}

## Introduction
The key to successful brown-field applications of Asset Administration Shells is compatibility with already installed assets. Many of the machine tools, robots, or production lines in use today offer interfaces, which can be used to integrate them into the higher-level control structures (like SCADA or MES systems if we consider the classical automation pyramid). When considering brown-filed applications of Asset Administration Shells, adapters can be used to create a holistic environment of asset administration shells agnostic of the underlying assets interfaces. One of the most recent interfaces available for a wide variety of vendors and equipment is OPC-UA. OPC-UA is generally not available for equipment produced before 2016. If we consider the average lifetime of industrial equipment of more than 20 years, it becomes clear that in many brown-field applications OPC-UA will not be an option. Thus, there is a need to develop further adapters.

BaSyx, as a reference implementation of the Asset Administration Shell, already supports OPC-UA through a so-called OPC-UA Connector. The Connector elements in BaSyx are used to implement the Adapter Pattern. In the following, a simple implementation of a BaSyx Connector is shown for the ADS interface. ADS (Automation Device Specification) is an interface mainly used in the products of Beckhoff Company. The Beckhoff automation software TwinCat includes a PLC (Programmable Logic Controller) for general purpose applications or motion controllers and an NC (Numerical Controller) for controlling motion axes or machine tools. TwinCat enables controlling of industrial hardware on a Windows-OS (Operating System) by extending the OS with a realtime driver. Thus, SPS, NC and HMI (Human-Machine Interface) can be accessed simultaneously by the same off-the-shelf hardware. ADS is fundamentally different from BaSyx due to the fact that the ADS Server interacts with industrial control systems that have and use strict rules for arranging their internal memory. ADS in its essence interacts with memory tables. Thus, access to process-data is enabled by ADS in TwinCat.


## The ADS Connector
ADS has a TCP-IP-based implementation and an official client library with Java bindings from Beckhoff. This library will be used to demonstrate how to create an ADS Connector for BaSyx. The library is available free of charge. An alternative open-source library is also available, but it does not have official Java bindings. The goal of this Connector is to translate ADS Read and ADS Write commands to AAS-specific get or set property commands, as presented in the figure below.

![ADSComm Sequence.png](./images/ADSComm_Sequence.png)

In BaSyx, connectors are meant to provide a way to access variables on different devices in order to build AAS Submodels with these variables. Connectors, by design, have to implement the `IModelProvider` interface. This way an `AdsConnector` type object will act as an AAS submodel for the ADS device.

A class implementing the `IModelProvider` interface has to implement the following methods:

```java

    public Object getValue(String path) throws ProviderException;
    public void setValue(String path, Object newValue) throws ProviderException;
    public void createValue(String path, Object newEntity) throws ProviderException;
    public void deleteValue(String path) throws ProviderException;
    public void deleteValue(String path, Object obj) throws ProviderException;
    public Object invokeOperation(String path, Object... parameter) throws ProviderException;
```

Only the first two methods `getValue` and `setValue` will be implemented in the following. The ADS interface allows the creation and deletion of variables on the target device, but this is not a common use-case of ADS devices in a brown-field application. As it is expected that the brown-field ADS device has a running application program which controls a production line or a machine tool, it can be assumed that the logic of this application program does reference new variables, possibly created with the ADS client and cannot cope with the deletion of variables which are referenced in the application program.

As this implementation of ADS is TCP-IP based, it requires a connection from the ADS Client (in this case the AAS Server) to the ADS Server and the connection must be closed after use. On the ADS Server side, things are more complicated than a simple TCP-IP server. The ADS Server acts as a message router between all the ADS devices connected to the ADS server on the device side (not on the TCP-IP Client side). To keep the description concise, many details of the ADS communication will be omitted. A detailed description can be found [here](https://infosys.beckhoff.com/english.php?content=../content/1033/tc3_ads_intro/index.html&id=). The ADS client implementation used in this description is the Beckhoff JAVA ADS Client library, available freely [here](https://infosys.beckhoff.com/english.php?content=../content/1033/tc3_ads_dlljava/127935371.html&id=2547073384998468561). It is important to note, that the current implementation of the Beckhoff Java ADS Library, used in this example, is installed together with the Beckhoff TwinCAT control system (on any x86/x64 system) due to its internal dependencies. For other languages (e.g. C#) ADS libraries are available from Beckhoff on the well known package managers (e.g. Nuget) and are not dependent on Beckhoff TwinCAT. A tutorial an installing a free trial version of the Beckhoff TwinCAt Control System can be found [here](https://infosys.beckhoff.com/english.php?content=../content/1033/tc3_installation/6162675979.html&id=1794155022845493209). Alternatively the [PLC4X](https://plc4x.apache.org) Java ADS Client can be used instead of the Beckhoff ADS Client, which has no internal dependencies to the Beckhoff TwinCAT Control System.

The connectivity information is not typical for an IP application. It is based on a so called AMSNetId. Although the AMSNetID, 6 bytes in length, is purely logical and has no relation to the IP Address, in practice, the first 4 bytes of the AMSNetID corresponds to the IPv4 address of the device.

```
    String address = "127.0.0.1.1.1";
```

This is unusual for IP communications, but this is the way the ADS client awaits a connection string. Furthermore a port has to be specified. Some AMS Port numbers are pre-assigned (e.g. the ams port of a PLC Runtime) and some are dynamically assigned by the message router (e.g. an HMI system)

```
	int port = 852;
```

The AMS port 852 is pre-assigned a PLC Runtime system, see the complete list [here](https://infosys.beckhoff.com/english.php?content=../content/1033/tc3_ads_intro/18014398625641867.html&id=3801185565839764443). It is worth noting that the TCP/UDP ports used are 48898, 48899 and 8016.

This is the connectivity address passed to the `AdsConnector` via its constructor. To adhere to BaSyx best practices an `ADSConnectorProvider` class has been implemented, which extends the BaSyx `ConnectionProvider` class.
```java

    import org.eclipse.basyx.vab.modelprovider.api.IModelProvider;
    import org.eclipse.basyx.vab.protocol.api.ConnectorProvider;
 
    public class AdsConnectorProvider extends ConnectorProvider {
 
	    @Override
	    protected IModelProvider createProvider(String addr) {
 
		    return new AdsConnector(addr.split(":")[0], Integer.parseInt(addr.split(":")[1]));
	    }
 
    }
```

The `createProvider()` method of the `AdsConnectorProvider` should be called with only one string parameter as per BaSyx convention, therefore, the AmsNetID and the AmsPort od an ADS device should be joint with : as follows:

```java
    IModelProvider mp = new AdsConnectionProvider().createProvider("128.0.0.1.1.1:852");
```

As it can be also seen in the code snippet above, the `AdsConnector` implements the `IModelProvider<code> interface`.

The `<code>getValue(String path)` method of the `IModelProvider` interface retrieves the value of the property defined in the `path` string. Retrieving values can be done using the `AdsSyncReadReq()` method of the ADSClient library. There is a difference in how ADS and how BaSyx treats symbols. An ADS client reads addresses on the ADS server and BaSyx uses symbolic names instead of addresses. ADS provides features to look-up the address of a symbolic name. As BaSyx uses the `/` character to indicate a hierarchy of namespaces and ADS uses the `.` character for this, it is useful to replace these characters (as ADS symbols cannot contain the character `/`).

```java
    @Override
	public String getValue(String path) throws ProviderException {
		String adspath = path.replace('/', '.');
		return adsReadValueByName(adspath);
    }
```

There are multiple ways to retrieve a value of a symbol in ADS. The `AdsConnector` first retrieves the variable declaration information of the symbolic variable. This includes type information and also the address at which the value of the symbol can be found. Furthermore, as the ADS client reads a byte array from an address space, it is necessary to convert the byte array to a Java type. As the return value of `getValue(String path)` method of the `IModelProvider` is formally an object, but it is in practice implemented as a `String` in other `IModelProviders`, the Java type is then converted to a string before it is returned.
```java

    import de.beckhoff.jni.tcads.AdsSymbolEntry;
 
    ...
 
 	private String adsReadValueByName(String Name){
                AdsCallDllFunction.adsPortOpen();
 
		AdsSymbolEntry sym = adsReadDeclarationByName(Name);
		byte[] val = adsReadValueByAdsSymEntry(sym);
		String str = AdsTypeToString.get(sym.getDataType()).apply(val);
 
                AdsCallDllFunction.adsPortClose();
               return str;
	}
```

Please note that for this prototype implementation we have chosen to open and close the ADS Port before and after the read command. For a production ready version this might not be suitable.

The ADS Client library provides a domain object for storing the variable declaration related information. This domain object can be populated as follows
```java

    import de.beckhoff.jni.Convert;
    import de.beckhoff.jni.JNIByteBuffer;
 
    import de.beckhoff.jni.tcads.AdsCallDllFunction;
    import de.beckhoff.jni.tcads.AmsAddr;
    import de.beckhoff.jni.tcads.AdsSymbolEntry;
 
    ...
 
    private AdsSymbolEntry adsReadDeclarationByName(String Name){
            JNIByteBuffer readBuff = new JNIByteBuffer(0xFFFF);
	    JNIByteBuffer writeBuff =  new JNIByteBuffer(Convert.StringToByteArr(Name,true));
 
  	    // Get variable declaration
	    long err = AdsCallDllFunction.adsSyncReadWriteReq(
	    		 	  addr,
	                  AdsCallDllFunction.ADSIGRP_SYM_INFOBYNAMEEX,
	                  0,
	                  readBuff.getUsedBytesCount(),
	                  readBuff,
	                  writeBuff.getUsedBytesCount(),
	                  writeBuff);
	    if(err!=0) {
	        	throw new ProviderException("Error: Read by handle: 0x" + Long.toHexString(err));
	    }
	    AdsSymbolEntry adsSymbolEntry =
	             new AdsSymbolEntry(readBuff.getByteArray());
 
	     return adsSymbolEntry;
	}
```

The `AdsSymbolEntry` object is then used to read the value of the symbol in the `adsReadValueByAdsSymEntry(AdsSymbolEntry adsSymbolEntry)` function.
```java

    private byte[] adsReadValueByAdsSymEntry(AdsSymbolEntry adsSymbolEntry)
	{
		JNIByteBuffer buffer = new JNIByteBuffer(
                adsSymbolEntry.getSize());
 
		long err = AdsCallDllFunction.adsSyncReadReq(addr,
                                                             adsSymbolEntry.getiGroup(),
                                                             adsSymbolEntry.getiOffs(),
                                                             adsSymbolEntry.getSize(),
                                                             buffer);
 
		if(err!=0) {
        	    throw new ProviderException("Error: Read by handle: 0x" + Long.toHexString(err));
                }
 
		return  buffer.getByteArray();
	}
```

At this point, the value of the variable is retrieved, but its format is not convenient, it is stored in a byte array. As a next step the byte array is converted to a Java type and then, that Java type is converted to a string. The type information is encoded in the `AdsSymbolEntry` object. The tye information is available using the `AdsSymbolEntry.getDataType()` method, which returns an integer, which encodes the data type information as follows:
```java

    private static final int ADST_VOID = 0;
    private static final int ADST_INT8 = 16;
    private static final int ADST_UINT8 = 17;
    private static final int ADST_INT16 = 2;
    private static final int ADST_UINT16 = 18;
    private static final int ADST_INT32 = 3;
    private static final int ADST_UINT32 = 19;
    private static final int ADST_INT64 = 20;
    private static final int ADST_UINT64 = 21;
    private static final int ADST_REAL32 = 4;
    private static final int ADST_REAL64 = 5;
    private static final int ADST_STRING = 30;
    private static final int ADST_WSTRING = 31;
    private static final int ADST_REAL80 = 32;
    private static final int ADST_BIT = 33;
    private static final int ADST_BIGTYPE = 65;
    private static final int ADST_MAXTYPES = 67;
```

The `AdsConnector` class defines a `Map<Integer, Function<byte[], String>> AdsTypeToString` to facilitate the conversion of the byte array to a Java type. The simplest is to convert the String type, as this Java type does not require a further conversion to a String.
```java

    Function<byte[], String> AdsStringToString = (args) -> {
		return new String(args);
	};
 
	AdsTypeToString.put(ADST_STRING, AdsStringToString);
```

Similarly type conversion of a UINT_32 can be implemented as

```java

    Function<byte[], String> AdsUInt32ToString = (args) -> {
        ByteBuffer bb = ByteBuffer.allocate(0);
        bb = ByteBuffer.wrap(args);
        bb.order(ByteOrder.LITTLE_ENDIAN);
        Integer i = bb.getInt();
	return String.valueOf(i);
    };
 
    AdsTypeToString.put(ADST_UINT32, AdsUInt32ToString);
```

Setting a property value in an `IModelProvider` is implemented in the `setValue(String path, Object newValue)` method. Similarly to the `getValue()` case, the `/` character is exchanged for the `.` character to conform ADS naming conventions.
```java

	@Override
	public void setValueValue(String path, Object newValue) throws ProviderException {
		String adsPath = path.replace('/', '.');
		adsWriteValueByName(adsPath, newValue);
	}
```

The logic of the `adsWriteValueByName()` follows closely the logic of the `adsReadValueByName()` method presented above.
```java

	private void adsWriteValueByName(String Name, Object newValue){
                AdsCallDllFunction.adsPortOpen();
		AdsSymbolEntry sym = adsReadDeclarationByName(Name);
		byte[] newBytes = StringToAdsType.get(sym.getDataType()).apply(newValue);
		adsWriteValueByAdsSymEntry(sym, newBytes);
		AdsCallDllFunction.adsPortClose();
	}
```

The variable declarations of the symbolic variable name (path) are retrieved from the ADS server. This has two reasons. First, it contains the address, where the variable is located and, second, it contains the ADS type information of the ADS variable. The type information can be used to correctly convert the variable to the required byte array representation.

```java

	private Map<Integer, Function<Object, byte[]>> objectToAdsType = new HashMap<>();
```

For instance, the AAS interface might not be able to differentiate between an integer and an unsigned integer type. This conversion is the opposite of the type conversion for the read instruction. It is however implemented using the same construct. A map is used to store the relation between the integer encoded type information and the `Function<Object, byte[]>`. In the example below the conversion from a byte array, representing the ADS String type to the Java String type is shown. As expected, this is the simplest conversion among the data types.
```java

	Function<byte[], String> AdsStringToString = (args) -> {
			return new String(args);
	};
 
	objectToAdsType.put(ADST_STRING, StringToAdsString);
```

After obtaining the byte array representation, writing to the ADS Server is done using:
```java

	private void adsWriteValueByAdsSymEntry(AdsSymbolEntry adsSymbolEntry, byte[] newVal){
		JNIByteBuffer buffer = new JNIByteBuffer(adsSymbolEntry.getSize());
 
		buffer.setByteArray(newVal, true);
 
		long err = AdsCallDllFunction.adsSyncWriteReq(addr,
                                                              adsSymbolEntry.getiGroup(),
                                                              adsSymbolEntry.getiOffs(),
                                                              adsSymbolEntry.getSize(),
                                                              buffer);
		if (err!=0) {
        	    throw new ProviderException("Error: Read by handle: 0x" + Long.toHexString(err));
                }
	}
```

This simplistic implementation of an ADS Connector is not suitable for high load applications and should be further improved by a concurrent implementation and a queue structure for the read and write operations.


## Authors
Akos Csiszar and Florian Schellroth (ISW University of Stuttgart)