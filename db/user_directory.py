import sys
import psycopg2
from PyQt5.QtWidgets import QTableWidget, QApplication, QMainWindow, QTableWidget
from PyQt5.QtWidgets import QTableWidgetItem, QWidget, QPushButton, QLineEdit
from PyQt5 import QtGui


class MyWidget(QWidget):
    def __init__(self):
        super().__init__()
# подключить базу данных
        self.con()
# параметры окна
        self.setGeometry(200, 65, 975, 650)
        self.setWindowTitle('Справочник пользователя')
        self.tb = Tb(self)
# кнопка "обновить"
        self.btn = QPushButton('Обновить', self)
        self.btn.resize(150, 40)
        self.btn.move(600, 10)
        self.btn.clicked.connect(self.upd)
# здесь идентификатор
        self.idp = QLineEdit('Идентификатор', self)
        self.idp.resize(150, 40)
        self.idp.move(600, 60)
        self.idp.setReadOnly(True)
# здесь сдача
        self.change = QLineEdit(self)
        self.change.resize(150, 40)
        self.change.move(600, 110)
# здесь план
        self.plan = QLineEdit(self)
        self.plan.resize(150, 40)
        self.plan.move(600, 160)
# здесь сборка
        self.assembly = QLineEdit(self)
        self.assembly.resize(150, 40)
        self.assembly.move(600, 210)
# здесь сварка
        self.welding = QLineEdit(self)
        self.welding.resize(150, 40)
        self.welding.move(600, 260)
# здесь сотрудники
        self.staff_member = QLineEdit(self)
        self.staff_member.resize(150, 40)
        self.staff_member.move(600, 310)
# здесь логин
        self.login = QLineEdit(self)
        self.login.resize(150, 40)
        self.login.move(600, 360)
# здесь пароль
        self.password = QLineEdit(self)
        self.password.resize(150, 40)
        self.password.move(600, 410)
# здесь подразделение
        self.date_of_creation = QLineEdit(self)
        self.date_of_creation.resize(150, 40)
        self.date_of_creation.move(600, 460)
# здесь подразделение
        self.units = QLineEdit(self)
        self.units.resize(150, 40)
        self.units.move(600, 510)
# кнопка добавить запись
        self.btn = QPushButton('Добавить столбец', self)
        self.btn.resize(150, 40)
        self.btn.move(600, 560)
        self.btn.clicked.connect(self.ins)
# кнопка изменить запись
        self.btn = QPushButton('Изменить', self)
        self.btn.resize(150, 40)
        self.btn.move(600, 610)
        self.btn.clicked.connect(self.refresh)
# кнопка удалить запись
        self.btn = QPushButton('Удалить', self)
        self.btn.resize(150, 40)
        self.btn.move(800, 10)
        self.btn.clicked.connect(self.dels)
# проверка сдачи
        self.btn = QPushButton('Проверка сдачи', self)
        self.btn.resize(150, 40)
        self.btn.move(800, 60)
        self.btn.clicked.connect(self.check_change)
# проверка плана
        self.btn = QPushButton('Проверка плана', self)
        self.btn.resize(150, 40)
        self.btn.move(800, 110)
        self.btn.clicked.connect(self.check_plan)
# проверка сборки
        self.btn = QPushButton('Проверка сборки', self)
        self.btn.resize(150, 40)
        self.btn.move(800, 160)
        self.btn.clicked.connect(self.check_assembly)
# проверка сварки
        self.btn = QPushButton('Проверка сварки', self)
        self.btn.resize(150, 40)
        self.btn.move(800, 210)
        self.btn.clicked.connect(self.check_welding)
# добавление роли
        self.btn = QPushButton('Добавление роли', self)
        self.btn.resize(150, 40)
        self.btn.move(800, 260)
        self.btn.clicked.connect(self.adding)

# соединение с базой данных
    def con(self):
        self.conn = psycopg2.connect(user="postgres",
                              password="postgres",
                              host="localhost",
                              port="5432",
                              database="NEFAZ")
        self.cur = self.conn.cursor()
# обновить таблицу и поля
    def upd(self):
        self.conn.commit()
        self.tb.updt()
        self.idp.setText('')
        self.change.setText('')
        self.plan.setText('')
        self.assembly.setText('')
        self.welding.setText('')
        self.staff_member.setText('')
        self.login.setText('')
        self.password.setText('')
        self.date_of_creation.setText('')
        self.units.setText('')
# добавить таблицу новую строку
    def ins(self):
        global login
        global password
        change, plan, assembly, welding, staff_member, login, password, date_of_creation, units = \
        self.change.text(), self.plan.text(), self.assembly.text(), self.welding.text(), self.staff_member.text(),\
        self.login.text(), self.password.text(), self.date_of_creation.text(), self.units.text()
        try:
            self.cur.execute("""insert into user_directory (change, plan, assembly, welding, staff_member, login,
            password, date_of_creation, units) values (%s,%s,%s,%s,%s,%s,%s,%s,%s)""",
                             (change, plan, assembly, welding, staff_member, login, password, date_of_creation, units))
            self.conn.commit()
        except:
            pass
        self.upd()
# удалить из таблицы строку 1073741845
    def dels(self):
        try:
            ids = int(self.idp.text()) # идентификатор строки
        except:
            return
        self.cur.execute("delete from user_directory where id=%s",(ids,))
        self.upd()
# изменить запись в таблице
    def refresh(self):
        global login
        global password
        change, plan, assembly, welding, staff_member, login, password, date_of_creation, units = \
        self.change.text(), self.plan.text(), self.assembly.text(), self.welding.text(), self.staff_member.text(), \
        self.login.text(), self.password.text(), self.date_of_creation.text(), self.units.text()
        try:
            ids = int(self.idp.text())  # идентификатор строки
        except:
            return
        self.cur.execute("""UPDATE user_directory SET change = %s, plan = %s, assembly = %s, welding = %s,
        staff_member = %s, login = %s, password = %s, date_of_creation = %s, units = %s where id=%s""",
                         (change, plan, assembly, welding, staff_member, login, password, date_of_creation, units, ids))
        self.upd()

    def check_change(self):
        try:
            ids = int(self.idp.text())  # идентификатор строки
        except:
            return
        self.cur.execute("""SELECT change from user_directory WHERE id=%s""", (ids, ))
        global a
        a = self.cur.fetchone()
        print(a)
        self.upd()

    def check_plan(self):
        try:
            ids = int(self.idp.text())  # идентификатор строки
        except:
            return
        self.cur.execute("""SELECT plan from user_directory WHERE id=%s""", (ids,))
        global b
        b = self.cur.fetchone()
        print(b)
        self.upd()

    def check_assembly(self):
        try:
            ids = int(self.idp.text())  # идентификатор строки
        except:
            return
        self.cur.execute("""SELECT assembly from user_directory WHERE id=%s""", (ids,))
        global c
        c = self.cur.fetchone()
        print(c)
        self.upd()

    def check_welding(self):
        try:
            ids = int(self.idp.text())  # идентификатор строки
        except:
            return
        self.cur.execute("""SELECT welding from user_directory WHERE id=%s""", (ids,))
        global d
        d = self.cur.fetchone()
        print(d)
        self.upd()

    def adding(self):
        self.cur.execute("""CREATE ROLE %s LOGIN PASSWORD %s""", (login, password))
        self.upd()

    def admin(self):
        if a == True:
            self.cur.execute("""GRANT UPDATE change_id on new_january to %s""", (login, ))
        elif b == True:
            self.cur.execute("""GRANT UPDATE plan_id on new_january to %s""", (login,))
        elif c == True:
            self.cur.execute("""GRANT UPDATE assembly_day on new_january to %s AND
            GRANT UPDATE assembly_month on new_january to %s""", (login, login,))
        elif d == True:
            self.cur.execute("""GRANT UPDATE welding_day on new_january to %s AND
            GRANT UPDATE welding_month on new_january to %s""", (login, login))
        elif a == True and b == True:
            ("""GRANT UPDATE change_id on new_january to %s AND GRANT UPDATE plan_id on new_january to %s""",
             (login, login, ))
        self.upd()

# класс - таблица
class Tb(QTableWidget):
    def __init__(self, wg):
        self.wg = wg  # запомнить окно, в котором эта таблица показывается
        super().__init__(wg)
        self.setGeometry(10, 10, 575, 500)
        self.setColumnCount(10)
        self.verticalHeader().hide();
        self.updt() # обновить таблицу
        self.setEditTriggers(QTableWidget.NoEditTriggers) # запретить изменять поля
        self.cellClicked.connect(self.cellClick)  # установить обработчик щелча мыши в таблице

# обновление таблицы
    def updt(self):
        self.clear()
        self.setRowCount(0);
        self.setHorizontalHeaderLabels(['id', 'Сдача', 'План', 'Сборка', 'Сварка', 'Сотрудник', 'Логин',
                                        'Пароль', 'Время создания', 'Подразделение']) # заголовки столцов
        self.wg.cur.execute("select * from user_directory order by id asc")
        rows = self.wg.cur.fetchall()
        i = 0
        for elem in rows:
            self.setRowCount(self.rowCount() + 1)
            j = 0
            for t in elem: # заполняем внутри строки
                self.setItem(i, j, QTableWidgetItem(str(t).strip()))
                j += 1
            i += 1
        self.resizeColumnsToContents()

# обработка щелчка мыши по таблице
    def cellClick(self, row, col): # row - номер строки, col - номер столбца
        self.wg.idp.setText(self.item(row, 0).text())
        self.wg.change.setText(self.item(row, 1).text().strip())
        self.wg.plan.setText(self.item(row, 2).text().strip())
        self.wg.assembly.setText(self.item(row, 3).text().strip())
        self.wg.welding.setText(self.item(row, 4).text().strip())
        self.wg.staff_member.setText(self.item(row, 5).text().strip())
        self.wg.login.setText(self.item(row, 6).text().strip())
        self.wg.password.setText(self.item(row, 7).text().strip())
        self.wg.date_of_creation.setText(self.item(row, 8).text().strip())
        self.wg.units.setText(self.item(row, 9).text().strip())

app = QApplication(sys.argv)
ex = MyWidget()
ex.show()
sys.exit(app.exec_())