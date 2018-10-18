import random
import string
import threading
import time

import harmony

def thread(i):
    h = harmony.HarmonyConnection('localhost', 11111)
    username = 'test_{}'.format(i)
    password = 'test'
    h.create_user(username, password)
    h.login(username, password)
    while True:
        time.sleep(random.randint(1, 5))
        msg_len = random.randint(8, 20)
        msg = ''.join(
            [random.choice(string.printable) for _ in range(msg_len)]
        )
        h.send_group_message('Hacking', msg)


def main():
    for _ in range(10):
        t = threading.Thread(target=thread, args=(_,))
        t.start()


if __name__ == '__main__':
    main()
