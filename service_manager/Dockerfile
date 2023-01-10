FROM python:3.10

RUN apt update -y && apt upgrade -y

RUN apt install gettext -y

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONBUFFERED 1

ENV HOME=/home/app
ENV APP_HOME=/home/app/web

WORKDIR $APP_HOME

RUN pip install --upgrade pip

COPY ./requirements.txt .

RUN pip install -r requirements.txt

COPY . .