FROM alpine:latest

RUN apk --no-cache add socat

COPY ez .
COPY flag.txt .

CMD ["socat", "TCP-LISTEN:3000,fork,reuseaddr", "EXEC:\"./ez\""]
