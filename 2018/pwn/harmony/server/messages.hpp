#include <memory>
#include <vector>
#include <string>

#ifndef HARMONY_MESSAGES_H
#define HARMONY_MESSAGES_H

struct DirectMessage {
    DirectMessage(const std::string& sending_user, const std::string& text);

    std::string sending_user;
    std::string text;
};

struct GroupMessage {
    GroupMessage(const std::string& sending_user, const std::string& group, const std::string& text);

    std::string sending_user;
    std::string group;
    std::string text;
};

struct MessagesToDeliver {
    std::unique_ptr<std::vector<DirectMessage>> direct_messages;
    std::unique_ptr<std::vector<GroupMessage>> group_messages;
};

#endif
