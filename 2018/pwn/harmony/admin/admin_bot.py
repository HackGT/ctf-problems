import sys
import time

import harmony


welcome_msgs = [
    'Welcome to Harmony, a chat application!',
    'There are three flags hidden in this application:',
    '\t[1] You are using a trial account. Can you get a real account?',
    '\t[2] The word "UGA" is filtered in Harmony. Can you message it' \
    ' to me?',
    '\t[3] This one is a secret, but you might want to look in the harmony' \
    ' server binary',
    'Good luck!'
]

def main_loop(h, bad_word_flag):
    try:
        while True:
            _, dms = h.get_messages()
            for user in dms:
                try:
                    msg = h.direct_msgs[user][-1]
                except KeyError:
                    continue
                if 'UGA' in msg:
                    h.send_direct_message(user, bad_word_flag)
                else:
                    for welcome in welcome_msgs:
                        h.send_direct_message(user, welcome)
            time.sleep(1)
    except KeyboardInterrupt:
        return



def main():
    if len(sys.argv) >= 2:
        host = sys.argv[1]
    else:
        print('USAGE: python3 admin_bot.py SERVER_IP')
        return -1

    with open('bad_word_flag.txt', 'r') as fh:
        bad_word_flag = fh.read()

    with open('admin_pw.txt', 'r') as fh:
        admin_pw = fh.read()
    h = harmony.HarmonyConnection(host, 11111)
    h.login('admin', admin_pw)
    main_loop(h, bad_word_flag)


if __name__ == '__main__':
    main()
