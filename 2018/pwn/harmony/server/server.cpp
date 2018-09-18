#include "server.hpp"

#include <iostream>

#include <arpa/inet.h>
#include <sys/socket.h>
#include <sys/types.h>
#include <unistd.h>

Server::Server(const unsigned int max_threads) : max_threads(max_threads)
{
    while (queue_lock.test_and_set()) {}
    for (unsigned int i = 0; i < max_threads; i++) {
        threads.emplace_back(&Server::process_request_thread, this);
    }
    queue_lock.clear();
}

Server::~Server()
{
    running = false;
    while (queue_lock.test_and_set()) {}
    for (unsigned i = 0; i < max_threads; i++) {
        if (threads[i].joinable()) {
            threads[i].join();
        }
    }
    queue_lock.clear();
}

void
Server::handle_request(const int client_fd)
{
    while (queue_lock.test_and_set()) {}
    client_fd_queue.push(client_fd);
    queue_lock.clear();
}

void
Server::process_request_thread()
{
    int client_fd = -1;
    while (running) {
        while (queue_lock.test_and_set()) {}
        if (client_fd_queue.size() > 0) {
            client_fd = client_fd_queue.front();
            client_fd_queue.pop();
        }
        queue_lock.clear();

        if (client_fd >= 0) {
            process_request(client_fd);
            client_fd = -1;
        }
    }
}

void
Server::process_request(const int client_fd)
{
    std::istringstream msg_buf_stream = get_msg_stream(client_fd);
    Command cmd = parse_protobuf_msg(&msg_buf_stream);
    Command rsp = handle_action(cmd);
    send_response(client_fd, rsp);
}

Command
Server::parse_protobuf_msg(std::istringstream* msg_buf_stream)
{
    Command cmd;
    if (!cmd.ParseFromIstream(msg_buf_stream)) {
        throw std::runtime_error("Bad message");
    }
    return cmd;
}

void
Server::send_response(const int client_fd, const Command& cmd)
{
    std::string out;
    cmd.SerializeToString(&out);
    uint16_t send_len = htons(out.size());
    if (send_exact(client_fd, 2, (char*)(&send_len)) < 0) {
        return;
    }
    if (send_exact(client_fd, out.size(), out.c_str())) {
        return;
    }
    return;
}

Command
Server::handle_action(const Command& cmd)
{
    if (cmd.has_create_user()) {
        return handle_create_user(cmd.create_user());
    } else if (cmd.has_create_user_response()) {
    } else if (cmd.has_create_user_response()) {
    } else if (cmd.has_login()) {
        std::cout << "Login" << std::endl;
    } else if (cmd.has_login_response()) {
    } else if (cmd.has_send_group_message()) {
    } else if (cmd.has_send_group_message_response()) {
    } else if (cmd.has_send_direct_message()) {
    } else if (cmd.has_send_direct_message_response()) {
    } else if (cmd.has_get_messages()) {
    } else if (cmd.has_get_messages_response()) {
    } else if (cmd.has_get_info()) {
    } else if (cmd.has_get_info_response()) {
    } else if (cmd.has_is_trial_user()) {
    } else if (cmd.has_is_trial_user_response()) {
    } else {
    }
    throw std::runtime_error("Invalid command");
}

Command
Server::handle_create_user(const CreateUser& cmd)
{
    Command out_cmd;
    std::string out_message;
    if (harmony.login(cmd.username(), cmd.password(), out_message)) {
        out_cmd.mutable_create_user_response()->set_success(true);
    } else {
        out_cmd.mutable_create_user_response()->set_success(false);
    }
    out_cmd.mutable_create_user_response()->set_msg(out_message);
    return out_cmd;
}

int
Server::read_exact(const int client_fd, const uint16_t read_len, char* buf)
{
    // TODO: add timeout here
    uint16_t curr_read = 0;
    while (curr_read < read_len) {
        ssize_t recv_res = recv(client_fd, (buf + curr_read), (read_len - curr_read), 0);
        if (recv_res < 0) {
            return -1;
        }
        curr_read += recv_res;
    }
    return curr_read;
}

int
Server::send_exact(const int client_fd, const uint16_t send_len, const char* buf)
{
    // TODO add timeout here
    uint16_t curr_sent = 0;
    while (curr_sent < send_len) {
        ssize_t send_res = send(client_fd, (buf + curr_sent), (send_len - curr_sent), 0);
        if (send_res < 0) {
            return -1;
        }
        curr_sent += send_res;
    }
    return curr_sent;
}

std::istringstream
Server::get_msg_stream(const int client_fd)
{
    uint16_t msg_len;
    if (read_exact(client_fd, 2, (char*)(&msg_len)) < 0) {
        close(client_fd);
        throw std::runtime_error{"Bad client connection"};
    }

    msg_len = ntohs(msg_len);
    char* msg_buf;
    try {
        msg_buf = new char[msg_len];
    } catch (std::bad_alloc) {
        close(client_fd);
        throw std::runtime_error{"Bad alloc"};
    }

    if (read_exact(client_fd, msg_len, msg_buf) < 0) {
        delete msg_buf;
        close(client_fd);
        throw std::runtime_error{"Bad client connection"};
    }

    std::istringstream msg_buf_stream{std::string{msg_buf, msg_len}};
    delete msg_buf;
    return msg_buf_stream;
}
