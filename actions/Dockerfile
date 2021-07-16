FROM rasa/rasa-sdk:latest

WORKDIR /app

COPY requirements.txt ./

COPY ./ /app/actions

USER root

RUN pip install -r requirements.txt

USER 1000