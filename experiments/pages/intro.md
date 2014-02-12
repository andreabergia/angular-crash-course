We will discuss how to write modern web applications, based on the technologies called "AJAX". The core design for this class of applications is as follows:

- the server does not render templates, such as JSP or similar, but rather sends the client "raw data" via a set of REST APIs, often in form of JSON;
- the client (the webpage) performs multiple HTTP requests using `XmlHttpRequest` (AJAX requests) to the server and applies templates to render the data directly in the browser.

This approach was started by Google's GMail, the first modern AJAX application. It has many advantages over the classic "server-side-templates" model:

- the application can feel istantaneous due to multiple factors: smaller requests and response sizes, avoidance of reloading a full page, background work
- the client is often easier to develop, due to the improvements in frameworks and in the browser
- the server can focus on the data, making it much simpler to develop and test, without having to worry also about the design
- other clients (i.e. not webpages) can easily access the server
- the APIs and the data transmitted is (often) human readable and, thus, simple to debug.

In this short introduction, we'll cover how to write a modern web application using these technologies:

- [AngularJS](http://angularjs.org) 1.2 in the client
- [Java 7](http://java.com/getjava) and [Spring](http://spring.io/) 3.3 in the server.

We'll start with an introduction to the underlying technologies: REST, HTTP and JSON. Then we'll move to the core concepts in the server and client technologies. Finally, we'll develop a fully working example application.
