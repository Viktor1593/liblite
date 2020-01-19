
import sys
import json
import re

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


    def get_stat(self, book_lines):
        l_count = len(book_lines)
        data = {
            'pages': l_count // self.book_linecount,
            'lines': l_count,
            'words': 0
        }
        word_mask = re.compile(r'\w+')
        words = {}
        # skip_words = ['the', 'to', 'of', 'a', 'r', 'i', 'in', 'that', 'it', 'you', 'he', 'was', 'and', 'his', 'with', 's', 'as', 'for', 'said', 'had', 'not', 'him']
        skip_words = []
        # i = 0
        for line in book_lines:
            l_words = re.findall(word_mask, line)
            if l_words is None:
                continue
            data['words'] += len(l_words)
            for word in l_words:
                word = word.lower()
                if word in skip_words:
                    continue
                if word not in words:
                    words[word] = 1
                else:
                    words[word] += 1
            # i+=1
            # if i > 25:
            #     break
            
        words = {k: v for k, v in sorted(words.items(), key=lambda item: item[1], reverse = True)}
        top_popular = {}
        i = 0
        for key, val in words.items():
            top_popular[key] = words[key]
            i+= 1
            if i > 10:
                break
        data['top_popular'] = top_popular
        # print(words)
        self.book_stat.setText(json.dumps(data, indent=4))



def show_reader(book_info, book_path):

    MainWindow = QMainWindow()
    reader = book_reader()
    reader.setupUi(MainWindow)
    
    reader.go_prev_page.clicked.connect(lambda x: reader.show_prev())
    reader.go_next_page.clicked.connect(lambda x: reader.show_next())


    reader.book_info = book_info
    reader.book_path = book_path
    reader.book_linecount = 20
    with open(book_path, 'r', encoding = 'utf-8') as f:
        reader.book_lines = f.readlines()
    
    reader.show_page(1)
    reader.get_stat(reader.book_lines)
    MainWindow.show()

    return MainWindow

