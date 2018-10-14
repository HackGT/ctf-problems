#include <map>
#include <memory>
#include <set>
#include <string>

#include "messages.hpp"
#include "user.hpp"

#ifndef HARMONY_HARMONY_H
#define HARMONY_HARMONY_H

class Harmony {
public:
    Harmony();

    bool add_user(const std::string& username, const std::string& password, const bool trial_user);

    bool login(const std::string& username, const std::string& password, std::string& out_token);

    bool send_group_message(const std::string& token, const std::string& target_group, const std::string& text);
    bool send_target_message(const std::string& token, const std::string& target_user, const std::string& text);

    bool get_messages(const std::string& token, MessagesToDeliver& out_messages);

    bool get_stats(const std::string& token, std::vector<std::string>& out_users, std::vector<std::string>& out_groups) const;

    bool get_trial_message(const std::string& token, std::string& out_trial_message) const;

private:
    std::string gen_random_token() const;

    std::map<std::string, std::unique_ptr<User>> user_name_map;
    std::map<std::string, std::string> user_token_name_map;
    std::set<std::string> group_list;
    const std::string trial_flag;
    const std::string flag_3;

};

#endif
