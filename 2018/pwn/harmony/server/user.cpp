#include "user.hpp"

User::User(const std::string& username, const std::string& password, const bool trial_user) :
    username(username), password(password), trial_user(trial_user),
    direct_messages(std::make_unique<std::vector<DirectMessage>>()),
    group_messages(std::make_unique<std::vector<GroupMessage>>())
{
}

bool
User::authenticate(const std::string& password) const
{
    return this->password == password;
}

bool
User::get_messages(MessagesToDeliver& out_messages)
{
    // XXX swap these instead? Equivalent.
    out_messages.direct_messages = std::move(direct_messages);
    out_messages.group_messages = std::move(group_messages);

    direct_messages = std::make_unique<std::vector<DirectMessage>>();
    group_messages = std::make_unique<std::vector<GroupMessage>>();
    return true;
}

bool
User::add_direct_message(const std::string& sending_user, const std::string& text)
{
    direct_messages->emplace_back(sending_user, text);
    return true;
}

bool
User::add_group_message(const std::string& sending_user, const std::string& group, const std::string& text)
{
    group_messages->emplace_back(sending_user, group, text);
    return true;
}

std::string
User::get_username() const
{
    return username;
}

bool
User::is_trial_user() const
{
    return trial_user;
}
