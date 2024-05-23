FROM python:3.10-alpine3.18 AS base

# The enviroment variable ensures that the python output is set straight
# to the terminal with out buffering it first
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1  

WORKDIR /app

COPY requirements.txt .

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt 

RUN apk update 
RUN apk upgrade
RUN apk add firefox

COPY . .

EXPOSE 8000

CMD python manage.py makemigrations api && \ 
    python manage.py migrate && \ 
    python manage.py runserver 0.0.0.0:8000 & celery -A server worker -l info -f celery.log
