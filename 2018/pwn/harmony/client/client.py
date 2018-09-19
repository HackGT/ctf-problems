import PyQt5.QtWidgets

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

    def handle_login(self):
        pass

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

    def handle_register(self):
        username = self.username.text()
        password = self.password.text()
        try:
            self.main_window.harmony.create_user(username, password)
            self.main_window.switch_to_login()
        except RuntimeError as e:
            self.error_label.setText(str(e))


class MainWindow(PyQt5.QtWidgets.QMainWindow):
    def __init__(self, harmony):
        super(MainWindow, self).__init__()
        self.harmony = harmony
        self.switch_to_login()

    def switch_to_login(self):
        self.ui = LoginWindow(self)

    def switch_to_register(self):
        self.ui = RegisterWindow(self)

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
