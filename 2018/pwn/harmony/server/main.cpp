#include <iostream>

#include <arpa/inet.h>
#include <cstring>
#include <sys/socket.h>

#include "proto/harmony.pb.h"
#include "server.hpp"

int main()
{
    GOOGLE_PROTOBUF_VERIFY_VERSION;

    Server server{5};

    struct sockaddr_in saddr;
    memset(&saddr, 0, sizeof(struct sockaddr_in));
    int socket_fd = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP);
    if (socket_fd == -1) {
        std::cout << "Failed to create socket" << std::endl;
        return 1;
    }

    saddr.sin_family = AF_INET;
    saddr.sin_addr.s_addr = htonl(INADDR_ANY);
    saddr.sin_port = htons(11111);

    if (bind(socket_fd, (struct sockaddr*)(&saddr), sizeof(saddr)) != 0) {
        std::cout << "Failed to bind socket" << std::endl;
        return 1;
    }
    if (listen(socket_fd, 100) != 0) {
        printf("Failed to start listening\n");
        return 1;
    }

    while (1) {
        int client_fd = accept(socket_fd, NULL, NULL);
        if (client_fd == -1) {
            std::cout << "Error accepting client.  Continuing..." << std::endl;
            continue;
        }
        server.handle_request(client_fd);
    }
}
