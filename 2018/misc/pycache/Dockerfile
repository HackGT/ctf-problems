FROM python:2.7-slim

RUN apt update && apt install -y xinetd

WORKDIR /pycache

COPY . /pycache
COPY ./pycache.xinetd /etc/xinetd.d/pycache
COPY ./xinetd.conf /etc/xinetd.conf

ENTRYPOINT ["xinetd", "-dontfork"]
