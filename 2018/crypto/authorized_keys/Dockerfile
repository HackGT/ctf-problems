FROM python:3-stretch as builder
WORKDIR /flag

RUN pip3 install cryptography
COPY . /flag
RUN ./create.py

FROM buildpack-deps:stretch
WORKDIR /
EXPOSE 22

RUN apt-get update && apt-get install -y openssh-server
RUN useradd -m -s /bin/give_flag gburdell

COPY give_flag /bin/give_flag
COPY flag.txt /root/flag.txt
COPY --from=builder /flag/authorized_keys /home/gburdell/.ssh/authorized_keys

ENTRYPOINT ["/usr/sbin/sshd", "-D"]
