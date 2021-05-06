# imagem base
FROM python:2.7

RUN pip install -r requirements.txt

ENV PYTHONDONTWRITEBYTECODE 1

RUN apt update \
    && apt install -y libpq-dev gcc

RUN pip install psycopg2

WORKDIR /code
COPY . /code/