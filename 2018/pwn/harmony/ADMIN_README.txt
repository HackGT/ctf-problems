Build the tool with `make`. It's best to do on Ubuntu 18.04 to ensure
compatibility with docker container.

Requirements:
    - clang
    - pyqt5
    - protobuf

Once built, you can create the two docker files:
    docker build -t harmony -f Dockerfile.server ./
    docker build -t admin -f Dockerfile.admin ./

And run the containers with:
    docker run -p 11111:11111 harmony
    docker run --network="host" admin

If you need to change the address of the server, modify the
Dockerfile.admin ENTRYPOINT parameter to use the IP address rather than
"localhost".

Competitors should be given the COMPETITORS_README.txt file, the
requirements.txt file, the client directory, and the server binary
(server/harmony). Server source code should not be distributed.

The admin folder has a tests.py file that will demonstrate the exploits. The
modified harmony.py file in the admin directory will create the client user as
a non trial user and strip the client side bad word filtering. This SHOULD NOT
be given to the competitors.
