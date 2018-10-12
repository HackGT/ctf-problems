#include "server.hpp"

#include <chrono>
#include <iostream>

#include <arpa/inet.h>
#include <sys/socket.h>
#include <sys/types.h>
#include <unistd.h>

Server::Server(const unsigned int max_threads) : max_threads(max_threads)
{
    for (unsigned int i = 0; i < max_threads; i++) {
        threads.emplace_back(&Server::process_request_thread, this);
    }
}

Server::~Server()
{
    running = false;
    std::lock_guard<std::mutex> guard{q_lock};
    for (unsigned i = 0; i < max_threads; i++) {
        if (threads[i].joinable()) {
            threads[i].join();
        }
    }
}

void
Server::handle_request(const int client_fd)
{
    std::unique_lock<std::mutex> lk{q_lock};
    client_fd_queue.push(client_fd);
    lk.unlock();
    q_cv.notify_one();
}

void
Server::process_request_thread()
{
    using namespace std::chrono_literals;

    std::unique_lock<std::mutex> lk{q_lock, std::defer_lock};
    while (running) {
        lk.lock();
        q_cv.wait(lk, [this]{return this->client_fd_queue.size() > 0;});

        int client_fd = -1;
        if (client_fd_queue.size() > 0) {
            client_fd = client_fd_queue.front();
            client_fd_queue.pop();
        }
        lk.unlock();

        if (client_fd >= 0) {
            process_request(client_fd);
        }
        std::this_thread::sleep_for(1s);
    }
}

void
Server::process_request(const int client_fd)
{
    try {
        std::istringstream msg_buf_stream = get_msg_stream(client_fd);
        Command cmd = parse_protobuf_msg(&msg_buf_stream);
        Command rsp = handle_action(cmd);
    send_response(client_fd, rsp);
    } catch (const std::runtime_error& e) {
        std::cout << "Error " << e.what() << std::endl;
    }
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
        std::cout << "Has create user" << std::endl;
        return handle_create_user(cmd.create_user());
    } else if (cmd.has_login()) {
        return handle_login(cmd.login());
    } else if (cmd.has_send_group_message()) {
        return handle_send_group_message(cmd.send_group_message());
    } else if (cmd.has_send_direct_message()) {
        return handle_send_direct_message(cmd.send_direct_message());
    } else if (cmd.has_get_messages()) {
        return handle_get_messages(cmd.get_messages());
    } else if (cmd.has_get_info()) {
        return handle_get_info(cmd.get_info());
    } else if (cmd.has_is_trial_user()) {
        return handle_is_trial_user(cmd.is_trial_user());
    }

    // No valid command
    Command resp;
    resp.mutable_invalid_command_response()->set_msg("Invalid Command");
    return resp;
}

Command
Server::handle_create_user(const CreateUser& cmd)
{
    // TODO: field size checking
    Command out_cmd;
    std::string out_message;
    if (harmony.add_user(cmd.username(), cmd.password(), cmd.trial_user())) {
        out_message = "Successfully created user";
        out_cmd.mutable_create_user_response()->set_success(true);
    } else {
        out_message = "User already exists";
        out_cmd.mutable_create_user_response()->set_success(false);
    }
    out_cmd.mutable_create_user_response()->set_msg(out_message);
    return out_cmd;
}

Command
Server::handle_login(const Login& cmd)
{
    Command out_cmd;
    std::string out_token;

    bool succ = harmony.login(cmd.username(), cmd.password(), out_token);
    std::cout << "Trying to login user: " << cmd.username() << cmd.password() << std::endl;
    out_cmd.mutable_login_response()->set_success(succ);
    out_cmd.mutable_login_response()->set_token(out_token);
    return out_cmd;
}

Command
Server::handle_send_group_message(const SendGroupMessage& cmd)
{
    Command out_cmd;
    bool succ = harmony.send_group_message(cmd.token(), cmd.target_group(), cmd.text());
    out_cmd.mutable_send_group_message_response()->set_success(succ);
    return out_cmd;
}

Command
Server::handle_send_direct_message(const SendDirectMessage& cmd)
{
    Command out_cmd;
    bool succ = harmony.send_target_message(cmd.token(), cmd.target_user(), cmd.text());
    out_cmd.mutable_send_direct_message_response()->set_success(succ);
    return out_cmd;
}

Command
Server::handle_get_messages(const GetMessages& cmd)
{
    Command out_cmd;
    MessagesToDeliver out_msgs;

    bool succ = harmony.get_messages(cmd.token(), out_msgs);
    out_cmd.mutable_get_messages_response()->set_success(succ);

    if (out_msgs.direct_messages != nullptr) {
        for (const auto& dm : *out_msgs.direct_messages) {
            GetDirectMessageResponse* pb_msg = out_cmd.mutable_get_messages_response()->add_direct_messages();
            pb_msg->set_sending_user(dm.sending_user);
            pb_msg->set_text(dm.text);
        }
    }
    if (out_msgs.group_messages != nullptr) {
        for (const auto& dm : *out_msgs.group_messages) {
            GetGroupMessageResponse* pb_msg = out_cmd.mutable_get_messages_response()->add_group_messages();
            pb_msg->set_sending_user(dm.sending_user);
            pb_msg->set_target_group(dm.group);
            pb_msg->set_text(dm.text);
        }
    }

    return out_cmd;
}

Command
Server::handle_get_info(const GetInfo& cmd)
{
    Command out_cmd;
    std::vector<std::string> out_users;
    std::vector<std::string> out_groups;

    bool succ = harmony.get_stats(cmd.token(), out_users, out_groups);
    out_cmd.mutable_get_info_response()->set_success(succ);

    for (const auto& usr : out_users) {
        out_cmd.mutable_get_info_response()->add_usernames(usr);
    }
    for (const auto& grp : out_groups) {
        out_cmd.mutable_get_info_response()->add_groups(grp);
    }

    return out_cmd;
}

Command
Server::handle_is_trial_user(const IsTrialUser& cmd)
{
    Command out_cmd;
    std::string out_trial_msg;

    harmony.get_trial_message(cmd.token(), out_trial_msg);
    // TODO handle false...
    out_cmd.mutable_is_trial_user_response()->set_msg(out_trial_msg);

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
