#include <atomic>
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
    std::istringstream get_msg_stream(const int client_fd);
    Command parse_protobuf_msg(std::istringstream* msg_buf_stream);
    Command handle_action(const Command& cmd);
    Command handle_create_user(const CreateUser& cmd);

    const unsigned int max_threads;
    Harmony harmony;
    std::vector<std::thread> threads;
    std::queue<int> client_fd_queue;

    std::atomic_flag queue_lock = ATOMIC_FLAG_INIT;
    std::atomic_flag harmony_lock = ATOMIC_FLAG_INIT;
    bool running = true;
};
