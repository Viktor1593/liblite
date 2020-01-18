# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'F:\PyScripts\liblite\liblite_ui.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(872, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.cmd_read_in_notepad = QtWidgets.QPushButton(self.centralwidget)
        self.cmd_read_in_notepad.setGeometry(QtCore.QRect(370, 10, 111, 23))
        self.cmd_read_in_notepad.setObjectName("cmd_read_in_notepad")
        self.lib_table = QtWidgets.QTableWidget(self.centralwidget)
        self.lib_table.setGeometry(QtCore.QRect(10, 40, 471, 511))
        self.lib_table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.lib_table.setObjectName("lib_table")
        self.lib_table.setColumnCount(0)
        self.lib_table.setRowCount(0)
        self.lib_table.verticalHeader().setVisible(False)
        self.cmd_edit_book = QtWidgets.QPushButton(self.centralwidget)
        self.cmd_edit_book.setGeometry(QtCore.QRect(620, 160, 111, 23))
        self.cmd_edit_book.setObjectName("cmd_edit_book")
        self.cmd_delete_book = QtWidgets.QPushButton(self.centralwidget)
        self.cmd_delete_book.setGeometry(QtCore.QRect(740, 160, 111, 23))
        self.cmd_delete_book.setObjectName("cmd_delete_book")
        self.cmd_add_book = QtWidgets.QPushButton(self.centralwidget)
        self.cmd_add_book.setGeometry(QtCore.QRect(500, 160, 111, 23))
        self.cmd_add_book.setObjectName("cmd_add_book")
        self.cmd_read_book = QtWidgets.QPushButton(self.centralwidget)
        self.cmd_read_book.setGeometry(QtCore.QRect(250, 10, 111, 23))
        self.cmd_read_book.setObjectName("cmd_read_book")
        self.cmb_author = QtWidgets.QComboBox(self.centralwidget)
        self.cmb_author.setGeometry(QtCore.QRect(500, 130, 351, 22))
        self.cmb_author.setEditable(False)
        self.cmb_author.setObjectName("cmb_author")
        self.book_id = QtWidgets.QLineEdit(self.centralwidget)
        self.book_id.setGeometry(QtCore.QRect(500, 40, 351, 21))
        self.book_id.setReadOnly(True)
        self.book_id.setObjectName("book_id")
        self.name = QtWidgets.QLineEdit(self.centralwidget)
        self.name.setGeometry(QtCore.QRect(500, 70, 351, 20))
        self.name.setObjectName("name")
        self.date = QtWidgets.QLineEdit(self.centralwidget)
        self.date.setGeometry(QtCore.QRect(500, 100, 351, 20))
        self.date.setObjectName("date")
        self.book_search = QtWidgets.QLineEdit(self.centralwidget)
        self.book_search.setGeometry(QtCore.QRect(10, 10, 211, 20))
        self.book_search.setObjectName("book_search")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 872, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Библиотека"))
        self.cmd_read_in_notepad.setText(_translate("MainWindow", "В Блокноте"))
        self.cmd_edit_book.setText(_translate("MainWindow", "Редактировать"))
        self.cmd_delete_book.setText(_translate("MainWindow", "Удалить"))
        self.cmd_add_book.setText(_translate("MainWindow", "Добавить"))
        self.cmd_read_book.setText(_translate("MainWindow", "Читать"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
