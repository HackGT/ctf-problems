#include "messages.hpp"

DirectMessage::DirectMessage(const std::string& sending_user, const std::string& text) :
    sending_user(sending_user), text(text)
{
}

GroupMessage::GroupMessage(const std::string& sending_user, const std::string& group, const std::string& text) :
    sending_user(sending_user), group(group), text(text)
{
}
