# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'F:\PyScripts\liblite\read_book_ui.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_read_book(object):
    def setupUi(self, read_book):
        read_book.setObjectName("read_book")
        read_book.resize(791, 662)
        self.centralwidget = QtWidgets.QWidget(read_book)
        self.centralwidget.setObjectName("centralwidget")
        self.page = QtWidgets.QTextEdit(self.centralwidget)
        self.page.setGeometry(QtCore.QRect(20, 20, 421, 541))
        self.page.setReadOnly(True)
        self.page.setObjectName("page")
        self.page_num = QtWidgets.QLineEdit(self.centralwidget)
        self.page_num.setGeometry(QtCore.QRect(156, 580, 71, 20))
        self.page_num.setObjectName("page_num")
        self.go_next_page = QtWidgets.QPushButton(self.centralwidget)
        self.go_next_page.setGeometry(QtCore.QRect(246, 580, 31, 23))
        self.go_next_page.setObjectName("go_next_page")
        self.go_prev_page = QtWidgets.QPushButton(self.centralwidget)
        self.go_prev_page.setGeometry(QtCore.QRect(110, 580, 31, 23))
        self.go_prev_page.setObjectName("go_prev_page")
        self.lbl_stat = QtWidgets.QLabel(self.centralwidget)
        self.lbl_stat.setGeometry(QtCore.QRect(500, 20, 191, 21))
        self.lbl_stat.setObjectName("lbl_stat")
        self.book_stat = QtWidgets.QTextEdit(self.centralwidget)
        self.book_stat.setGeometry(QtCore.QRect(490, 40, 251, 201))
        self.book_stat.setReadOnly(True)
        self.book_stat.setObjectName("book_stat")
        read_book.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(read_book)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 791, 21))
        self.menubar.setObjectName("menubar")
        read_book.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(read_book)
        self.statusbar.setObjectName("statusbar")
        read_book.setStatusBar(self.statusbar)

        self.retranslateUi(read_book)
        QtCore.QMetaObject.connectSlotsByName(read_book)

    def retranslateUi(self, read_book):
        _translate = QtCore.QCoreApplication.translate
        read_book.setWindowTitle(_translate("read_book", "MainWindow"))
        self.go_next_page.setText(_translate("read_book", ">"))
        self.go_prev_page.setText(_translate("read_book", "<"))
        self.lbl_stat.setText(_translate("read_book", "Статистика"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    read_book = QtWidgets.QMainWindow()
    ui = Ui_read_book()
    ui.setupUi(read_book)
    read_book.show()
    sys.exit(app.exec_())
