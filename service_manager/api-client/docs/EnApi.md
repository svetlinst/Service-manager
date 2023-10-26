# ServiceManagerApi.EnApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**enApiServiceOrdersCreate**](EnApi.md#enApiServiceOrdersCreate) | **POST** /en/api/service_orders/ | 
[**enApiServiceOrdersDestroy**](EnApi.md#enApiServiceOrdersDestroy) | **DELETE** /en/api/service_orders/{id}/ | 
[**enApiServiceOrdersList**](EnApi.md#enApiServiceOrdersList) | **GET** /en/api/service_orders/ | 
[**enApiServiceOrdersPartialUpdate**](EnApi.md#enApiServiceOrdersPartialUpdate) | **PATCH** /en/api/service_orders/{id}/ | 
[**enApiServiceOrdersRetrieve**](EnApi.md#enApiServiceOrdersRetrieve) | **GET** /en/api/service_orders/{id}/ | 
[**enApiServiceOrdersUpdate**](EnApi.md#enApiServiceOrdersUpdate) | **PUT** /en/api/service_orders/{id}/ | 



## enApiServiceOrdersCreate

> ServiceOrderHeader enApiServiceOrdersCreate(serviceOrderHeader)



### Example

```javascript
import ServiceManagerApi from 'service_manager_api';
let defaultClient = ServiceManagerApi.ApiClient.instance;
// Configure API key authorization: cookieAuth
let cookieAuth = defaultClient.authentications['cookieAuth'];
cookieAuth.apiKey = 'YOUR API KEY';
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//cookieAuth.apiKeyPrefix = 'Token';

let apiInstance = new ServiceManagerApi.EnApi();
let serviceOrderHeader = new ServiceManagerApi.ServiceOrderHeader(); // ServiceOrderHeader | 
apiInstance.enApiServiceOrdersCreate(serviceOrderHeader, (error, data, response) => {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully. Returned data: ' + data);
  }
});
```

### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **serviceOrderHeader** | [**ServiceOrderHeader**](ServiceOrderHeader.md)|  | 

### Return type

[**ServiceOrderHeader**](ServiceOrderHeader.md)

### Authorization

[cookieAuth](../README.md#cookieAuth)

### HTTP request headers

- **Content-Type**: application/json, application/x-www-form-urlencoded, multipart/form-data
- **Accept**: application/json


## enApiServiceOrdersDestroy

> enApiServiceOrdersDestroy(id)



### Example

```javascript
import ServiceManagerApi from 'service_manager_api';
let defaultClient = ServiceManagerApi.ApiClient.instance;
// Configure API key authorization: cookieAuth
let cookieAuth = defaultClient.authentications['cookieAuth'];
cookieAuth.apiKey = 'YOUR API KEY';
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//cookieAuth.apiKeyPrefix = 'Token';

let apiInstance = new ServiceManagerApi.EnApi();
let id = 56; // Number | A unique integer value identifying this service order header.
apiInstance.enApiServiceOrdersDestroy(id, (error, data, response) => {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully.');
  }
});
```

### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **Number**| A unique integer value identifying this service order header. | 

### Return type

null (empty response body)

### Authorization

[cookieAuth](../README.md#cookieAuth)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: Not defined


## enApiServiceOrdersList

> [ServiceOrderHeader] enApiServiceOrdersList()



### Example

```javascript
import ServiceManagerApi from 'service_manager_api';
let defaultClient = ServiceManagerApi.ApiClient.instance;
// Configure API key authorization: cookieAuth
let cookieAuth = defaultClient.authentications['cookieAuth'];
cookieAuth.apiKey = 'YOUR API KEY';
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//cookieAuth.apiKeyPrefix = 'Token';

let apiInstance = new ServiceManagerApi.EnApi();
apiInstance.enApiServiceOrdersList((error, data, response) => {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully. Returned data: ' + data);
  }
});
```

### Parameters

This endpoint does not need any parameter.

### Return type

[**[ServiceOrderHeader]**](ServiceOrderHeader.md)

### Authorization

[cookieAuth](../README.md#cookieAuth)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json


## enApiServiceOrdersPartialUpdate

> ServiceOrderHeader enApiServiceOrdersPartialUpdate(id, opts)



### Example

```javascript
import ServiceManagerApi from 'service_manager_api';
let defaultClient = ServiceManagerApi.ApiClient.instance;
// Configure API key authorization: cookieAuth
let cookieAuth = defaultClient.authentications['cookieAuth'];
cookieAuth.apiKey = 'YOUR API KEY';
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//cookieAuth.apiKeyPrefix = 'Token';

let apiInstance = new ServiceManagerApi.EnApi();
let id = 56; // Number | A unique integer value identifying this service order header.
let opts = {
  'patchedServiceOrderHeader': new ServiceManagerApi.PatchedServiceOrderHeader() // PatchedServiceOrderHeader | 
};
apiInstance.enApiServiceOrdersPartialUpdate(id, opts, (error, data, response) => {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully. Returned data: ' + data);
  }
});
```

### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **Number**| A unique integer value identifying this service order header. | 
 **patchedServiceOrderHeader** | [**PatchedServiceOrderHeader**](PatchedServiceOrderHeader.md)|  | [optional] 

### Return type

[**ServiceOrderHeader**](ServiceOrderHeader.md)

### Authorization

[cookieAuth](../README.md#cookieAuth)

### HTTP request headers

- **Content-Type**: application/json, application/x-www-form-urlencoded, multipart/form-data
- **Accept**: application/json


## enApiServiceOrdersRetrieve

> ServiceOrderHeader enApiServiceOrdersRetrieve(id)



### Example

```javascript
import ServiceManagerApi from 'service_manager_api';
let defaultClient = ServiceManagerApi.ApiClient.instance;
// Configure API key authorization: cookieAuth
let cookieAuth = defaultClient.authentications['cookieAuth'];
cookieAuth.apiKey = 'YOUR API KEY';
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//cookieAuth.apiKeyPrefix = 'Token';

let apiInstance = new ServiceManagerApi.EnApi();
let id = 56; // Number | A unique integer value identifying this service order header.
apiInstance.enApiServiceOrdersRetrieve(id, (error, data, response) => {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully. Returned data: ' + data);
  }
});
```

### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **Number**| A unique integer value identifying this service order header. | 

### Return type

[**ServiceOrderHeader**](ServiceOrderHeader.md)

### Authorization

[cookieAuth](../README.md#cookieAuth)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json


## enApiServiceOrdersUpdate

> ServiceOrderHeader enApiServiceOrdersUpdate(id, serviceOrderHeader)



### Example

```javascript
import ServiceManagerApi from 'service_manager_api';
let defaultClient = ServiceManagerApi.ApiClient.instance;
// Configure API key authorization: cookieAuth
let cookieAuth = defaultClient.authentications['cookieAuth'];
cookieAuth.apiKey = 'YOUR API KEY';
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//cookieAuth.apiKeyPrefix = 'Token';

let apiInstance = new ServiceManagerApi.EnApi();
let id = 56; // Number | A unique integer value identifying this service order header.
let serviceOrderHeader = new ServiceManagerApi.ServiceOrderHeader(); // ServiceOrderHeader | 
apiInstance.enApiServiceOrdersUpdate(id, serviceOrderHeader, (error, data, response) => {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully. Returned data: ' + data);
  }
});
```

### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **Number**| A unique integer value identifying this service order header. | 
 **serviceOrderHeader** | [**ServiceOrderHeader**](ServiceOrderHeader.md)|  | 

### Return type

[**ServiceOrderHeader**](ServiceOrderHeader.md)

### Authorization

[cookieAuth](../README.md#cookieAuth)

### HTTP request headers

- **Content-Type**: application/json, application/x-www-form-urlencoded, multipart/form-data
- **Accept**: application/json

