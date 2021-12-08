# /path1/path2
```HTTP
GET /path1/path2
```

## Summary
Get a `path2` resource
## Description
Given an identifier, return a `path2` resrouce, if found. <br /> There are four possible results:
  * result 1 → something
  * result2:
    * something else → do something different
    * something else but quite similar to the previous case → do something different again
  * anything else → do whatever you want

---
## Request
### Parameters
| Parameter | Description | Type | Required | Example |
| ------------ | ------------------------------------ | ------ | -------- | ----------------- |
|resourcename|The name of the resource to retrieve|string|Yes|12345a6789b01234c|

## Responses
### 302
This service goes anywhere.<br /> Available URLs are:
  * Success request - https://{host}/success
  * Almost success - https://{host}/success-1
  * Almost success, case 2- https://{host}/success-2
  * Error - https://{host}/error-page

#### Headers
| Header | Description | Type | Example |
| -------- | ----------------------- | ------ | ---------------------- |
|Location|The page to redirect to|string|https://{host}/success|
