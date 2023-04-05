FROM maven:3.9.0-eclipse-temurin-8

RUN apt-get update && apt-get -y install gnupg unzip iputils-ping

RUN useradd -m builduser

RUN mkdir /app
RUN chown builduser /app

WORKDIR /app
COPY checkrelease.sh .
RUN chmod +x checkrelease.sh

USER builduser

ENTRYPOINT ["sh","checkrelease.sh"]
