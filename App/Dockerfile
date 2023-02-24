FROM ubuntu:latest
FROM python:3.11


WORKDIR usr/src/flask_app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN apt-get update -y && apt-get upgrade -y
RUN apt-get install wkhtmltopdf -y
COPY . .
EXPOSE 5000
CMD flask --app main.py run --host=0.0.0.0