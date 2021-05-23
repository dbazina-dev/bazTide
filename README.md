# bazTide - Microservice for xTide application

**All rights reserved to https://flaterco.com/xtide/disclaimer.html** 

*App was built as wrapper around xTide application.*

**Guide for installing application from Docker hub.**

## 1) Pull image for REST API

```docker pull domo123/baztide:restapi```

## 2)Start docker container, on port 5000. That port is used for fetch request in React

```docker run -it -p 5000:5000 domo123/baztide:restapi```

## 3)Pull image for REACT application

```docker pull domo123/baztide:react```

## 4)Start docker container, I used port 3000.

```docker run -it -p 3000:3000 domo123/baztide:react```

*Now you can use full service, enjoy :)*
