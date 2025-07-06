# Cloud computing project

## Setup
### Docker
1. Generate the keys for https: \
`sudo chmod +x nginx/keygen.sh` \
`./nginx/keygen.sh`
2.  Start the docker compose file: \
`docker-compose up`
### Kubernetes
1. Berechtigungen für build und rollout dateien setzen \
`sudo chmod +x build.sh` \
`sudo chmod +x rollout.sh`
2. Build und Rollout ausführen \
`./build.sh` \
`./rollout.sh`
3. Tunnel starten \
`minikube tunnel`
4. Verbinden durch: http://localhost \

*Note: Ich habe keinen `host` bei ingress benutzt, da es DNS probleme gab.
Wenn man eine funktionierende Domain hätte, könnte man es auch einfach einfügen.*


## Docker Einzelbefehle
### Network:
`docker network create webstack`

### Redis:

#### Docker build

`docker build -f redis/redis.dockerfile -t cloud-computing-redis redis/`

##### Docker run

`docker run -it --rm -p 6379:6379 --env REDIS_PASSWORD=1234 --name redis-dev --network webstack cloud-computing-redis`

### Webserver

#### Docker build
`docker build -f webserver/webserver.dockerfile -t webserver webserver/`

##### Docker run

Development:
`docker run -it --rm -p 5000:5000 -v %cd%\webserver\webserver-code:/usr/src/webserver-code/ --entrypoint flask --env REDIS_PASSWORD=1234 --env REDIS_NAME redis-dev --name webserver-dev --network webstack webserver --app /usr/src/webserver-code/app run --host=0.0.0.0 --debug`\
Deploy:
`docker run -it --rm -p 5000:5000 --name webserver --network webstack webserver`