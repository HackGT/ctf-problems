#include <memory>
#include <string>

#include "messages.hpp"

#ifndef HARMONY_USER_H
#define HARMONY_USER_H

class User {
public:
    User(const std::string& username, const std::string& password, const bool trial_user);

    bool authenticate(const std::string& password) const;

    bool get_messages(MessagesToDeliver& out_messages);

    bool add_direct_message(const std::string& sending_user, const std::string& text);

    bool add_group_message(const std::string& sending_user, const std::string& group, const std::string& text);

    std::string get_username() const;
    bool is_trial_user() const;

private:
    const std::string username;
    const std::string password;
    const bool trial_user;

    std::unique_ptr<std::vector<DirectMessage>> direct_messages;
    std::unique_ptr<std::vector<GroupMessage>> group_messages;
};

#endif
