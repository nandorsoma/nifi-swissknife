#!/bin/sh

id=$(openssl rand -hex 12)

mkdir buildresult

docker build -t nifi-build-image-$id .
docker run --name nifi-build-container-$id -v "$(pwd)"/buildresult:/buildresult nifi-build-image-$id $1 $2 $3

docker rm nifi-build-container-$id
docker rmi nifi-build-image-$id
