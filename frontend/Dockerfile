FROM python:3.9-slim-buster

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY source /app
WORKDIR /app


CMD gunicorn -b 0.0.0.0:80 -w 4 app:APP 