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
        self.setGeometry(300, 100, 800, 600)
        self.setWindowTitle('Новый Январь')
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
# здесь идентификатор модели
        self.model_id = QLineEdit(self)
        self.model_id.resize(150, 40)
        self.model_id.move(600, 110)
# здесь идентификатор плана
        self.plan_id = QLineEdit(self)
        self.plan_id.resize(150, 40)
        self.plan_id.move(600, 160)
# здесь сборка за день
        self.assembly_day = QLineEdit(self)
        self.assembly_day.resize(150, 40)
        self.assembly_day.move(600, 210)
# здесь сборка за месяц
        self.assembly_month = QLineEdit(self)
        self.assembly_month.resize(150, 40)
        self.assembly_month.move(600, 260)
# здесь сварка за день
        self.welding_day = QLineEdit(self)
        self.welding_day.resize(150, 40)
        self.welding_day.move(600, 310)
# здесь сварка за месяц
        self.welding_month = QLineEdit(self)
        self.welding_month.resize(150, 40)
        self.welding_month.move(600, 360)
# идентификатор сдачи
        self.change_id = QLineEdit(self)
        self.change_id.resize(150, 40)
        self.change_id.move(600, 410)
# кнопка добавить запись
        self.btn = QPushButton('Добавить', self)
        self.btn.resize(150, 40)
        self.btn.move(600, 460)
        self.btn.clicked.connect(self.ins)
# кнопка изменить запись
        self.btn = QPushButton('Изменить', self)
        self.btn.resize(150, 40)
        self.btn.move(600, 510)
        self.btn.clicked.connect(self.refresh)
# кнопка удалить запись
        self.btn = QPushButton('Удалить', self)
        self.btn.resize(150, 40)
        self.btn.move(600, 560)
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
        self.model_id.setText('')
        self.plan_id.setText('')
        self.assembly_day.setText('')
        self.assembly_month.setText('')
        self.welding_day.setText('')
        self.welding_month.setText('')
        self.change_id.setText('')
# добавить таблицу новую строку
    def ins(self):
        model_id, plan_id, assembly_day, assembly_month, welding_day, welding_month, change_id\
            = self.model_id.text(), self.plan_id.text(), self.assembly_day.text(), self.assembly_month.text(),\
              self.welding_day.text(), self.welding_month.text(), self.change_id.text()
        try:
            self.cur.execute("""insert into new_january (model_id, plan_id, assembly_day, assembly_month,
             welding_day, welding_month, change_id)
             values (%s,%s,%s,%s,%s,%s,%s)""", (model_id, plan_id, assembly_day, assembly_month,
                                                welding_day, welding_month, change_id))
        except:
            pass
        self.upd()
# удалить из таблицы строку
    def dels(self):
        try:
            ids = int(self.idp.text()) # идентификатор строки
        except:
            return
        self.cur.execute("delete from new_january where id=%s",(ids,))
        self.upd()

# изменение данных в таблице
    def refresh(self):
        model_id, plan_id, assembly_day, assembly_month, welding_day, welding_month, change_id\
            = self.model_id.text(), self.plan_id.text(), self.assembly_day.text(), self.assembly_month.text(),\
              self.welding_day.text(), self.welding_month.text(), self.change_id.text()
        try:
            ids = int(self.idp.text())  # идентификатор строки
        except:
            return
        self.cur.execute("""UPDATE new_january SET model_id = %s, plan_id = %s, assembly_day = %s, assembly_month = %s, 
        welding_day = %s, welding_month = %s, change_id = %s where id = %s""",
                         (model_id, plan_id, assembly_day, assembly_month, welding_day, welding_month, change_id, ids))
        self.upd()

# класс - таблица
class Tb(QTableWidget):
    def __init__(self, wg):
        self.wg = wg  # запомнить окно, в котором эта таблица показывается
        super().__init__(wg)
        self.setGeometry(10, 10, 550, 500)
        self.setColumnCount(8)
        self.verticalHeader().hide();
        self.updt() # обновить таблицу
        self.setEditTriggers(QTableWidget.NoEditTriggers) # запретить изменять поля
        self.cellClicked.connect(self.cellClick)  # установить обработчик щелча мыши в таблице

# обновление таблицы
    def updt(self):
        self.clear()
        self.setRowCount(0);
        self.setHorizontalHeaderLabels(['id', 'id_модель', 'id_план', 'Сборка_день',
                                        'Сборка_месяц', 'Сварка_день', 'Сварка_месяц', 'id_сдача']) # заголовки столцов
        self.wg.cur.execute("select * from new_january order by id asc")
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
        self.wg.model_id.setText(self.item(row, 1).text().strip())
        self.wg.plan_id.setText(self.item(row, 2).text().strip())
        self.wg.assembly_day.setText(self.item(row, 3).text().strip())
        self.wg.assembly_month.setText(self.item(row, 4).text().strip())
        self.wg.welding_day.setText(self.item(row, 5).text().strip())
        self.wg.welding_month.setText(self.item(row, 6).text().strip())
        self.wg.change_id.setText(self.item(row, 7).text().strip())


app = QApplication(sys.argv)
ex = MyWidget()
ex.show()
sys.exit(app.exec_())