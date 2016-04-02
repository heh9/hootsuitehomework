FROM       ubuntu:latest
MAINTAINER Vladimir "vladimiriacobm@gmail.com"

RUN apt-get update -y
RUN apt-get install -y python-pip python-dev build-essential
COPY requirements.txt webserver.py /webapp/
WORKDIR /webapp
RUN pip install -r requirements.txt
EXPOSE 5000
