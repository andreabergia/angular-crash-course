# REST

## Introduction

[REST](https://en.wikipedia.org/wiki/Representational_state_transfer) is an architectural paradigm for designing web applications, based on HTTP 1.1 and URLs (also known as URIs). The main design points are:

- clear separation of clients and servers
- stateless
- cacheable
- transparently layered (the client doesn't know to which specific machine it is talking)
- uniform interface, which we'll now discuss in detail.

The central principle is the concept of _resources_. A server can provide access to multiple resources via URLs. The clients and servers communicates _representations_ of the resources and access them only using the principal methods of the HTTP 1.1 standard:

- `GET`
- `POST`
- `PUT`
- `DELETE`

Resources are often represented using HTML, XML, or JSON.

## A first example

Let us suppose a server provides access to a list of users. Thus, it might expose these "api":

- `GET` on `/users`, to retrieve the list of the users
- `GET` on `/users/{id}`, to retrieve an user given its id
- `POST` on `/users`, to create a new user
- `PUT` on `/users/{id}`, to update the user with the given id
- `DELETE` on /users/{id}`, to remove an user.

Furthermore, it is common to support _subordinate_ resources, which represent resources contained under another one. For instance, the mail for an users might be thought of as a subordinate resource, and thus accessed - for instance - with a `GET` on `/users/{id}/mail`.

<hr>

## Introduction to HTTP

HTTP is a textual protocol, used - as everyone knows - to access the web, but which can be used as a general-purpose inter-application protocol. HTTP requests always have a _method_, a set of _headers_ and might have _parameters_ and a _request body_. HTTP responses always have a _status_ and might have a set of _headers_ and a _response body_. Let us now discuss the [main methods](http://www.w3.org/Protocols/rfc2616/rfc2616-sec9.html).

### Methods

#### GET

`GET` is used to retrieve a resource, given its path on the server (the last part of the URL, e.g. `/users` for `http://localhost:8080/users`). `GET` is designed to be used only for retrieval of a resource. It should be _idempotent_, meaning that it should not modify the resource on the server. It cannot have a content, but it might have parameters. A response to a `GET` request should have a body. Parameters are specified in the URL in the form `param1=value1&param2=value2&param3=value3`.

#### PUT

`PUT` is used to modify an already existing resource, or (somewhat less commonly) to create a new one. It should have a request body, unless an empty resource makes sense for the application. Its response might or might not have a body.

#### DELETE

`DELETE` is used to destory an already existing resource. It cannot have a request body. Its response might have a body, although that isn't too common.

#### POST

`POST` is used to create a new resource under an existing one, but it also commonly used as a general RPC (remote procedure call) mechanism, meaning you might allow a request on `/users/{id}/invite` to send an invite to an existing user. However, these kind of resources might be thought of, or redesigned, in terms of a "invite" resource subordinated to an "user". Its request commonly has a body, and so does its response, but neither is required. A common kind of body is `application/x-www-form-urlencoded`, from a web form.

### Statuses

All HTTP responses have a status. A status is a three-digit number, which identifies whether the request was successful or not. Status codes are grouped in families by the first digit. The most commonly used statuses are:

- `2xx` success, of which the most common are:

    * `200 OK`, which means that the request was succesful.
    * `201 Created`, which means that the resource was created. A server might return `200` instead of `201`.
    * `204 No Content`, which means that the request was succesful but the response has no body. It is often used for a `DELETE` request. A server might return `200` instead of `204`.

- `3xx` family, which are designed to handle redirect. Generally the client libraries will handle these automatically, and they are thus transparent for the end application.

- `4xx` errors, which mean errors in the requests. The most common errors in this family are:

    * `400 Bad Request`, meaning that the client has performed a malformed request.
    * `401 Unauthorized`, meaning that authentication is required and has failed, or has not yet provided.
    * `403 Forbidden`, meaning that the request is valid but the server is refusing to respond to it.
    * `404 Not Found`, meaning that the requested resource does not exist. It might also be returned in case the resource exists, but the user cannot access it, to prevent the user discovering that the resource _exists_.
    * `409 Conflict`, meaning that there was a conflict in a request, such as an edit conflict in case of multiple updates.

- `5xx` errors, which mean a valid request but a processing errors in the server. The most common error in this family is `500 Internal Server Error`, a generic error code when an error happens in the server.

### Headers

HTTP requests and responses can have headers, which are helpful to describe the content of the request or response, and can provide additional information to the server. The most common ones in the response are:

- `Cache-Control`, 'Expires', and `ETag`<C-F2>, used to control cache. Caching is a complex topic; please look up [this link](https://developers.google.com/speed/articles/caching) for further information.
- `Content-Length`, the length of the response in bytes.
- `Content-Encoding`, which specifies the compression algorithm used in the response. For instance, `Content-Encoding: gzip`.
- `Content-Disposition`, which instructs the browser to show a "save attachment" dialog. For instance, `Content-Disposition: attachment; filename="fname.ext"`.
- `Set-Cookie`, which sets a cookie in the client. The client is expected to add a `Cookie` header with the returned value in any following request. See [wikipedia](https://en.wikipedia.org/wiki/HTTP_cookie) for more details.

Some of the common ones in the request are:

- `Accept`, to specify the acceptables representations of a resource. For instance, `Accept: application/json`. The server should send the response in the requested format or return an error.
- `Accept-Encoding`, to specify an acceptable compression for a resource. The most common value is `Accept-Encoding: gzip, deflate`. It is generally handled transparently by the client and the server libraries.
- `ETag`, to handle caching.
- `Cookie`, which should contain the value returned to the server as `Set-Cookie`.

<hr>

## JSON

[JSON](https://en.wikipedia.org/wiki/JSON) is a format commonly used for encoding request and response body in HTTP requests. JSON is based on JavaScript, but it is a language-independent encoding. The valid data types are:

- _number_: in double precision, for instance `3.14`
- _string_: unicode, double-quoted, backslash escaped, for instance `"Hèlló \"Wórlð"`
- _boolean_: either `true` or `false`
- _null_
- _array_: ordered, comma separated collection of etherogeneous values, for instance `[2, true, "Hi"]`
- _objects_: unordered collection of key-values pair, for instance `{"name": "Andrea", age: 28}`

Often a JSON HTTP response will be an object, or an array, but that is not necessary. A realistic example of a response that might be returned from a server:

```json
{
    "main": {
        "temp": 4.51,
        "pressure": 999,
        "humidity": 75,
        "temp_min": 3.33,
        "temp_max": 6
    },
    "weather": {
        "main": "Clear",
        "description": "sky is clear"
    }
}
```

<hr>

## A weather example

Let us now write a full python program that will perform an HTTP request to a real web server.

```python
import httplib
import json
import sys

if len(sys.argv) == 1:
    print "Please give a city as argument"
    sys.exit(1)
city = sys.argv[1]

conn = httplib.HTTPConnection("api.openweathermap.org")
conn.request("GET", "/data/2.5/forecast/daily?mode=json&units=metric&q=" + city)
resp = conn.getresponse()

# It should print 200 OK
# print resp.status, resp.reason

data = json.load(resp)
day = 1
for forecast in data['list']:
    print "In %d days the temperature will be %d, and the wheather %s" % (day, forecast['temp']['day'], forecast['weather'][0]['description'])
    day += 1
```
