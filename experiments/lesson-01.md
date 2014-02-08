[TOC]

# Lesson 1: Getting started

## What is AngularJS?

[AngularJS](http://angularjs.org) is an amazingly productive javascript web framework. It's extremely productive, designed for testability and embeddable in other applications. In a sense, AngularJS extends HTML. We'll soon see how.
[http://angularjs.org](http://angularjs.org)


## Bindings

```html
<input type="text" ng-model="name">
Hello, {{name}}
```

- ng-model is an attribute defined by AngularJS.
- It roughly means: bind this textbox's value to the variable called "name".
- <code>{{expression}}</code> tells AngularJS to evaluate expression and display its value. In this case, the value of the variable "name" is displayed.
- As you type, the value of the variable is kept in sync with the content of the text field. As soon as the variable is updated, the block {{name}} is updated.
- In MVC terminology, ng-model and the expressions allow you to use HTML element as a view.
- Furthermore, this binding is two-way, as you can see in the next example.

```html
<input type="text" ng-model="name"><br>
<input type="text" ng-model="name"><br>
Hello, {{name}}!
```

- We now have two inputs bound to the same variable: as you update one, the other gets updated as well.
- This happens, as we mentioned before, because the binding is two-way: as you update the variable, the DOM elements bound to it get updated and viceversa.


## Controllers and scope

```html
<script>
    function Test1Ctrl($scope) {
        $scope.name = 'Andrea';
    }
</script>

<div class="live-example-content">
    <div ng-controller="Test1Ctrl">
        Hello, {{name}}!
    </div>
</div>
```

- A controller is a javascript function, whose name by convention ends with Ctrl or Controller.
- The <code>$scope</code> is a special Angular object, that is used as glue between the controller (the javascript) and the view (the html).
- Variables set on the <code>$scope</code> are available to the view.
- We can use <code>ng-controller</code> on a node to specify the controller to use for the children of the given node.

```html
<script>
function Test2Ctrl($scope) {
    $scope.name = 'Andrea';
}

function Test3Ctrl($scope) {
    $scope.age = 28;
}
</script>

<div ng-controller="Test2Ctrl">
    <div ng-controller="Test3Ctrl">
        Hello, {{name}} - you are {{age}} old!
    </div>
</div>
```

- Controllers can be nested. Elements in the children controller can access properties set on the parent controller.

## Directives

```html
<script>
function Test4Ctrl($scope) {
    $scope.cities = ['Rome', 'Paris', 'Berlin'];
}
</script>

<div ng-controller="Test4Ctrl">
    <p ng-repeat="city in cities">
        {{city}} is a nice place!
    </p>
</div>
```
                    
- As you can see by the example above, <code>ng-repeat</code> will iterate in an array and replicate the node it is attached to, for each element of the array. <code>ng-repeat</code> can be applied to any html tag.
- <code>ng-repeat</code> can be applied to any html tag.
- Directives are the method used by Angular to extend html.
- <code>ng-model</code>, <code>ng-repeat</code> are examples of builtin directives
It is possible, and extremely useful, to define your own directives; however that will be covered later on, as it requires a good knowledge of Angular.

```html
<script>
function Test5Ctrl($scope) {
    $scope.age = 28;
}
</script>

<div ng-controller="Test5Ctrl">
    <p ng-show="age >= 18">
        You can vote.
    </p>
    <p ng-show="age < 18">
        Sorry kid, come back in a while.
    </p>
</div>
```

- Another extremely useful directive is <code>ng-show</code>: the node to which it is applyed will be invisible if the expression is not true.
- You can also use <code>ng-hide</code> to make your code clearer.
- We'll see some more useful directives later on.

## Filters

```html
<script>
function Test6Ctrl($scope) {
    $scope.now = new Date(2013, 01, 22);
    $scope.price = 42.67;
    $scope.name = 'Picard';
}
</script>

<div ng-controller="Test6Ctrl">
    Today is {{now | date}}. The captain is {{name | lowercase}}, 
    yelled as {{name | uppercase}}. The price is {{price | number:1}}.
</div>
```

- Filters are applied in the general form <code>{{expression | filter}}</code>.
- Filters are simply javascript functions that transform the given input.
- Angular defines a few useful filters, like <code>date</code>, <code>lowercase</code>, <code>uppercase</code>, and <code>number</code>.
- Filters can take parameters: in the example we have passed 1 as parameter to <code>number</code>, using the syntax <code>number:1</code>. This tells the number filter to display the result using one decimal.

```html
<script>
function Test7Ctrl($scope) {
    $scope.items = ['France', 'Italy', 'Germany'];
}
</script>

<div ng-controller="Test7Ctrl">
    <span ng-repeat="item in items | filter:'e'">{​{item}}. </span>
</div>
```

- We have now applied the special filter <code>filter</code>. It is a filter that, when applied to an array, returns only the items that match the given parameter (in this case, 'e'). Therefore, "Italy" was excluded.
- And now for a cool example...

```html
<script>
function Test8Ctrl($scope) {
    $scope.items = ['France', 'Italy', 'Germany', 'Austria', 'Japan'];
}
</script>
<div ng-controller="Test8Ctrl">
    <input type="text" ng-model="query">
    <br>
    <ul>
        <li ng-repeat="item in items | filter:query">{​{item}}</li>
    </ul>
</div>
```

- By combining <code>ng-model</code> on an input box and </code>filter</code>, we can build a list with a quick-search.

## Responding to clicks

```html
<script>
function Test9Ctrl($scope) {
    $scope.items = ['One', 'Two', 'Three'];
    $scope.add = function() {
        $scope.items.push($scope.newItem);
    }
}
</script>
<div ng-controller="Test9Ctrl">
    <input type="text" ng-model="newItem">
    <button ng-click="add()">Add</button>
</div>
<br>
<ul>
    <li ng-repeat="item in items">{​{item}}</li>
</ul>
```

- We have now defined, in the <code>$scope</code>, a function called <code>add</code>.
- The function can access <code>newItem</code> from the <code>$scope</code>. Its value is automatically updated by Angular, as we discussed when we talked about two-way binding.
- We have also used the <code>ng-click</code> directive to have the function invoked when the button is clicked.
- Note: whatever function we want to attach to an <code>ng-click</code>, must be exposed to the <code>$scope</code>.

## Talking to servers

```html
<script>
function Test10Ctrl($scope, $http) {
    $scope.getWeather = function() {
        $http.get('http://api.openweathermap.org/data/2.5/weather', {params: {
units: 'metric',
q: $scope.city
}
}).then(function(response) {
    $scope.weather = response.data;
    });
}
}
</script>
<div ng-controller="Test10Ctrl">
City: <input type="text" ng-model="city">
<button ng-click="getWeather()">Search</button><br>
<p ng-show="weather">Temperature: {​{weather.main.temp}}°C,
    humidity: {​{weather.main.humidity}}%.</p>
    <p ng-hide="weather">Please enter a city name and press "Search".</p>
    </div>
```

- We are now ready to start talking to servers. In this case, we'll use the excellent and free Open Weather Map service.
- This server accepts a query to an url of the form [http://api.openweathermap.org/data/2.5/weather?units=metric&q=Turin](http://api.openweathermap.org/data/2.5/weather?units=metric&q=Turin), and will return a json object representing the current weather for Turin. (Open the URL now to see it.)
- In our controller we defined a function <code>getWeather</code> to invoke this service. We use the Angular builtin service <code>$http</code> to perform an HTTP request and manipulate the json result.
- We'll discuss later what services are and how they work.
- Note how we use the second argument of <code>$http.get</code> to pass the parameters to the HTTP request.
- Since we perform an asynchronous ajax request, we cannot simply do <code>$scope.weather = $http.get(...)</code>. <code>$http.get</code> returns a promise object. We'll discuss promises in more detail later; for the moment let us focus on the then method.
- The then method of a promise accepts a callback (a javascript function) that will be invoked with an object wrapping the raw <code>XmlHttpRequest</code> (the browser object to perform Ajax requests).
- By accessing <code>response.data</code>, we can access the json object returned by Open Weather Map. In turn, we save this object in the scope.
- Therefore, what happens is: the user clicks on the button. Angular invokes the function <code>getWeather</code>, that performs the HTTP request to Open Weather Map.
- When the HTTP requests returns, the anonymous function passed to then is executed, and there we'll save the result in the <code>$scope</code>.
- At this point, Angular will hide the second paragraph, fill in the expressions and display the first paragraph with the values returned by the server.

## That's it for now

You're done with this lesson. In the next part, we'll cover applications, modules and services, which will help us structure our code and build more modular applications.
