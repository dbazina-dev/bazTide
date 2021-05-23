FROM ubuntu:latest

RUN apt-get update -y && apt-get install -y python3 python3-pip xtide

RUN touch /root/.disableXTidedisclaimer
    
RUN DEBIAN_FRONTEND="noninteractive" apt-get -y install tzdata locales && locale-gen en_US.UTF-8

ENV LANG='en_US.UTF-8' LANGUAGE='en_US:en' LC_ALL='en_US.UTF-8' HOST='0.0.0.0' PORT=5000 DEBUG=true

WORKDIR /app

RUN pip3 install --no-cache-dir flask pandas DateTime && pip3 install -U flask-cors

COPY main.py /app
COPY backend.py /app

CMD [ "python3", "main.py" ]
