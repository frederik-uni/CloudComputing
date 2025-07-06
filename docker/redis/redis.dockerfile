FROM ubuntu:latest
LABEL maintainer="Karla Schramm"

RUN apt-get update && apt-get upgrade -y --fix-missing
RUN apt-get install lsb-release curl gpg -y
RUN curl -fsSL https://packages.redis.io/gpg | gpg --dearmor -o /usr/share/keyrings/redis-archive-keyring.gpg
RUN chmod 644 /usr/share/keyrings/redis-archive-keyring.gpg
RUN echo "deb [signed-by=/usr/share/keyrings/redis-archive-keyring.gpg] https://packages.redis.io/deb $(lsb_release -cs) main" | tee /etc/apt/sources.list.d/redis.list
RUN apt-get update && apt-get install redis -y
COPY redis.conf /usr/local/etc/redis/redis.conf
COPY entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh

RUN echo "user default on >\${REDIS_PASSWORD} ~* +@all" > /usr/local/etc/redis/users.acl.template

ENTRYPOINT [ "/usr/local/bin/entrypoint.sh" ]