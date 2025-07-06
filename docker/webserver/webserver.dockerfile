FROM ubuntu:24.04
LABEL maintainer="Karla Schramm"
RUN apt-get update && apt-get upgrade -y
RUN apt-get install python3-full python3-pip -y

COPY entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh

RUN mkdir -p /usr/src/webserver-code

COPY webserver-code/ /usr/src/webserver-code/
WORKDIR /usr/src/webserver-code/
RUN python3 -m venv /venv # todo: no venv needed in docker
ENV PATH="/venv/bin:$PATH"
RUN pip install --no-cache-dir -r /usr/src/webserver-code/requirements.txt

ENTRYPOINT [ "/usr/local/bin/entrypoint.sh" ]
