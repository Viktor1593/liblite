
import sys
import json
import re

from PyQt5 import QtGui, QtCore
import PyQt5.QtWidgets as QW

import read_book_ui
from msgbox import msgbox

class book_reader(read_book_ui.Ui_read_book):
    
    # def __init__(self, parent=None):
        
    # def __init__(self, parent=None):
    #     super(book_reader, self).__init__(parent)
    
    def show_page(self, page_num):
        # return None

        page_num = self.correct_page(page_num)
        first_line = (page_num - 1) * self.book_linecount
        last_line = page_num * self.book_linecount
        self.page.setText("\n".join(self.book_lines[first_line:last_line]))
        self.page_num.setText(str(page_num))
    
    def correct_page(self, page_num):
        if page_num < 1:
            page_num = abs(page_num)
            page_num = page_num % self.book_pagecount
            page_num = self.book_pagecount - page_num
        elif page_num > self.book_pagecount:
            page_num = page_num % self.book_pagecount
        return page_num


    def show_prev(self):
        c_page = int(self.page_num.text())
        self.show_page(c_page-1)
        
    def show_next(self):
        c_page = int(self.page_num.text())
        self.show_page(c_page+1)


    def get_stat(self, book_lines):
        l_count = len(book_lines)
        data = {
            'pages': self.book_pagecount,
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
        for key, _ in words.items():
            top_popular[key] = words[key]
            i+= 1
            if i > 10:
                break
        data['top_popular'] = top_popular
        # print(words)
        self.book_stat.setText(json.dumps(data, indent=4))


    def search_text(self):
        text = self.search_in_book.text()
        self.search_res.clear()
        if len(text) < 3:
            return
        if self.is_regular.isChecked():
            try:
                text = re.compile(text)
            except Exception:
                return
        else:
             text = text.lower()
        self.found = []
        for i, item in enumerate(self.book_lines):
            if self.line_match(item, text):
                self.found.append((i, item))
                self.search_res.addItem(item)
        print(self.found)
        
    def line_match(self, line, text):
        if self.is_regular.isChecked():
            return re.search(text, line)
        else:
            return line.lower().find(text) != -1

    def search_res_onclick(self):
        text = self.search_res.currentItem().text()
        items = list(filter(lambda x: x[1] == text, self.found))
        print(items)
        if len(items) > 0:
            self.show_page_by_line(items[0][0])

    def show_page_by_line(self, line_index):
        page = line_index // self.book_linecount
        if line_index % self.book_linecount > 0:
            page+=1
        self.show_page(page)





def show_reader(book_info, book_path):

    MainWindow = QW.QMainWindow()

    reader = book_reader()
    reader.setupUi(MainWindow)

    MainWindow.setWindowTitle(book_info['name'])

    reader.search_in_book.textChanged.connect(lambda x: reader.search_text())
    reader.search_res.clicked.connect(lambda x: reader.search_res_onclick())
    
    reader.go_prev_page.clicked.connect(lambda x: reader.show_prev())
    reader.go_next_page.clicked.connect(lambda x: reader.show_next())

    reader.book_info = book_info
    reader.book_path = book_path
    reader.book_linecount = 20
    with open(book_path, 'r', encoding = 'utf-8') as f:
        reader.book_lines = f.readlines()
    
    reader.book_pagecount =  len(reader.book_lines) // reader.book_linecount
    if len(reader.book_lines) % reader.book_linecount > 0:
        reader.book_pagecount += 1
    reader.show_page(1)
    reader.get_stat(reader.book_lines)
    MainWindow.show()

    return MainWindow

