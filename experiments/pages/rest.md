[TOC]

## Introduction

[REST](https://en.wikipedia.org/wiki/Representational_state_transfer) is an architectural paradigm for designing web applications, based on HTTP 1.1 and URLs (also known as URIs).

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

### Authentication and statelessness

REST prescribes "statelessness" as one of the main points. However, for a lot of applications, it is much simpler to keep some state in the server - for instance, the current user session. This is much simpler to program, but it also hurts scalability, beecause the session must be shared between the various servers. The most common way to do this is by using cookies: the server will associate a session in its memory to a session token, sent to the client as a cookie. This is the approach natively follower by some server technologies, such as Java's servlets.

The other option is to avoid keeping state in the server. To do this and implement authentication, HTTP supports various mechanisms. Unfortunately none of these is both secure _and_ easy to use. Most websites (such as Twitter or Google) use one of these mechanism for their REST APIs, most commonly [HTTP Basic Auth](https://en.wikipedia.org/wiki/Basic_access_authentication).

<hr>

## JSON

[JSON](https://en.wikipedia.org/wiki/JSON) is a format commonly used for encoding request and response body in HTTP requests. JSON is based on JavaScript, but it is a language-independent encoding. The valid data types are:

- _number_: in double precision, for instance `3.14`
- _string_: unicode, double-quoted, backslash escaped, for instance `"Hèlló \"Wórlð"`
- _boolean_: either `true` or `false`
- _null_
- _array_: ordered, comma separated collection of etherogeneous values, for instance `[2, true, "Hi"]`
- _objects_: unordered collection of key-values pair, for instance `{"name": "Andrea", age: 28}`

JSON got a lot of momentum in the last few years because of its simplicity, the fact that it is human-readable, the ease of implementation of a parser, and its expressiveness. It is also far more compact than XML, which has started to replace.

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

## An example client

Let us now write a full python program that will perform an HTTP request to a real web server. The service we'll use is [OpenWeatherMap.org](http://openweathermap.org), which exposes a free REST API for weather forecast. A `GET` request on the url [http://api.openweathermap.org/data/2.5/forecast/daily?mode=json&units=metric&q=CITY](http://api.openweathermap.org/data/2.5/forecast/daily?mode=json&units=metric&q=CITY) will return a JSON object representing the weather forecast for the given CITY. With this in mind, we can write our little program:

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

Let us look at what has gone on the wire. The request was something like:

```http
GET /data/2.5/forecast/daily?mode=json&units=metric&q=CITY HTTP/1.1
Host: api.openweathermap.org
Connection: keep-alive
Cache-Control: no-cache
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
Pragma: no-cache
Accept-Encoding: gzip,deflate,sdch
```

While the response might have been:

```http
HTTP/1.1 200 OK
Access-Control-Allow-Credentials:true
Access-Control-Allow-Methods:GET, POST
Access-Control-Allow-Origin:*
Connection:keep-alive
Content-Type:application/json; charset=utf-8
Date:Wed, 12 Feb 2014 19:53:39 GMT
Server:nginx
Transfer-Encoding:chunked

{"cod":"200","message":0.0269,"city":{"id":"6691831","name":"","coord":{"lon":12.458,"lat":41.9024},"country":"Vatican City","population":0},"cnt":7,"list":[{"dt":1392202800,"temp":{"day":9.35,"min":7.63,"max":9.35,"night":7.63,"eve":9.35,"morn":9.35},"pressure":1014.66,"humidity":100,"weather":[{"id":802,"main":"Clouds","description":"scattered clouds","icon":"03n"}],"speed":3.88,"deg":340,"clouds":32},{"dt":1392289200,"temp":{"day":11.57,"min":5.92,"max":12.14,"night":12.14,"eve":10.86,"morn":5.92},"pressure":1018.03,"humidity":100,"weather":[{"id":500,"main":"Rain","description":"light rain","icon":"10d"}],"speed":4.81,"deg":201,"clouds":56,"rain":3},{"dt":1392375600,"temp":{"day":13.65,"min":8.12,"max":13.76,"night":8.12,"eve":11.01,"morn":11.12},"pressure":1017.05,"humidity":89,"weather":[{"id":800,"main":"Clear","description":"sky is clear","icon":"01d"}],"speed":7.06,"deg":332,"clouds":0},{"dt":1392462000,"temp":{"day":13.59,"min":6.48,"max":13.86,"night":12.08,"eve":12.46,"morn":6.48},"pressure":1021.8,"humidity":96,"weather":[{"id":800,"main":"Clear","description":"sky is clear","icon":"02d"}],"speed":3.97,"deg":135,"clouds":8},{"dt":1392548400,"temp":{"day":14.41,"min":12.19,"max":14.61,"night":13.47,"eve":14.33,"morn":12.19},"pressure":1018.54,"humidity":89,"weather":[{"id":500,"main":"Rain","description":"light rain","icon":"10d"}],"speed":10.56,"deg":157,"clouds":92,"rain":0.5},{"dt":1392634800,"temp":{"day":14.18,"min":11.49,"max":14.18,"night":11.49,"eve":11.89,"morn":11.88},"pressure":1021.54,"humidity":92,"weather":[{"id":800,"main":"Clear","description":"sky is clear","icon":"01d"}],"speed":3.56,"deg":223,"clouds":0},{"dt":1392721200,"temp":{"day":13.54,"min":11.67,"max":13.54,"night":12.2,"eve":12.57,"morn":11.67},"pressure":1011.41,"humidity":0,"weather":[{"id":500,"main":"Rain","description":"light rain","icon":"10d"}],"speed":8.1,"deg":224,"clouds":50,"rain":1.2}]}
```

This concludes our introduction to REST apis, HTTP and JSON.
