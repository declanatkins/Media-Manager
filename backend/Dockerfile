FROM python:3.9-slim-buster

COPY source /source
WORKDIR /source
RUN pip install .

EXPOSE 5000

CMD gunicorn -b 0.0.0.0:5000 -w 4 media_api.main:APP