import collections
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
    def __init__(self, host, port, username=None, token=None):
        self.host = host
        self.port = port
        self.username = None
        self.token = token
        self.usernames = []
        self.groups = []
        self.group_msgs = {}
        self.direct_msgs = {}

    def create_user(self, username, password):
        cmd = harmony_pb2.Command()
        cmd.create_user.username = username
        cmd.create_user.password = password
        cmd.create_user.unused = True
        resp = self.send_cmd(cmd)
        if not resp.HasField('create_user_response'):
            raise RuntimeError('Unknown response from server')
        if resp.create_user_response.success:
            self.token = resp.create_user_response.msg
        else:
            raise RuntimeError(resp.create_user_response.msg)
        return True

    def login(self, username, password):
        cmd = harmony_pb2.Command()
        cmd.login.username = username
        cmd.login.password = password
        resp = self.send_cmd(cmd)
        if not resp.HasField('login_response'):
            raise RuntimeError('Unknown response from server')
        if resp.login_response.success:
            self.token = resp.login_response.token
        else:
            raise RuntimeError(resp.login_response.token)
        self.username = username
        return True

    def is_trial_user(self):
        cmd = harmony_pb2.Command()
        cmd.is_trial_user.token = self.token
        resp = self.send_cmd(cmd)
        if not resp.HasField('is_trial_user_response'):
            raise RuntimeError('Unknown response from server')
        return resp.is_trial_user_response.msg

    def send_group_message(self, target_group, msg):
        msg = self.filter_msg(msg)
        cmd = harmony_pb2.Command()
        cmd.send_group_message.token = self.token
        cmd.send_group_message.target_group = target_group
        cmd.send_group_message.text = msg
        resp = self.send_cmd(cmd)
        if not resp.HasField('send_group_message_response'):
            raise RuntimeError('Unknown response from server')
        return resp.send_group_message_response.success

    def send_direct_message(self, target_user, msg):
        msg = self.filter_msg(msg)
        cmd = harmony_pb2.Command()
        cmd.send_direct_message.token = self.token
        cmd.send_direct_message.target_user = target_user
        cmd.send_direct_message.text = msg

        resp = self.send_cmd(cmd)
        if not resp.HasField('send_direct_message_response'):
            raise RuntimeError('Unknown response from server')
        if not resp.send_direct_message_response.success:
            return False

        fmt_contents = '<{}>: {}'.format(self.username, msg)
        try:
            self.direct_msgs[target_user].append(fmt_contents)
        except KeyError:
            self.direct_msgs[target_user] = collections.deque(
                [fmt_contents], maxlen=100)
        return True

    def get_messages(self):
        cmd = harmony_pb2.Command()
        cmd.get_messages.token = self.token
        resp = self.send_cmd(cmd)
        if not resp.HasField('get_messages_response'):
            raise RuntimeError('Unknown response from server')
        if not resp.get_messages_response.success:
            raise RuntimeError('failed to send group message!!')

        updated_groups = set()
        group_msgs = resp.get_messages_response.group_messages
        for msg in group_msgs:
            updated_groups.add(msg.target_group)
            fmt_contents = '<{}>: {}'.format(msg.sending_user, msg.text)
            try:
                self.group_msgs[msg.target_group].append(fmt_contents)
            except KeyError:
                self.group_msgs[msg.target_group] = collections.deque(
                    [fmt_contents], maxlen=100)

        updated_dms = set()
        direct_msgs = resp.get_messages_response.direct_messages
        for msg in direct_msgs:
            updated_dms.add(msg.sending_user)
            fmt_contents = '<{}>: {}'.format(msg.sending_user, msg.text)
            try:
                self.direct_msgs[msg.sending_user].append(fmt_contents)
            except KeyError:
                self.direct_msgs[msg.sending_user] = collections.deque(
                    [fmt_contents], maxlen=100)

        return updated_groups, updated_dms

    def get_info(self):
        cmd = harmony_pb2.Command()
        cmd.get_info.token = self.token
        resp = self.send_cmd(cmd)
        if not resp.HasField('get_info_response'):
            raise RuntimeError('Unknown response from server')
        if not resp.get_info_response.success:
            raise RuntimeError('failed to send group message!!')

        self.usernames = resp.get_info_response.usernames
        self.groups = resp.get_info_response.groups
        return True

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
        cmd = harmony_pb2.Command()
        cmd.ParseFromString(buf)
        return cmd

    def filter_msg(self, msg):
        # return msg.replace('UGA', '***')
        return msg
