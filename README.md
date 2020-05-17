# Interlock Local Server

This software will allow you to connect the Interlock Server to access the devices on your local network in realtime communication with Websockets

### Status Codes

These are the status codes that represent the state of the system

In production, the class of the code will be represented with an LED.

##### 1000 - Setting Up Codes

| Class | Code | Name | Description |
|-------|------|------|-------------|
| SETUP | 1000  | INTERNAL_SETUP | The device is setting up |
| SETUP | 1100 | SERVICE_SETUP | The device is setting up a service |
| SETUP | 1110 | WEBSERVER_SETUP | The device is setting up a service |
| SETUP | 1200 | RUNNING_TESTS | The device is running tests |
| SETUP | 1210 | RUNNING_INET_TESTS | The device is running internet tests |
| SETUP | 1211 | RUNNING_INET_TEST | The device is running internet connection test |
| SETUP | 1212 | RUNNING_SERVER_TEST | The device is running the server connection test |


##### 2000 - Success Codes

| Class | Code | Name | Description |
|-------|------|------|-------------|
| SUCCESS | 2000  | OK | All systems are fully operational |

##### 4000 - Error Codes

| Class | Code | Name | Description |
|-------|------|------|-------------|
| ERROR | 4100  | SERVICE_ERROR | A service has encountered an error |
| ERROR | 4200  | TEST_ERROR | A test has failed |
| ERROR | 4210  | INET_TEST_ERROR | An internet test has failed |
| ERROR | 4211  | NO_INTERNET | The device has no internet |
| ERROR | 4212  | NO_SERVER | The remote server is down |

### Websocket Client

The local server will communicate with the remote server through a websocket

#### Requests

This is the basic request data structure in JSON.

```json
{
  "t": "CMD",
  "c": "device.shutdown",
  "a": {
    "timeout": 100
  }
}
```

It is in best practice to keep the request size small so when you can use abrv. 

##### Common Keys

| Key | Meaning | Type | Handler |
|:---:|:-------:|:----:|:-------:|
|`t`| Type of request | `string` | Request handler |
|`i`| Identifier | `int` | `GET` handler |
|`c`| Command | `string` | `CMD` handler |
|`a`| Arguments | `dict` of `any` | `CMD` handler |
|`m`| Message | `string` | `MSG` handler |
|`mt`| Message Type | `string` | `MSG` handler |
