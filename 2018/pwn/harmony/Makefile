CC=clang++
CFLAGS=-g -std=c++1z -Werror -Wextra -Wall -pedantic
LFLAGS=-lprotobuf -lpthread -lstdc++


all: server/harmony client admin

client: client/harmony_pb2.py client/ui/chat_window.py client/ui/login_window.py client/ui/register_window.py

admin: admin/harmony_pb2.py

client/ui/%.py: client/ui/%.ui
	pyuic5 $< > $@

client/harmony_pb2.py : harmony.proto
	protoc -I./client --proto_path=./ --python_out ./client ./harmony.proto

admin/harmony_pb2.py : harmony.proto
	protoc -I./admin --proto_path=./ --python_out ./admin ./harmony.proto

server/proto/harmony.pb.h: harmony.proto
	protoc -I./server --proto_path=./ --cpp_out=./server/proto ./harmony.proto

server/proto/harmony.pb.o: server/proto/harmony.pb.cc
	$(CC) -c -o server/proto/harmony.pb.o server/proto/harmony.pb.cc

server/%.o: server/%.cpp server/proto/harmony.pb.h
	$(CC) -c -o $@ $< $(CFLAGS)

server/harmony: server/harmony.o server/user.o server/messages.o server/server.o server/main.o server/proto/harmony.pb.o
	$(CC) $(LFLAGS) -o $@ $^

clean:
	rm -f server/harmony server/*.o server/proto/*.o server/proto/harmony.pb.cc server/proto/harmony.pb.h client/harmony_pb2.py client/ui/*.py

.PHONY: clean client admin
