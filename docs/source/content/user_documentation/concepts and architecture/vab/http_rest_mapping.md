# HTTP Mapping

The following table illustrates the mapping of VAB communication operations to HTTP REST communication that was used in this example. Short values, e.g. the path to the element and an operation ID are transmitted in the header, while complex objects, e.g. parameters are transmitted in the HTTP body, which has no size limitation.


| VAB operation   | HTTP/REST mapping                 |
|-----------------|-----------------------------------|
| retrieve(e,p)   | HTTP-GET e/p                      |
| update(e,p,v)   | HTTP-PUT e/p [body: v as JSON]    |
| create(e,n,v)   | HTTP-POST e/n [body: v as JSON]   |
| delete(e,p)     | HTTP-DELETE e/p                   |
| invoke(e,p,par) | HTTP-POST e/p [body: par as JSON] |
