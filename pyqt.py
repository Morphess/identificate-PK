from cProfile import label
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QTextEdit, QVBoxLayout, QWidget, QInputDialog
from PyQt5.QtCore import QProcess
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import Qt

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("FACEID")
        
        self.setFixedSize(400, 300)  # Set the size of the window
        self.setStyleSheet("background-image: url(bg2.jpg);")

        self.process = QProcess()
        #self.process.started.connect(self.on_process_started)
        self.process.errorOccurred.connect(self.on_process_error)

        self.run_script()  

        self.command1Button = QPushButton("Додати нове обличчя")
        self.command1Button.clicked.connect(self.send_command1)
        self.command1Button.setFixedSize(380, 30)
        self.command1Button.setStyleSheet("background-color: white; color: black;  font-weight: bold; font-family: Georgia, serif")

        self.command2Button = QPushButton("Запустити FACE ID")
        self.command2Button.clicked.connect(self.send_command2)
        self.command2Button.setFixedSize(380, 40)
        self.command2Button.setStyleSheet("background-color: #7fff00; color: black; font-weight: bold; font-family: Georgia, serif; font-size: 20px")

        self.command3Button = QPushButton("Вихід")
        self.command3Button.clicked.connect(self.close)
        self.command3Button.setFixedSize(380, 30)
        self.command3Button.setStyleSheet("background-color: red; color: black; font-weight: bold; font-family: Georgia, serif")

        self.readyButton = QPushButton("Почати реєстрацію обличчя")
        self.readyButton.clicked.connect(self.send_enter)
        self.readyButton.setEnabled(False)
        self.readyButton.setStyleSheet("background-color: white; color: black; font-weight: bold; font-family: Georgia, serif")

        self.output = QTextEdit()
        self.output.setReadOnly(True)  
        
        self.imageLabel = QLabel(self)
        pixmap = QPixmap('photo.png')
        self.imageLabel.setPixmap(pixmap)
        self.imageLabel.setAlignment(Qt.AlignCenter)

        layout = QVBoxLayout()
        layout.addWidget(self.imageLabel)  
        layout.addWidget(self.command2Button)
        layout.addWidget(self.command1Button)
        layout.addWidget(self.readyButton)
        layout.addWidget(self.command3Button)

        container = QWidget()
        container.setLayout(layout)

        self.setCentralWidget(container)

    def run_script(self):
        #self.process.setWorkingDirectory("C:/Users/User/OneDrive/Робочий стіл/PK/PK")  
        self.process.start("python", ["facerecog.py"])
        started = self.process.waitForStarted(5000)
        if not started:
            print("Process did not start in time")

    #def on_process_started(self):
        #print("Process started")
    def on_process_error(self, error):
        print(f"Process error: {error}")

    def send_command1(self):
        text, ok = QInputDialog.getText(self, 'FACEID', 'Після введеня назви нажміть на кнопку "Почати реєстрацію обличчя":\n\nВведіть назву обличчя:')
        if ok:
            command = f"1\n{text}\n"
        self.process.write(command.encode())
        self.readyButton.setEnabled(True)

    def send_command2(self):
        command = "2\n"
        self.process.write(command.encode())

    def send_enter(self):
        command = "1\n"
        self.process.write(command.encode())

    def on_readyReadStandardOutput(self):
        data = self.process.readAllStandardOutput().data().decode()
        self.output.append(data)

    def on_readyReadStandardError(self):
        data = self.process.readAllStandardError().data().decode()
        self.output.append(data)

app = QApplication([])
window = MainWindow()
window.show()

app.exec_()