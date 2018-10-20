FROM alpine:latest

RUN apk --no-cache add socat
RUN apk --no-cache add make
RUN apk --no-cache add gcc
RUN apk --no-cache add libc-dev

WORKDIR /usr/local/bin

COPY ./ez.c .
COPY ./Makefile .
COPY ./flag.txt .

RUN make
RUN chmod 755 ez

CMD ["socat", "TCP-LISTEN:3000,fork,reuseaddr", "EXEC:./ez"]