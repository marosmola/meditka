FROM python:3-alpine

RUN apk update && apk add \
    build-base make libxml2-dev libxslt-dev bash

RUN pip install gunicorn

COPY requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

WORKDIR /app
COPY . /app

ENTRYPOINT ["make"]

CMD ["runserver"]
