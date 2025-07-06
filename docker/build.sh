#!/usr/bin/env bash
WEB_IMG=webserver
DB_IMG=redis

docker build -t $WEB_IMG:latest -f webserver/webserver.dockerfile ./webserver
docker build -t $DB_IMG:latest -f redis/redis.dockerfile ./redis

mkdir -p tmp
docker save -o tmp/$WEB_IMG.tar $WEB_IMG
docker save -o tmp/$DB_IMG.tar $DB_IMG

minikube image load tmp/$WEB_IMG.tar
minikube image load tmp/$DB_IMG.tar

rm -r ./tmp