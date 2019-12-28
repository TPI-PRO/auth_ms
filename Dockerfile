FROM python:3.6-alpine

RUN mkdir /app
WORKDIR /app
COPY . /app
RUN pip install -r requirements.txt
RUN flask db init
RUN flask db migrate 
RUN flask db upgrade
