import functools
import sys

import PyQt5.QtWidgets
import PyQt5.QtGui
import PyQt5.QtCore

import harmony
from ui import chat_window, login_window, register_window


def locked(func):
    @functools.wraps(func)
    def inner(self, *args, **kwargs):
        lock = PyQt5.QtCore.QMutexLocker(self.lock)
        res = func(self, *args, **kwargs)
        lock.unlock()
        return res
    return inner


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
        except Exception as e:
            self.error_label.setText(str(e))
            return
        trial_resp = self.main_window.harmony.is_trial_user()
        PyQt5.QtWidgets.QMessageBox.question(
            self.main_window, 'Trial Status', trial_resp, PyQt5.QtWidgets.QMessageBox.Ok
        )
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
        self.cancel.clicked.connect(self.main_window.switch_to_login)

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
        self.lock = PyQt5.QtCore.QMutex()
        self.load_hooks()
        self.load_srv_info()
        self.room_list.setCurrentRow(0)
        self.get_messages()

        self.updater_thread = self.Updater()
        self.updater_thread.get_messages.connect(self.get_messages)
        self.updater_thread.load_srv_info.connect(self.load_srv_info)
        self.updater_thread.start()

    class Updater(PyQt5.QtCore.QThread):
        get_messages = PyQt5.QtCore.pyqtSignal()
        load_srv_info = PyQt5.QtCore.pyqtSignal()

        def __init__(self):
            super().__init__()
            self.active = True

        def run(self):
            while self.active:
                self.get_messages.emit()
                self.load_srv_info.emit()
                self.sleep(1)

        def quit(self):
            self.active = False

    def _logout(self):
        self.updater_thread.quit()
        if self.updater_thread.isFinished():
            self.updater_thread.join()
        self.main_window.logout()

    def load_hooks(self):
        self.logout.clicked.connect(self._logout)
        self.new_msg.returnPressed.connect(self.send_message)
        self.send.clicked.connect(self.send_message)

        self.room_list.itemClicked.connect(self.room_clicked)
        self.people_list.itemClicked.connect(self.user_clicked)

    @locked
    def send_message(self, *args, **kwargs):
        msg = self.new_msg.text()
        if len(msg) == 0:
            return

        room = self.room_list.currentItem()
        dm = self.people_list.currentItem()
        if self.room_list.currentItem() is not None:
            room = room.text()
            self.main_window.harmony.send_group_message(room, msg)
        elif dm is not None:
            dm = dm.text()
            self.main_window.harmony.send_direct_message(dm, msg)

        self.new_msg.clear()

    @locked
    def load_srv_info(self):
        self.main_window.harmony.get_info()
        for group in self.main_window.harmony.groups:
            if not self.room_list.findItems(group,
                                            PyQt5.QtCore.Qt.MatchExactly):
                self.room_list.addItem(group)
        for person in self.main_window.harmony.usernames:
            if not self.people_list.findItems(person,
                                              PyQt5.QtCore.Qt.MatchExactly):
                self.people_list.addItem(person)
        return

    @locked
    def get_messages(self):
        color = PyQt5.QtGui.QColor(200, 200, 200)
        brush = PyQt5.QtGui.QBrush(color)
        updated_groups, updated_dms = self.main_window.harmony.get_messages()
        room = self.room_list.currentItem()
        dm = self.people_list.currentItem()
        if room is not None:
            self._display_room(room.text())
        elif dm is not None:
            self._display_dm(dm.text())

        for group in updated_groups:
            for i in range(len(self.room_list)):
                if self.room_list.item(i).text() == group:
                    self.room_list.item(i).setBackground(brush)
        for user in updated_dms:
            for i in range(len(self.people_list)):
                if self.people_list.item(i).text() == user:
                    self.people_list.item(i).setBackground(brush)

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

    @locked
    def room_clicked(self, room):
        color = PyQt5.QtGui.QColor(255, 255, 255)
        brush = PyQt5.QtGui.QBrush(color)
        if room is not None:
            self.people_list.clearSelection()
            self.people_list.setCurrentRow(-1)
            self._display_room(room.text())
            for i in range(len(self.room_list)):
                if self.room_list.item(i).text() == room.text():
                    self.room_list.item(i).setBackground(brush)

    @locked
    def user_clicked(self, user):
        color = PyQt5.QtGui.QColor(255, 255, 255)
        brush = PyQt5.QtGui.QBrush(color)
        if user is not None:
            self.room_list.clearSelection()
            self.room_list.setCurrentRow(-1)
            self._display_dm(user.text())
            for i in range(len(self.people_list)):
                if self.people_list.item(i).text() == user.text():
                    self.people_list.item(i).setBackground(brush)


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
        self.switch_to_login()

    def exit(self):
        pass


def main():
    if len(sys.argv) >= 2:
        host = sys.argv[1]
    else:
        print('Usage: python3 client.py SERVER_IP')
        return -1
    harmony_instance = harmony.HarmonyConnection(host, 11111)
    app = PyQt5.QtWidgets.QApplication(['Harmony'])
    window = MainWindow(harmony_instance)
    window.show()
    return app.exec_()


if __name__ == '__main__':
    main()
