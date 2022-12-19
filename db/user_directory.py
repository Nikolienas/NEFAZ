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
        self.setGeometry(450, 100, 500, 600)
        self.setWindowTitle('Справочник пользователя')
        self.tb = Tb(self)
# кнопка "обновить"
        self.btn = QPushButton('Обновить', self)
        self.btn.resize(150, 40)
        self.btn.move(300, 10)
        self.btn.clicked.connect(self.upd)
# здесь идентификатор
        self.idp = QLineEdit('Идентификатор', self)
        self.idp.resize(150, 40)
        self.idp.move(300, 60)
        self.idp.setReadOnly(True)
# здесь сдача
        self.change = QLineEdit(self)
        self.change.resize(150, 40)
        self.change.move(300, 110)
# здесь план
        self.plan = QLineEdit(self)
        self.plan.resize(150, 40)
        self.plan.move(300, 160)
# здесь сборка
        self.assembly = QLineEdit(self)
        self.assembly.resize(150, 40)
        self.assembly.move(300, 210)
# здесь сварка
        self.welding = QLineEdit(self)
        self.welding.resize(150, 40)
        self.welding.move(300, 260)
# здесь сотрудники
        self.staff_member = QLineEdit(self)
        self.staff_member.resize(150, 40)
        self.staff_member.move(300, 310)
# кнопка добавить запись
        self.btn = QPushButton('Добавить', self)
        self.btn.resize(150, 40)
        self.btn.move(300, 360)
        self.btn.clicked.connect(self.ins)
# кнопка изменить запись
        self.btn = QPushButton('Изменить', self)
        self.btn.resize(150, 40)
        self.btn.move(300, 410)
        self.btn.clicked.connect(self.refresh)
# кнопка удалить запись
        self.btn = QPushButton('Удалить', self)
        self.btn.resize(150, 40)
        self.btn.move(300, 460)
        self.btn.clicked.connect(self.dels)
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
# добавить таблицу новую строку
    def ins(self):
        change, plan, assembly, welding, staff_member\
            = self.change.text(), self.plan.text(), self.assembly.text(), self.welding.text(), self.staff_member.text()
        try:
            self.cur.execute("""insert into user_directory (change, plan, assembly, welding, staff_member)
                              values (%s,%s,%s,%s,%s)""", (change, plan, assembly, welding, staff_member))
        except:
            pass
        self.upd()
# удалить из таблицы строку
    def dels(self):
        try:
            ids = int(self.idp.text()) # идентификатор строки
        except:
            return
        self.cur.execute("delete from user_directory where id=%s",(ids,))
        self.upd()
# изменить запись в таблице
    def refresh(self):
        change, plan, assembly, welding, staff_member \
            = self.change.text(), self.plan.text(), self.assembly.text(), self.welding.text(), self.staff_member.text()
        try:
            ids = int(self.idp.text())  # идентификатор строки
        except:
            return
        self.cur.execute("""UPDATE user_directory SET change = %s, plan = %s, assembly = %s, welding = %s, 
        staff_member = %s where id=%s""", (change, plan, assembly, welding, staff_member, ids))
        self.upd()


# класс - таблица
class Tb(QTableWidget):
    def __init__(self, wg):
        self.wg = wg  # запомнить окно, в котором эта таблица показывается
        super().__init__(wg)
        self.setGeometry(10, 10, 280, 500)
        self.setColumnCount(6)
        self.verticalHeader().hide();
        self.updt() # обновить таблицу
        self.setEditTriggers(QTableWidget.NoEditTriggers) # запретить изменять поля
        self.cellClicked.connect(self.cellClick)  # установить обработчик щелча мыши в таблице

# обновление таблицы
    def updt(self):
        self.clear()
        self.setRowCount(0);
        self.setHorizontalHeaderLabels(['id', 'Сдача', 'План', 'Сборка', 'Сварка', 'Сотрудник']) # заголовки столцов
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


app = QApplication(sys.argv)
ex = MyWidget()
ex.show()
sys.exit(app.exec_())