'''
    main module of liblite
'''

import sys
import os.path
import webbrowser
import ntpath
import shutil
import itertools

import PyQt5.QtWidgets as QW

import liblite_ui
import lib_read
import sql
from msgbox import msgbox

script_path = (os.path.dirname(os.path.realpath(__file__)))
ui = None

def edit_book_info(book_info: dict) -> None:
    '''
    edit book in sqlite and update table
    
    :param book_info: book params to edit
	:return: Nothing    
    '''
    sql.edit_book_info(book_info)
    update_book_table()
    return None


def delete_book(book_id: int) -> None:
    '''
    delete book in sqlite and update table
    
    :param book_id: id of book to delete
	:return: Nothing    
    '''
    sql.delete_book(book_id)
    update_book_table()
    clear_form()
    return None


def update_book_table() -> None:
    '''
    update book in sqlite and update table
    
    :param book_info: book params to edit
	:return: Nothing    
    '''
    # global ui
    ui.lib_table.clear()
    ui.lib_table.t_data = sql.get_books()
    books_data = filter_books_data(ui.lib_table.t_data)
    fillTable(ui.lib_table, books_data)
    return None


def filter_table() -> None:
    '''
    filter table and update table
    
	:return: Nothing    
    '''
    ui.lib_table.clear()
    books_data = filter_books_data(ui.lib_table.t_data)
    # print(books_data)
    fillTable(ui.lib_table, books_data)
    return None

def filter_books_data(books_data: list) -> list:
    '''
    tooks table data and apply filter on it
    
    :param books_data: list of book infos
	:return: filtered books_data    
    '''
    text = ui.book_search.text().lower()
    if len(text) == 0:
        return books_data
    return list(filter(lambda x: find_in_row(x, text), books_data))

def find_in_row(book_info: dict, text: str) -> bool:
    '''
    search filter text in book info
    
    :param row: dict of book info
    :param text: searching string
	:return: True if found, False if not   
    '''
    print(book_info)
    for _, val in book_info.items():
        if str(val).lower().find(text) != -1:
            return True
    return False


def fillTable(table, data = []) -> None:
    '''
    fill table with data 
    
    :param table: table to be filled
    :param data: data to fill table with
	:return: Nothing 
    '''
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
            table.setItem(i,j, QW.QTableWidgetItem(str(val)))
            j+=1
        i+=1
    return None



def get_selected_id() -> any:
    '''
    get id from selected table row
    
	:return: book_id 
    '''
    row = ui.lib_table.currentRow()
    if row > -1:
        return ui.lib_table.item(row, 0).text()
    return None
    
def get_selected_info():
    '''
    get selected book_info
    
	:return: book_info 
    '''
    row = ui.lib_table.currentRow()
    if row == -1:
        return None
    cols = ui.lib_table.columnCount()
    row_data = {}
    for col in range(cols):
        row_data[ui.lib_table.horizontalHeaderItem(col).text()] = ui.lib_table.item(row, col).text()
    print(row_data)
    return row_data


def fill_book_form(book_info: dict) -> None:
    '''
    fill fields with book_info
    
    :param book_info: data to fill form with
	:return: Nothing 
    '''
    if book_info is None:
        clear_form()
        return None
    ui.book_id.setText(str(book_info['book_id']))
    ui.name.setText(str(book_info['name']))
    ui.date.setText(str(book_info['date']))
    ui.book_path.setText(build_path(book_info))
    i = ui.cmb_author.findData(book_info['author_id'])
    if(i > -1) :
        ui.cmb_author.setCurrentIndex(i)
    else:
        ui.cmb_author.setCurrentIndex(-1)
    return None

def clear_form() -> None:
    '''
    fill fields with book_info
    
    :param table: table to be filled
    :param data: data to fill table with
	:return: Nothing 
    '''
    ui.book_id.setText('')
    ui.name.setText('')
    ui.date.setText('')
    ui.book_path.setText('')
    ui.cmb_author.setCurrentIndex(-1)
    return None


def get_book_form() -> dict:
    '''
    get data from form
    
	:return: book_info 
    '''
    return {
        'book_id': ui.book_id.text(),
        'publisher_id': '', 
        'name': ui.name.text(), 
        'main_path': 'books', 
        'enter_path': ntpath.basename(ui.book_path.text()), 
        'date': ui.date.text(), 
        'wiki_link': '', 
        'description':  ''
    }


def read_with_notepad(book_info: dict) -> None:
    '''
    open book in notepad
    
    :param book_info: book_info with file path data
	:return: Nothing 
    '''
    if book_info is None:
        return None
    webbrowser.open(build_path(book_info))


def read_book(book_info: dict) -> None:
    '''
    open book in lib_read
    
    :param book_info: book_info with file path data
	:return: Nothing 
    '''
    if book_info is None:
        return
    book_path = build_path(book_info)
    reader = lib_read.show_reader(book_info, book_path)
    ui.book_readers.append(reader)


def showMain() -> None:
    '''
    open main liblite window
    
	:return: Nothing 
    '''
    global ui
    app = liblite_ui.QtWidgets.QApplication(sys.argv)
    MainWindow = liblite_ui.QtWidgets.QMainWindow()
    ui = liblite_ui.Ui_MainWindow()
    ui.setupUi = setupMainUi(ui.setupUi) ## decorator for fun
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
    return None

def setupMainUi(setupUi):
    '''
    decorator for setup ui
    
    :param setupUi: setup function to decorate
	:return: wraper 
    '''
    def wrp(MainWindow):
        setupUi(MainWindow)

        ui.book_search.textChanged.connect(filter_table)
        ui.lib_table.clicked.connect(lambda x: fill_book_form(get_selected_info()))

        ui.cmd_read_book.clicked.connect(lambda x: read_book(get_selected_info()))
        ui.cmd_read_in_notepad.clicked.connect(lambda x: read_with_notepad(get_selected_info()))

        ui.cmd_add_book.clicked.connect(show_add_book_dialog)
        ui.cmd_edit_book.clicked.connect(lambda x: edit_book_info(get_book_form()))
        ui.cmd_delete_book.clicked.connect(lambda x: delete_book(get_selected_id()))
        update_book_table()

        for author in sql.select("authors"):
            ui.cmb_author.addItem(author['name'] + ' ' + author['surname'], author['author_id'])
        ui.cmb_author.setCurrentIndex(-1)

        ui.book_readers = list()
        # ui.cmb_author.currentData()
    return wrp

def show_add_book_dialog() -> any:
    '''
    display QFileDialog
    take filepath, parse it for main fields and add to catalog
    
	:return: Nothing 
    '''
    file_name, _ = QW.QFileDialog.getOpenFileName(None, 'Select book text file', '', 'Text Files (*.txt)' )
    if file_name:
        book_info = {
            'book_id': '',
            'publisher_id': '', 
            'name': '', 
            'main_path': 'books', 
            'enter_path': ntpath.basename(file_name), 
            'date': '', 
            'wiki_link': '', 
            'description':  '',
            'author_id': ''
        }
        with open(file_name, 'r') as f:
            try:
                for line in f:
                    if ':' in line:
                        ar = line.split(':')
                        key = ar[0].strip()
                        if key == 'Author':
                            pass
                        elif key == 'Title':
                            book_info['name'] = ':'.join(ar[1:]).strip()
                            book_info['enter_path'] = book_info['name'] + '.txt'
                        elif key == 'Release Date':
                            book_info['date'] = ':'.join(ar[1:]).strip()
            except Exception:
                pass
        sql.add_book(book_info['publisher_id'], book_info['name'], book_info['main_path'], \
            book_info['enter_path'], book_info['date'], book_info['wiki_link'], book_info['description'])     
        update_book_table()
        shutil.copyfile(file_name, build_path(book_info))   
        fill_book_form(book_info)

def build_path(book_info: dict) -> str:
    '''
    build path to book file
    
    :param book_info: provider of book path info
	:return: book file_path 
    '''
    return '\\'.join([script_path, book_info['main_path'], book_info['enter_path']])

   
if __name__ == '__main__':
    sql.connect()
    showMain()
    sql.close()
