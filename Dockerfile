FROM python:3.7-alpine

LABEL maintainer="DeedWark - github.com/DeedWark"

WORKDIR /app

COPY app/ /app

ARG ZENDESK_TOKEN
ENV ZENDESK_TOKEN=${ZENDESK_TOKEN}

RUN pip3 install -r requirements.txt &&\
    apk add --no-cache ruby &&\
    gem install ruby-msg

CMD ["python", "/app/msg2eml.py"]
