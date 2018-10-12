import PyQt5.QtWidgets
import PyQt5.QtGui

import harmony
from ui import chat_window, login_window, register_window


class LoginWindow(login_window.Ui_MainWindow):
    def __init__(self, main_window):
        super(LoginWindow, self).__init__()
        self.main_window = main_window
        self.setupUi(main_window)
        self.load_hooks()

    def load_hooks(self):
        self.login.clicked.connect(self.handle_login)
        self.register_2.clicked.connect(self.handle_register)
        self.password.returnPressed.connect(self.handle_login)

    def handle_login(self):
        username = self.username.text()
        password = self.password.text()

        try:
            self.main_window.harmony.login(username, password)
        except Exception:
            raise
            # TODO handle error
            return
        self.main_window.username = username
        self.main_window.switch_to_chat()

    def handle_register(self):
        self.main_window.switch_to_register()


class RegisterWindow(register_window.Ui_MainWindow):
    def __init__(self, main_window):
        super(RegisterWindow, self).__init__()
        self.main_window = main_window
        self.setupUi(main_window)
        self.load_hooks()

    def load_hooks(self):
        self.register_2.clicked.connect(self.handle_register)
        self.password.returnPressed.connect(self.handle_register)

    def handle_register(self):
        username = self.username.text()
        password = self.password.text()
        try:
            self.main_window.harmony.create_user(username, password)
            self.main_window.switch_to_login()
        except RuntimeError as e:
            self.error_label.setText(str(e))


class ChatWindow(chat_window.Ui_MainWindow):
    def __init__(self, main_window):
        super(ChatWindow, self).__init__()
        self.main_window = main_window
        self.setupUi(main_window)
        self.load_hooks()
        self.load_srv_info()
        self.room_list.setCurrentRow(0)
        self.room_clicked(self.room_list.currentItem())

    def load_hooks(self):
        self.logout.clicked.connect(self.main_window.logout)
        self.new_msg.returnPressed.connect(self.send_message)
        self.send.clicked.connect(self.send_message)

        self.room_list.itemClicked.connect(self.room_clicked)
        self.people_list.itemClicked.connect(self.user_clicked)

    def send_message(self):
        msg = self.new_msg.text()
        if len(msg) == 0:
            return

        room = self.room_list.currentItem()
        dm = self.people_list.currentItem()
        if self.room_list.currentItem() is not None:
            room = room.text()
            self.main_window.harmony.send_group_message(room, msg)
        else:
            dm = dm.text()
            self.main_window.harmony.send_direct_message(dm, msg)

        self.new_msg.clear()
        self.get_messages()

    def load_srv_info(self):
        # TODO call periodically, get new users...
        self.main_window.harmony.get_info()
        self.room_list.clear()
        self.people_list.clear()
        self.room_list.addItems(self.main_window.harmony.groups)
        self.people_list.addItems(self.main_window.harmony.usernames)

    def get_messages(self):
        # TODO run this in new thread, lock harmony instance.
        self.main_window.harmony.get_messages()

    def _display_room(self, room):
        self.message_list.clear()
        try:
            self.message_list.addItems(
                self.main_window.harmony.group_msgs[room])
        except KeyError:
            pass  # No room data yet, empty is fine.
        self.message_list.scrollToBottom()

    def _display_dm(self, user):
        self.message_list.clear()
        try:
            self.message_list.addItems(
                self.main_window.harmony.direct_msgs[user])
        except KeyError:
            pass  # No dm data yet, empty is fine.
        self.message_list.scrollToBottom()

    def room_clicked(self, room):
        self.people_list.clearSelection()
        self.people_list.setCurrentRow(-1)
        self.get_messages()
        self._display_room(room.text())

    def user_clicked(self, user):
        self.room_list.clearSelection()
        self.room_list.setCurrentRow(-1)
        self.get_messages()
        self._display_dm(user.text())


class MainWindow(PyQt5.QtWidgets.QMainWindow):
    def __init__(self, harmony):
        super(MainWindow, self).__init__()
        self.username = None
        self.token = None
        self.harmony = harmony
        self.switch_to_login()

    def switch_to_login(self):
        self.ui = LoginWindow(self)

    def switch_to_register(self):
        self.ui = RegisterWindow(self)

    def switch_to_chat(self):
        self.ui = ChatWindow(self)

    def logout(self):
        # TODO send logout
        self.switch_to_login()

    def exit(self):
        pass


def main():
    harmony_instance = harmony.HarmonyConnection('localhost', 11111)
    app = PyQt5.QtWidgets.QApplication(['Harmony'])
    window = MainWindow(harmony_instance)
    window.show()
    return app.exec_()


if __name__ == '__main__':
    main()
