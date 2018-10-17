import random
import string
import sys
import time

import harmony


def main():
    if len(sys.argv) >= 2:
        host = sys.argv[1]
    else:
        print('USAGE: python3 admin_bot.py SERVER_IP')
        return -1

    username = ''.join([random.choice(string.printable) for _ in range(5)])
    password = ''.join([random.choice(string.printable) for _ in range(60)])
    h = harmony.HarmonyConnection(host, 11111)
    h.create_user(username, password)
    h.login(username, password)

    print(h.is_trial_user())

    h.send_direct_message('admin', 'UGA')
    time.sleep(3)
    h.get_messages()
    print(h.direct_msgs['admin'][-1])

    h.send_direct_message('admin', '    SWoRdfiSh' + 'a'*242)
    time.sleep(3)
    h.get_messages()
    print(h.direct_msgs['admin'][-1])


if __name__ == '__main__':
    main()
