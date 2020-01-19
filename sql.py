
import os.path
import sqlite3

script_path = (os.path.dirname(os.path.realpath(__file__)))
lib_con = None



def select(table_name, key_dict = {}):
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
    cur = lib_con.cursor()
    book_info.keys()
    query = 'INSERT INTO books ({}) VALUES ({});'.format(book_info.keys().join(', '), book_info.join(', '))
    cur.execute(query)
    lib_con.commit()
    return None


def edit_book_info(book_info):
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


def delete_book(book_id):
    cur = lib_con.cursor()
    query = 'DELETE FROM books WHERE book_id = {};'.format(book_id)
    cur.execute(query)
    lib_con.commit()
    return None


def drop_tables(tables = None):
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

def get_tables():
    return select('sqlite_master', {'type': 'table'})

def add_books():
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


def add_author(name, patronym, surname, wiki_link):
    cur = lib_con.cursor()
    query = '''
    INSERT INTO authors 
    (name, patronym, surname, wiki_link)
    values
    ('{}', '{}', '{}', '{}')
    '''
    cur.execute(query.format(name, patronym, surname, wiki_link))

def add_book(publisher_id, name, main_path, enter_path, date, wiki_link, description):
    cur = lib_con.cursor()
    query = '''
    INSERT INTO books 
    (publisher_id, name, main_path, enter_path, date, wiki_link, description)
    values
    ('{}', '{}', '{}', '{}', '{}', '{}', '{}')
    '''
    cur.execute(query.format(publisher_id, name, main_path, enter_path, date, wiki_link, description))
    lib_con.commit()

def add_publisher(pub_name, link):
    cur = lib_con.cursor()
    query = '''
    INSERT INTO publishers 
    (pub_name, link)
    values
    ('{}', '{}')
    '''
    cur.execute(query.format(pub_name, link))

def add_author_book_bind(book_id, author_id):
    cur = lib_con.cursor()
    query = '''
    INSERT INTO publishers 
    (book_id, author_id)
    values
    ('{}', '{}')
    '''
    cur.execute(query.format(book_id, author_id))


def connect():
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
    