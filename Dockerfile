FROM python:3.6.6-alpine3.7 AS build

RUN ["mkdir", "-p", "/opt/airtable"]
COPY . /opt/airtable
WORKDIR /opt/airtable
RUN ["pip", "install", "poetry"]
RUN ["poetry", "config", "settings.virtualenvs.create", "false"]
RUN ["poetry", "dev"]
ENTRYPOINT ["airtable", "schema"]
