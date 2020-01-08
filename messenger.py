import datetime
import time
import design
import requests
import threading
from PyQt5 import QtWidgets


class MessengerApp(QtWidgets.QMainWindow, design.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.send)
        threading.Thread(target=self.receive).start()

    def send(self):
        username = self.lineEdit.text()
        password = self.lineEdit_2.text()
        text = self.plainTextEdit.toPlainText().strip()

        if not username or not password or not text:
            return

        try:
            response = requests.post(
                'http://127.0.0.1:5000/send',
                json={'username': username, 'password': password, 'text': text}
            )
            self.plainTextEdit.clear()

        except:
            pass

    def receive(self):
        last_received = 0
        while True:
            response = requests.get(
                'http://127.0.0.1:5000/messages',
                params={'after': last_received}
            )
            if response.status_code == 200:
                messages = response.json()['messages']
                for message in messages:
                    self.textBrowser.append(message['username'] + ' ' +
                                            datetime.datetime.fromtimestamp(message['time']).strftime('%H:%M:%S'))
                    self.textBrowser.append(message['text'] + '\n')
                    last_received = message['time']

            time.sleep(1)


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    window = MessengerApp()
    window.show()
    app.exec_()
