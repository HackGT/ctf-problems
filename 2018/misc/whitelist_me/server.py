import socket
import time
import threading
import regex
import sys

FLAG = "hackgt{two_is_b3tter_than_uno}\n"
FLAG2 = "hackgt{lol_y0u_technically_DOSd_urse1f}\n"
MY_SECRET_EMAIL = "9023802938402394820394820394823094823094823@gmail.com"

INTRO_TEXT = """################################################
HELLO, welcome to this server. Your IP will be temporary allowed.
If you supply the correct email, your IP will be permenently whitelisted.
If you don't, the temporary whitelist will be removed.
################################################
Please enter your email: """

STAGE_TWO_TEXT = """
CONGRATS YOU GOT THE FLAG {}.
Welcome to the admin panel.
1). Change Admin Email
2). Exit
"""

FINAL_TEXT = """
CONGRATS YOU GOT THE FLAG {}.
We aren't going to actually change the email,
cause that would be RIP. But take your prize!

"""

EMAIL_REGEX = r'^([a-zA-Z0-9])(([_]+)?([a-zA-Z0-9]+))*(@){1}[a-z0-9]+[.]{1}(([a-z]{2,3})|([a-z]{2,3}[.]{1}[a-z]{2,3}))$'

WHITELISTED_IPS = []
WHITELIST_MUTEX = threading.Lock()

def check_auth(unit, old_email, answer_store):
    out = regex.match(EMAIL_REGEX, unit)
    out2 = (MY_SECRET_EMAIL == old_email)
    if out and out2:
        answer_store[0] = False
    else:
        answer_store[0] = True

def async_auth(new_email, old_email):
    no_match = [None,] # Lets not waste a class, a list should suffice to pass by reference.
    t = threading.Thread(target=check_auth, args=(new_email, old_email, no_match)) # This will make things faster, right?
    t.start()
    t.join(10.0) # Prevent DOS.
    return no_match[0]

# Whitelist / Blacklist Helpers
def whitelist_ip(ip):
    WHITELIST_MUTEX.acquire()
    WHITELISTED_IPS.append(ip)
    WHITELIST_MUTEX.release()

def remove_ip(ip):
    WHITELIST_MUTEX.acquire()
    if ip in WHITELISTED_IPS:
        WHITELISTED_IPS.remove(ip)
    WHITELIST_MUTEX.release()

def is_auth(ip):
    WHITELIST_MUTEX.acquire()
    to_return = ip in WHITELISTED_IPS
    WHITELIST_MUTEX.release()
    return to_return

def handle(conn, addr):
    local_email = MY_SECRET_EMAIL
    ip = addr[0]
    if is_auth(ip):
        conn.sendall(STAGE_TWO_TEXT.format(FLAG).encode())
        selection = conn.recv(1024).decode('utf-8').strip()
        if selection.isnumeric() and int(selection) == 1:
            conn.sendall(b"What would you like to change your email to?\n")
            to_change = conn.recv(1024).decode('utf-8').strip()

            conn.sendall(b"Please confirm your old email...\n")
            old_email = conn.recv(1024).decode('utf-8').strip()

            if not async_auth(to_change, old_email):
                conn.sendall(FINAL_TEXT.format(FLAG2).encode())
            else:
                conn.sendall(b"Nah...\n")

    else:
        conn.sendall(INTRO_TEXT.encode())
        whitelist_ip(ip)
        email = conn.recv(1024).decode('utf-8').strip()

        if email == local_email:
            conn.sendall(b"Cool, we'll auth you forever\n")
        else:
            conn.sendall(b"Nah, removing your whitelist...\n")
            remove_ip(ip)
    conn.close()

if __name__ == "__main__":
    HOST = ''   # Symbolic name, meaning all available interfaces
    PORT = 9876 # Arbitrary non-privileged port

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    #Bind socket to local host and port
    try:
        s.bind((HOST, PORT))
    except socket.error as msg:
        sys.exit()

    #Start listening on socket
    s.listen(10)

    #now keep talking with the client
    try:
        while 1:
            #wait to accept a connection - blocking call
            conn, addr = s.accept()
            t = threading.Thread(target=handle, args=(conn, addr))
            t.start()
    except KeyboardInterrupt:
        s.close()
