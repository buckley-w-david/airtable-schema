FROM python:3.6.6 AS build

RUN ["mkdir", "-p", "/opt/airtable"]
RUN ["pip", "install", "poetry"]

COPY . /opt/airtable
WORKDIR /opt/airtable
RUN poetry build -f wheel | grep Built | cut -c10- > wheel.txt

############################################
FROM python:3.6.6-alpine3.7

COPY --from=build /opt/airtable /opt/airtable
WORKDIR /opt/airtable
RUN pip install dist/$(cat wheel.txt)
ENTRYPOINT ["airtable", "schema"]
