
import sys

from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QApplication, QWidget, QAction, QTableWidget, QTableWidgetItem, QVBoxLayout, QFileDialog

import read_book_ui
from msgbox import msgbox

class book_reader(read_book_ui.Ui_read_book):
    
    # def __init__(self, parent=None):
        
    # def __init__(self, parent=None):
    #     super(book_reader, self).__init__(parent)

    def test(self):
        pass

    def show_page(self, page_num):
        # return None
        print(page_num)
        first_line = (page_num - 1) * self.book_linecount
        last_line = page_num * self.book_linecount
        self.page.setText("\n".join(self.book_lines[first_line:last_line]))
        self.page_num.setText(str(page_num))

    def show_prev(self):
        c_page = int(self.page_num.text())
        self.show_page(c_page-1)
        
    def show_next(self):
        c_page = int(self.page_num.text())
        self.show_page(c_page+1)




def show_reader(book_info, book_path):

    MainWindow = QMainWindow()
    reader = book_reader()
    reader.setupUi(MainWindow)
    
    reader.go_prev_page.clicked.connect(lambda x: reader.show_prev())
    reader.go_next_page.clicked.connect(lambda x: reader.show_next())


    reader.book_info = book_info
    reader.book_path = book_path
    reader.book_linecount = 20
    with open(book_path, 'r') as f:
        reader.book_lines = f.readlines()
    
    reader.show_page(1)

    MainWindow.show()

    return MainWindow

