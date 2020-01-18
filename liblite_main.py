

import sys
import sqlite3
import os.path
import webbrowser


from PyQt5.QtWidgets import QMainWindow, QMessageBox, QApplication, QWidget, QAction, QTableWidget,QTableWidgetItem,QVBoxLayout
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot

import liblite_ui

script_path = (os.path.dirname(os.path.realpath(__file__)))
ui = None

def get_books():
    global lib_con
    cur = lib_con.cursor()
    query = '''
    SELECT b.book_id, b.name, a.author_id, a.name as author_name, a.patronym, a.surname
    FROM books b 
    LEFT JOIN b_athors_books ab 
        on b.book_id = ab.book_id
    LEFT JOIN authors a 
        on ab.author_id = a.author_id
    '''
    return [dict(row) for row in cur.execute(query).fetchall()]

    
def get_book_info(book_id):
    print(book_id)
    if book_id is None:
        return
    res = select('books', {'book_id': book_id})
    if len(res) == 0:
        return None
    else:
        return res[0]

def add_book_info(book_info, author_info = {}, pub_info = {}):
    global lib_con
    cur = lib_con.cursor()
    book_info.keys()
    query = 'INSERT INTO books ({}) VALUES ({});'.format(book_info.keys().join(', '), book_info.join(', '))
    cur.execute(query)
    lib_con.commit()
    return None

def edit_book_info(book_info):
    global lib_con
    cur = lib_con.cursor()
    query = '''
        UPDATE books SET 
        name = '{}',
        date = '{}'
        WHERE book_id = {}
    '''
    cur.execute(query.format(book_info['name'], book_info['date'], book_info['book_id']))
    lib_con.commit()
    return None

def delete_book(book_id):
    global lib_con
    cur = lib_con.cursor()
    query = 'DELETE FROM books WHERE book_id = {};'.format(book_id)
    cur.execute(query)
    lib_con.commit()
    return None

def get_tables():
    return select('sqlite_master', {'type': 'table'})

def select(table_name, key_dict = {}):
    global lib_con
    cur = lib_con.cursor()
    condis_query = ''
    condis = []
    for key, val in key_dict.items():
        condis.append("{}='{}'".format(key, val))
    if len(condis) > 0:
        condis_query = 'where {}'.format(' AND '.join(condis))
    query = 'SELECT * FROM {} {};'.format(table_name, condis_query)
    return [dict(row) for row in cur.execute(query).fetchall()]

def fillTable(table, data: []):
    if len(data) == 0:
        return None
    table.setColumnCount(len(data[0]))
    table.setRowCount(len(data))
    table.setHorizontalHeaderLabels(data[0].keys())
    i = 0
    for row in data:
        j = 0
        for key, val in row.items():
            if i == 0:
                table.horizontalHeaderItem(j).setToolTip(key)
            table.setItem(i,j, QTableWidgetItem(str(val)))
            j+=1
        i+=1
    return None


def showMain():
    global ui
    app = liblite_ui.QtWidgets.QApplication(sys.argv)
    MainWindow = liblite_ui.QtWidgets.QMainWindow()
    ui = liblite_ui.Ui_MainWindow()
    ui.setupUi = setupMainUi(ui.setupUi)
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())


def get_selected_id():
    global ui
    row = ui.lib_table.currentRow()
    if row > -1:
        return ui.lib_table.item(row, 0).text()
    return None
    
def get_selected_info():
    global ui
    row = ui.lib_table.currentRow()
    cols = ui.lib_table.columnCount()
    row_data = []
    for col in range(cols):
        row_data.append(ui.lib_table.item(row, col).text())
    print(row_data)
    return row_data

def fill_book_form(book_id):
    global ui
    book_info = get_book_info(book_id)
    book_info2 = get_selected_info()
    ui.book_id.setText(str(book_info['book_id']))
    ui.name.setText(str(book_info['name']))
    ui.date.setText(str(book_info['date']))
    i = ui.cmb_author.findData(book_info2[2])
    if(i > -1) :
        ui.cmb_author.setCurrentIndex(i)
    else:
        ui.cmb_author.setCurrentIndex(-1)


def get_book_form():
    global ui
    return {
        'book_id': ui.book_id.text(),
        'name': ui.name.text(),
        'date': ui.date.text()
    }


def read_with_notepad(book_id):
    global script_path
    book_info = get_book_info(book_id)
    webbrowser.open('/'.join([script_path, book_info['main_path'], book_info['enter_path']]))

def msgbox(text, buttons = QMessageBox.Ok, fun_ok = None, fun_cancel = None, msg_type = QMessageBox.Information, title = "Внимание!", add_info = None, detailed_info = None):
    msg = QMessageBox()
    msg.setIcon(msg_type) #QMessageBox.Information
    msg.setText(text)
    msg.setWindowTitle(title)
    if add_info is not None:
        msg.setInformativeText(add_info)
    if detailed_info is not None:
        msg.setDetailedText(detailed_info)
    return msg.exec_()

def setupMainUi(setupUi):
    def wrp(MainWindow):
        global ui
        books_data = get_books()
        setupUi(MainWindow)
        ui.lib_table.clicked.connect(lambda x: fill_book_form(get_selected_id()))
        ui.cmd_read_book.clicked.connect(lambda x: msgbox('В разработке'))
        ui.cmd_read_in_notepad.clicked.connect(lambda x: read_with_notepad(get_selected_id()))

        ui.cmd_add_book.clicked.connect(lambda x: msgbox('В разработке'))
        # ui.cmd_edit_book.clicked.connect(lambda x: msgbox('В разработке'))
        ui.cmd_edit_book.clicked.connect(lambda x: edit_book_info(get_book_form()))
        ui.cmd_delete_book.clicked.connect(lambda x: msgbox('В разработке'))
        fillTable(ui.lib_table, books_data)
        ui.authors = select("authors")
        for author in select("authors"):
            ui.cmb_author.addItem(author['name'] + ' ' + author['surname'], author['author_id'])
        ui.cmb_author.setCurrentIndex(-1)
        # ui.cmb_author.currentData()
    return wrp


def drop_tables(tables = None):
    global lib_con
    if tables is None:
        tables = [
            'authors',
            'publishers',
            'books',
            'b_athors_books',
        ]
    drop_query  = 'DROP TABLE IF EXISTS {};'
    cur = lib_con.cursor()
    for table in tables:
        cur.execute(drop_query.format(table))
    lib_con.commit()

def create_tables():
    global lib_con
    cur = lib_con.cursor()
    cur.execute('''
    CREATE TABLE IF NOT EXISTS authors
    (author_id INTEGER PRIMARY KEY, name, patronym, surname, wiki_link);
    ''')
    cur.execute('''
    CREATE TABLE IF NOT EXISTS publishers
    (publisher_id INTEGER PRIMARY KEY, pub_name, link);
    ''')
    cur.execute('''
    CREATE TABLE IF NOT EXISTS books
    (book_id INTEGER PRIMARY KEY, publisher_id, name, main_path, enter_path, date, wiki_link, description);
    ''')
    cur.execute('''
    CREATE TABLE IF NOT EXISTS b_athors_books 
    (book_id INTEGER, author_id INTEGER);
    ''')
    lib_con.commit()
    return None
 

def add_author(name, patronym, surname, wiki_link):
    global lib_con
    cur = lib_con.cursor()
    query = '''
    INSERT INTO authors 
    (name, patronym, surname, wiki_link)
    values
    ('{}', '{}', '{}', '{}')
    '''
    cur.execute(query.format(name, patronym, surname, wiki_link))

def add_book(publisher_id, name, main_path, enter_path, date, wiki_link, description):
    global lib_con
    cur = lib_con.cursor()
    query = '''
    INSERT INTO books 
    (publisher_id, name, main_path, enter_path, date, wiki_link, description)
    values
    ('{}', '{}', '{}', '{}', '{}', '{}', '{}')
    '''
    cur.execute(query.format(publisher_id, name, main_path, enter_path, date, wiki_link, description))

def add_publisher(pub_name, link):
    global lib_con
    cur = lib_con.cursor()
    query = '''
    INSERT INTO publishers 
    (pub_name, link)
    values
    ('{}', '{}')
    '''
    cur.execute(query.format(pub_name, link))

def add_author_book_bind(book_id, author_id):
    global lib_con
    cur = lib_con.cursor()
    query = '''
    INSERT INTO publishers 
    (book_id, author_id)
    values
    ('{}', '{}')
    '''
    cur.execute(query.format(book_id, author_id))

def add_books():
    global lib_con
    cur = lib_con.cursor()
    books = [
        (1, '', 'The Strange Case Of Dr. Jekyll And Mr. Hyde', 'books', 'The Strange Case Of Dr. Jekyll And Mr. Hyde.txt', 'June 25, 2008', '', ''),
        (2, '', 'The Adventures of Sherlock Holmes', 'books', 'The Adventures of Sherlock Holmes.txt', 'November 29, 2002', '', ''),
        (3, '', 'A Christmas Carol A Ghost Story of Christmas', 'books', 'A Christmas Carol A Ghost Story of Christmas.txt', 'November 29, 2002', '', ''),
        (4, '', 'David Copperfield', 'books', 'David Copperfield.txt', 'August 11, 2004', '', ''),
        (5, '', 'Beowolf', 'books', 'Beowolf.txt', 'July 19, 2005', '', '')
    ]
    authors = [
        (1, 'Robert Louis', '', 'Stevenson', ''),
        (2, 'Arthur Conan', '', 'Doyle', ''),
        (3, 'Charles', '', 'Dickens', ''),

    ]
    book_author_binds = [
        (1, 1), 
        (2, 2), 
        (3, 3), 
        (4, 3)
    ] 
    cur.executemany("INSERT INTO books VALUES (?,?,?,?,?,?,?,?)", books)
    cur.executemany("INSERT INTO authors VALUES (?,?,?,?,?)", authors)
    cur.executemany("INSERT INTO b_athors_books VALUES (?,?)", book_author_binds)
    lib_con.commit()
    return None


   
if __name__ == '__main__':
    lib_con = sqlite3.connect("library.db")

    # drop_tables()
    # create_tables()
    # add_books()

    # print(select('books'))

    lib_con = sqlite3.connect(script_path + "/library.db")
    lib_con.row_factory = sqlite3.Row
    # print(get_books())
    # print(get_book_info(1))
    # print(get_tables())
    showMain()
    lib_con.close()