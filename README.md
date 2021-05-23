# bazTide - Microservice for xTide application

## What is xTide?
XTide is a package that provides tide and current predictions in a wide variety of formats.  Graphs, text listings, and calendars can be generated, or a tide clock can be provided on your desktop. XTide can work with X-windows, plain text terminals, or the web.  This is accomplished with three separate programs:  the interactive interface (xtide), the non-interactive or command-line interface (tide), and the web interface (xttpd).

The algorithm that XTide uses to predict tides is the one used by the National Ocean Service in the U.S.  It is significantly more accurate than the simple tide clocks that can be bought in novelty stores.  However, it takes more to predict tides accurately than just a spiffy algorithm—you also need some special data for each and every location for which you want to predict tides.  XTide reads these data from harmonics files.

XTide and its documentation are maintained by David Flater (dave@flaterco.com).

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
