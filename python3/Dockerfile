FROM python:3.8
ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install -y supervisor

RUN mkdir -p /src
WORKDIR /src
ADD requirements.txt /src/
ADD uwsgi.ini /src/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

ADD supervisor /etc/supervisor/conf.d

WORKDIR /src
