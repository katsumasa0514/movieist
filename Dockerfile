FROM python:3

ENV PYTHONUNBUFFERED 1

RUN mkdir /code/container

RUN mkdir /code/django_app

RUN mkdir /code/django_app/django_app

RUN mkdir /code/movieist

RUN mkdir /code/manage.py

WORKDIR /code

COPY requirements.txt /code/

RUN pip install -r requirements.txt

COPY . /code/

