FROM alpine:latest

RUN apk --no-cache add socat

WORKDIR /usr/local/bin

COPY ./guessmyflag2 .
COPY ./flag.txt .

RUN chmod 755 guessmyflag2

CMD ["socat", "TCP-LISTEN:3000,fork,reuseaddr", "EXEC:./guessmyflag2"]
