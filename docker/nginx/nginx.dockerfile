FROM ubuntu:latest
LABEL maintainer="Karla Schramm"

RUN apt-get update && apt-get upgrade -y
RUN apt-get install nginx -y
RUN apt-get install gettext -y

COPY entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh

COPY nginx.conf.template /etc/nginx/nginx.conf.template

ENTRYPOINT [ "/usr/local/bin/entrypoint.sh" ]

