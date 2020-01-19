"""
module to connect sqlite with main info about books

"""
import os.path
import sqlite3

script_path = (os.path.dirname(os.path.realpath(__file__)))
lib_con = None



def select(table_name: str, key_dict: dict = {}) -> list:
    '''
    select data from sqlite table with optional condis
    
    :param table_name: name of table in sql
    :param key_dict: condis to filter
	:return: query result as list  
    '''
    cur = lib_con.cursor()
    condis_query = ''
    condis = []
    for key, val in key_dict.items():
        condis.append("{}='{}'".format(key, val))
    if len(condis) > 0:
        condis_query = 'where ({})'.format(') AND ('.join(condis))
    query = 'SELECT * FROM {} {};'.format(table_name, condis_query)
    return [dict(row) for row in cur.execute(query).fetchall()]

    
def get_books():
    '''
    select books data for main table
    
	:return: query result as list  
    '''
    # global lib_con
    cur = lib_con.cursor()
    query = '''
    SELECT b.book_id, b.name, b.date, a.author_id, a.name as author_name, a.patronym, a.surname, b.main_path, b.enter_path
    FROM books b 
    LEFT JOIN b_athors_books ab 
        on b.book_id = ab.book_id
    LEFT JOIN authors a 
        on ab.author_id = a.author_id
    '''
    return [dict(row) for row in cur.execute(query).fetchall()]


def get_book_info(book_id) -> any:
    '''
    select main book info by id
    
    :param book_id: id of book to select
	:return: book_info on Nothing if not found
    '''
    print(book_id)
    if book_id is None:
        return
    res = select('books', {'book_id': book_id})
    if len(res) == 0:
        return None
    else:
        return res[0]

        
def add_book_info(book_info: dict, author_info: dict = {}, pub_info: dict = {}) -> None:
    '''
    add book info to sql
    
    :param book_info: book info to insert
    :param author_info: author info to insert
    :param pub_info: publisher info to insert
	:return: Nothing
    '''
    cur = lib_con.cursor()
    book_info.keys()
    query = 'INSERT INTO books ({}) VALUES ({});'.format(book_info.keys().join(', '), book_info.join(', '))
    cur.execute(query)
    lib_con.commit()
    return None


def edit_book_info(book_info: dict) -> None:
    '''
    add book info to sql
    
    :param book_info: book info to update
	:return: Nothing
    '''
    cur = lib_con.cursor()
    query = '''
        UPDATE books SET 
        publisher_id = '{}',
        name = '{}',
        main_path = '{}',
        enter_path = '{}',
        date = '{}',
        wiki_link = '{}',
        description = '{}'
        WHERE book_id = {}
    '''
    cur.execute(query.format(book_info['publisher_id'], book_info['name'], book_info['main_path'], book_info['enter_path'], book_info['date'], book_info['wiki_link'], book_info['description'], book_info['book_id']))
    lib_con.commit()
    return None


def delete_book(book_id: int) -> None:
    '''
    delete book info from sql
    
    :param book_id: book info to update
	:return: Nothing
    '''
    cur = lib_con.cursor()
    query = 'DELETE FROM books WHERE book_id = {};'.format(book_id)
    cur.execute(query)
    lib_con.commit()
    return None


def drop_tables(tables: list = None) -> None:
    '''
    delete book info from sql
    
    :param book_id: optional list of table
	:return: Nothing
    '''
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
    return None

def create_tables() -> None:
    '''
    create main table in sqlite

	:return: Nothing
    '''
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

def get_tables() -> list:
    '''
    get info about sql tables
    
	:return: list of table infos
    '''
    return select('sqlite_master', {'type': 'table'})

def add_books() -> None:
    '''
    add base book infos

	:return: Nothing
    '''
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
        (3, 'Charles', '', 'Dickens', '')
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


def add_author(name: str, patronym: str, surname: str, wiki_link: str) -> None:
    '''
    add author
    
    :param name: author name
    :param patronym: author patronym
    :param surname: author surname
    :param wiki_link: author wiki_link
	:return: Nothing
    '''
    cur = lib_con.cursor()
    query = '''
    INSERT INTO authors 
    (name, patronym, surname, wiki_link)
    values
    ('{}', '{}', '{}', '{}')
    '''
    cur.execute(query.format(name, patronym, surname, wiki_link))
    return None

def add_book(publisher_id: str, name: str, main_path: str, enter_path: str, date: str, wiki_link: str, description: str) -> None:
    '''
    add book
    
    :param publisher_id: book publisher_id
    :param name: book name
    :param main_path: book main_path
    :param enter_path: book enter_path
    :param date: book date
    :param wiki_link: book wiki_link
    :param description: book description
	:return: Nothing
    '''
    cur = lib_con.cursor()
    query = '''
    INSERT INTO books 
    (publisher_id, name, main_path, enter_path, date, wiki_link, description)
    values
    ('{}', '{}', '{}', '{}', '{}', '{}', '{}')
    '''
    cur.execute(query.format(publisher_id, name, main_path, enter_path, date, wiki_link, description))
    lib_con.commit()
    return None

def add_publisher(pub_name: str, link: str) -> None:
    '''
    add publisher
    
    :param pub_name: publisher pub_name
    :param link: publisher link
	:return: Nothing
    '''
    cur = lib_con.cursor()
    query = '''
    INSERT INTO publishers 
    (pub_name, link)
    values
    ('{}', '{}')
    '''
    cur.execute(query.format(pub_name, link))
    return None

def add_author_book_bind(book_id: int, author_id: int) -> None:
    '''
    add author book bind
    
    :param book_id: book_id
    :param author_id: author_id
	:return: Nothing
    '''
    cur = lib_con.cursor()
    query = '''
    INSERT INTO publishers 
    (book_id, author_id)
    values
    ('{}', '{}')
    '''
    cur.execute(query.format(book_id, author_id))
    return None


def connect():
    '''
    create sql connection
    
	:return: Nothing
    '''
    global lib_con
    lib_con = sqlite3.connect("library.db")
    lib_con.row_factory = sqlite3.Row

def close():
    lib_con.close()



if __name__ == '__main__':

    # drop_tables()
    # create_tables()
    # add_books()

    # print(select('books'))

    lib_con = sqlite3.connect(script_path + "/library.db")
    lib_con.row_factory = sqlite3.Row
    # print(get_books())
    # print(get_book_info(1))
    # print(get_tables())
    