import functools
import socket
import struct

import harmony_pb2

def auth(func):
    @functools.wraps(func)
    def inner(self, *args, **kwargs):
        if self.token is None:
            raise RuntimeError('Must be authenticated')
        return func(self, *args, **kwargs)
    return inner

class HarmonyConnection:
    def __init__(self, host, port, token=None):
        self.host = host
        self.port = port
        self.token = token

    def create_user(self, username, password):
        if len(username) > 100 or len(password) > 100:
            raise RuntimeError('Username or password too long')
        cmd = harmony_pb2.Command()
        cmd.create_user.username = username
        cmd.create_user.password = password
        resp = self.send_cmd(cmd)
        print(resp)

    def send_cmd(self, cmd):
        cmd_bytes = cmd.SerializeToString()
        send_len = struct.pack('>H', len(cmd_bytes))
        s = socket.socket()
        s.connect((self.host, self.port))
        s.sendall(send_len)
        s.sendall(cmd_bytes)

        recv_bytes = []
        recv_len = struct.unpack('>H', s.recv(2))[0]
        while recv_len > 0:
            recv_buf_tmp = s.recv(recv_len)
            if recv_buf_tmp is None:
                raise RuntimeError('Socket error')
            recv_bytes.append(recv_buf_tmp)
            recv_len -= len(recv_buf_tmp)
        buf = b''.join(recv_bytes)
        cmd = harmony_pb2
        cmd.ParseFromString(buf)
        return cmd

x = HarmonyConnection('localhost', 11111)
x.create_user('hello', 'world')
