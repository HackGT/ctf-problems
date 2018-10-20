FROM alpine:latest

RUN apk --no-cache add socat

WORKDIR /usr/local/bin

COPY ./guessmyflag .
COPY ./flag.txt .

RUN chmod 755 guessmyflag

CMD ["socat", "TCP-LISTEN:3000,fork,reuseaddr", "EXEC:./guessmyflag"]
