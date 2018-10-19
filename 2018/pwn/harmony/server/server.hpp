#include <atomic>
#include <condition_variable>
#include <mutex>
#include <queue>
#include <sstream>
#include <thread>
#include <vector>

#include "harmony.hpp"
#include "proto/harmony.pb.h"

class Server
{
public:
    Server(const unsigned int max_threads);
    ~Server();
    Server(const Server& o) = delete;
    Server(Server&& o) = delete;
    Server operator=(const Server& o) = delete;
    Server operator=(Server&& o) = delete;

    void handle_request(const int client_fd);

private:
    void process_request_thread();
    void process_request(const int client_fd);
    int read_exact(const int client_fd, const uint16_t read_len, char* buf);
    int send_exact(const int client_fd, const uint16_t send_len, const char* buf);
    void send_response(const int client_fd, const Command& cmd);
    std::istringstream get_msg_stream(const int client_fd);
    Command parse_protobuf_msg(std::istringstream* msg_buf_stream);
    Command handle_action(const Command& cmd);
    Command handle_create_user(const CreateUser& cmd);
    Command handle_login(const Login& cmd);
    Command handle_send_group_message(const SendGroupMessage& cmd);
    Command handle_send_direct_message(const SendDirectMessage& cmd);
    Command handle_get_messages(const GetMessages& cmd);
    Command handle_get_info(const GetInfo& cmd);
    Command handle_is_trial_user(const IsTrialUser& cmd);

    const unsigned int max_threads;
    Harmony harmony;
    std::vector<std::thread> threads;
    std::queue<int> client_fd_queue;

    std::mutex q_lock;
    std::condition_variable q_cv;
    std::mutex harmony_lock;
    bool running = true;
};
