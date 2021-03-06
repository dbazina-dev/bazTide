# bazTide - Microservice for xTide application
**All rights reserved to https://flaterco.com/xtide/disclaimer.html** 

## What is xTide?
[XTide](https://flaterco.com/xtide/) is a package that provides tide and current predictions in a wide variety of formats.  Graphs, text listings, and calendars can be generated, or a tide clock can be provided on your desktop. XTide can work with X-windows, plain text terminals, or the web.  This is accomplished with three separate programs:  the interactive interface (xtide), the non-interactive or command-line interface (tide), and the web interface (xttpd).

The algorithm that XTide uses to predict tides is the one used by the [National Ocean Service](https://oceanservice.noaa.gov/) in the U.S.  It is significantly more accurate than the simple tide clocks that can be bought in novelty stores.  However, it takes more to predict tides accurately than just a spiffy algorithm—you also need some special data for each and every location for which you want to predict tides.  XTide reads these data from harmonics files.

XTide and its documentation are maintained by David Flater (dave@flaterco.com).

## Cheatsheet for REST-API.
In this REST-API, I have declared 3 different routes that implement xtide functions.

* First one is used for fetching tide data within time period. I've used HTTP (GET) method.

```/data/<location>/tidedata```

* *If you want to fetch data within time period, you can define start date, end date or both of them.*

eg. ```/data/Miami/tidedata?start=2021-05-21 12:00&end=2021-05-22 12:00``` 

* Second one is used for fetching deatailed data about location. I've used HTTP (GET) method.

```/data/<location>/metadata```

* Third one is used for fetching all locations available in xTide application. I've used HTTP (GET) method.

```/search/<chars>```

## How to mount your own harmonics files?
If you want to use Your own harmonic files, it can be done by mounting those files from host.

```docker run -it --mount type=bind,source=/tmp/someHarmonicfile.tcd,target=/usr/share/xtide/someHarmonicfile.tcd domo123/baztide:restapi```

By default, there will be standard xtide harmonics files for United States. 

## Guide for installing service from Docker hub.

* Pull image for REST API

```docker pull domo123/baztide:restapi```

* Start docker container, on port 5000. That port is used for fetch request in React

```docker run -it -p 5000:5000 domo123/baztide:restapi```

* Pull image for REACT application

```docker pull domo123/baztide:react```

* Start docker container, You can use port 3000.

```docker run -it -p 3000:3000 domo123/baztide:react```
## Content of Github repository.

### Environment variables
Inside dockerfile, You can find multiple enviroment variables.
* **HOST** - before initialzing container, You can define network interface on which service will be deployed.
* **PORT** - You can define on which PORT service will listen.
* **DEBUG** - debug mode. To turn it on use any of these values "true, 1, t, y, yes, yeah, yup, certainly, uh-huh, da". If You want to turn it off, use any other value.

### Example folder
In example folder, You will find **React application**. It is used as Graphical user interface, that sends requests to the API.
