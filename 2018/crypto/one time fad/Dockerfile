FROM python:3.4-alpine

WORKDIR /usr/local/bin

RUN apk --no-cache add socat

COPY broken_decrypt.py .
COPY setup.py .
COPY flag.txt .

RUN python ./setup.py
CMD ["socat", "TCP-LISTEN:3000,fork,reuseaddr", "EXEC:\"python ./broken_decrypt.py\""]
