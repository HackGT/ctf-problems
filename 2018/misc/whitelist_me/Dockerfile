FROM frolvlad/alpine-python3

RUN apk add gcc python3-dev musl-dev
RUN pip3 install regex

COPY server.py /
ENTRYPOINT ["python3"]
CMD ["server.py"]
