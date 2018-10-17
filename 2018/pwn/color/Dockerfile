FROM ubuntu:18.04
WORKDIR /color

COPY ./color /color
COPY ./flag.txt /color

RUN useradd -ms /bin/bash h3
USER h3

ENTRYPOINT ["/color/color"]
