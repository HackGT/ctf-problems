#include "harmony.hpp"

#include <algorithm>
#include <fstream>
#include <iostream>
#include <sstream>

static std::string read_file(const std::string& file_name)
{
    std::ifstream fh{file_name};
    if (!fh.is_open()) {
        std::stringstream e_ss;
        e_ss << "Cannot find file " << file_name;
        throw std::runtime_error(e_ss.str());
    }
    std::stringstream contents_ss;
    contents_ss << fh.rdbuf();
    return contents_ss.str();
}

Harmony::Harmony() : group_list{"Hacking", "Off Topic", "Memes"}, trial_flag{read_file("trial_flag.txt")}
{
    std::string admin_pw = read_file("admin_pw.txt");
    add_user("admin", admin_pw, true);
}

bool
Harmony::add_user(const std::string& username, const std::string& password, const bool trial_user)
{
    if (user_name_map.find(username) != user_name_map.end()) {
        return false;
    }
    user_name_map[username] = std::make_unique<User>(username, password, trial_user);
    return true;
}

bool
Harmony::login(const std::string& username, const std::string& password, std::string& out_token)
{
    auto user_iter = user_name_map.find(username);
    if (user_iter == user_name_map.end()) {
        out_token = "Bad username or password";
        return false;
    }

    if (!user_iter->second->authenticate(password)) {
        out_token = "Bad username or password";
        return false;
    }

    out_token = gen_random_token();
    user_token_name_map[out_token] = username;
    return true;
}

bool
Harmony::send_group_message(const std::string& token, const std::string& target_group, const std::string& text)
{
    auto user_iter = user_token_name_map.find(token);
    if (user_iter == user_token_name_map.end()) {
        return false;
    }

    auto group_iter = group_list.find(target_group);
    if (group_iter == group_list.end()) {
        return false;
    }

    for (auto& entry : user_name_map) {
        entry.second->add_group_message(user_iter->second, target_group, text);
    }
    return true;
}

bool Harmony::send_target_message(const std::string& token, const std::string& target_user, const std::string& text) {
    auto sending_user_iter = user_token_name_map.find(token);
    if (sending_user_iter == user_token_name_map.end()) {
        return false;
    }

    auto recv_user_iter = user_name_map.find(target_user);
    if (recv_user_iter == user_name_map.end()) {
        return false;
    }

    recv_user_iter->second->add_direct_message(sending_user_iter->second, text);
    return true;

}

bool
Harmony::get_messages(const std::string& token, MessagesToDeliver& out_messages)
{
    auto user_iter = user_token_name_map.find(token);
    if (user_iter == user_token_name_map.end()) {
        return false;
    }

    auto user = user_name_map.find(user_iter->second);
    if (user == user_name_map.end()) {
        return false;
    }

    return user->second->get_messages(out_messages);
}

bool
Harmony::get_stats(const std::string& token, std::vector<std::string>& out_users, std::vector<std::string>& out_groups) const
{
    auto user_iter = user_token_name_map.find(token);
    if (user_iter == user_token_name_map.end()) {
        return false;
    }

    for (const auto& users : user_name_map) {
        out_users.push_back(users.first);
    }

    for (const auto& group : group_list) {
        out_groups.push_back(group);
    }
    return true;
}

bool
Harmony::get_trial_message(const std::string& token, std::string& out_trial_message) const
{
    const auto user_iter = user_token_name_map.find(token);
    if (user_iter == user_token_name_map.end()) {
        out_trial_message = "Not logged in";
        return false;
    }

    if (user_name_map.at(user_iter->second)->is_trial_user()) {
        out_trial_message = "You are currently using a trial version of Harmony";
    } else {
        out_trial_message = trial_flag;
    }
    return true;
}

std::string
Harmony::gen_random_token() const
{
    auto randchar = []() -> char
    {
        const char charset[] =
        "0123456789"
        "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        "abcdefghijklmnopqrstuvwxyz";
        const size_t max_index = (sizeof(charset) - 1);
        return charset[ rand() % max_index ];
    };
    std::string str(64, 0);
    std::generate_n(str.begin(), 64, randchar);
    return str;
}
