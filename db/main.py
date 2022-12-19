import sys
from PyQt5.QtWidgets import QMainWindow, QPushButton, QApplication, QLineEdit, QLabel, QHBoxLayout
import os
import psycopg2
from PyQt5.QtGui import QPixmap


class START(QMainWindow):

    def __init__(self):
        super().__init__()
        self.access_db()

    def access_db(self):
        global logo
        pixmap = QPixmap('logo.jpg')
        logo = QLabel(self)
        logo.setPixmap(pixmap)
        logo.resize(700, 70)
        logo.move(20, 20)

        global name
        name = QLineEdit(self)
        name.resize(150, 35)
        name.setPlaceholderText('Введите логин:')
        name.move(100, 100)

        global password
        password = QLineEdit(self)
        password.resize(150, 35)
        password.setPlaceholderText('Введите пароль:')
        password.move(100, 150)

        global enter
        enter = QPushButton('Войти', self)
        enter.resize(60, 35)
        enter.move(145, 200)

        enter.clicked.connect(self.buttonClicked)

        self.setGeometry(500, 100, 400, 400)
        self.setWindowTitle('ВХОД')
        self.show()

    def initUI(self):
        btn1 = QPushButton("Справочник моделей", self)
        btn1.resize(200, 50)
        btn1.move(50, 25)

        btn2 = QPushButton("Справочник пользователя", self)
        btn2.resize(200, 50)
        btn2.move(50, 80)

        btn3 = QPushButton("Новый Январь", self)
        btn3.resize(200, 50)
        btn3.move(50, 135)

        btn1.clicked.connect(self.buttonClicked)
        btn2.clicked.connect(self.buttonClicked)
        btn3.clicked.connect(self.buttonClicked)


        self.setGeometry(550, 300, 300, 205)
        self.setWindowTitle('NEFAZ')
        self.show()

    def buttonClicked(self):
        sender = self.sender()
        if sender.text() == "Справочник моделей":
            self.hide()
            os.system(r'model_directory.py')
            self.termiante()
        elif sender.text() == "Справочник пользователя":
            self.hide()
            os.system(r'user_directory.py')
            self.terminate()
        elif sender.text() == "Новый Январь":
            self.hide()
            os.system(r'new_january.py')
            self.terminate()
        elif sender.text() == 'Войти':
            self.conn = psycopg2.connect(user=name.text(),
                                         password=password.text(),
                                         host="localhost",
                                         port="5432",
                                         database="NEFAZ")
            self.cur = self.conn.cursor()
            logo.hide(), self.hide(), enter.hide(), name.hide(), password.hide()
            self.initUI()


            # self.cur.execute("""SELECT * FROM model_directory""")
            # sv = self.cur.fetchone()
            # print(sv)
            # self.conn.commit

if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = START()
    sys.exit(app.exec_())


