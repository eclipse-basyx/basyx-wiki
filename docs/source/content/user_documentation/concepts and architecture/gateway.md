# BaSyx VAB Gateway

Gateways realize the translation part of the end-to-end communication of the Virtual Automation Bus. By transparently translating the five semantic primitives from a native communication technology to another native technology, they are completely invisible to sender and receiver of messages.

For example, a *GET* primitive send over the BaSyx-TCP implementation can seamlessly be translated to HTTP-REST. The response to the *GET* primitive is handled in the same way. 

![Gateway communication](./images/BaSyx_Gateway_Communication.png)

It is possible to cascade an arbitrary number of gateways. Since the gateways utilize the same access functionalities of the VAB as a client, it is also for gateways transparent if they directly address the data provider or another gateway.

In the current [implementation](../implementation/gateway.md), gateways do not contain any further access logic since the path used for gateway access contains all necessary information for further processing, e.g. http://gw1//basyx://10.0.0.1:2332.