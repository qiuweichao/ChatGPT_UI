import os
import sys
import openai
from PyQt5 import QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QTextEdit

try:
    from ctypes import windll  # Only exists on Windows.
    myappid = 'mycompany.myproduct.subproduct.version'
    windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
except ImportError:
    pass
 

class ChatWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ChatGPT")
        self.setGeometry(100, 100, 800, 600)
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)
        self.chat_history = QTextEdit()
        self.chat_history.setFont(QFont('Comic Sans MS', 14))
        self.chat_history.setStyleSheet("""
            background-color: #ffffff;
            border: 1px solid #999999;
            padding: 10px;
            border-radius: 5px;
        """)
        self.layout.addWidget(self.chat_history)
        self.input_layout = QHBoxLayout()
        self.input_field = QLineEdit()
        self.input_field.setFont(QFont('Comic Sans MS', 14))
        self.input_field.setStyleSheet("""
            background-color: #ffffff;
            border: 1px solid #999999;
            padding: 10px;
            border-radius: 5px;
            width: 100%;
        """)
        self.input_layout.addWidget(self.input_field)
        self.send_button = QPushButton("Send")
        self.send_button.setFont(QFont('Comic Sans MS', 14))
        self.send_button.setStyleSheet("""
            background-color: #336699;
            color: #ffffff;
            border: none;
            padding: 10px 20px;
            border-radius: 5px;
        """)
        self.send_button.clicked.connect(self.send_message)
        self.input_layout.addWidget(self.send_button)
        self.layout.addLayout(self.input_layout)
        self.chat_history.setReadOnly(True)
        self.chat_history.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.chat_history.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.input_field.setFocus()
        self.setStyleSheet("""
            background-color: #f5f5f5;
        """)

    def send_message(self):
        message = self.input_field.text()
        self.input_field.clear()
        openai.api_key = "{YOU_API}"
        response = openai.ChatCompletion.create(
            model='gpt-3.5-turbo',
            messages=[
                {"role": "user", "content": message}
            ]
        )
        response_text = response.get('choices')[0]['message']['content']
        self.chat_history.append(f"<span style='font-weight:bold;color:#336699;'>User: </span>{message}")
        self.chat_history.append(f"<span style='font-weight:bold;color:#dc143c;'>AI: </span>{response_text}")


if __name__ == '__main__':
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)  # 支持高分辨率显示器显示
    app = QApplication(sys.argv)
    basedir = os.path.dirname(__file__)
    app.setWindowIcon(QtGui.QIcon(os.path.join(basedir, '123.ico')))
    chat_window = ChatWindow()
    chat_window.show()
    sys.exit(app.exec_())
