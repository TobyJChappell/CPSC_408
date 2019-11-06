import pymysql
import sqlite3
import pandas as pd

def create_mysql_connection(db_user, db_password, host_name, db_name):

    conn = None

    try:
        conn = pymysql.connect(user=db_user, password=db_password, host=host_name, db=db_name)
    except:
        print('connection failed')

    return conn

def create_sqlite_connection(db_filename):

    conn = None

    try:
        conn = sqlite3.connect(db_filename)
    except:
        print('connection failed')

    return conn

def main():

    # ------------------------------------
    # SQLite
    # ------------------------------------

    # create SQLite connection and cursor
    sqlite_conn = create_sqlite_connection('/Users/tobychappell/Documents/CPSC_Courses/CPSC_408/Lab_4/toby_chappell_lab4.db')
    sqlite_cur = sqlite_conn.cursor()

    # INSERT statement
    insert_sql = '''INSERT INTO Bakery_Goods(item_id, flavor, food, price)
                         VALUES (?,?,?,?)'''

    insert_vals = ('1', 'Strawberry', 'Ice Cream', 10.50)

    sqlite_cur.execute(insert_sql, insert_vals)

    # UPDATE statement
    update_sql = '''UPDATE Bakery_Goods
                       SET flavor = ?
                     WHERE item_id = ?
                 '''

    update_vals = ('Vanilla', '1')

    sqlite_cur.execute(update_sql, update_vals)

    # SELECT statement
    sqlite_cur.execute('SELECT * FROM Bakery_Goods;')

    result = sqlite_cur.fetchall()

    for row in result:
        print(row)

    # Load DB to pandas for analysis
    sqlite_pandas = pd.read_sql('SELECT * FROM Bakery_Goods;', con=sqlite_conn)

    print(sqlite_pandas.head())

    # ------------------------------------
    # MySQL
    # ------------------------------------

    # create MySQL connection and cursor
    mysql_conn = create_mysql_connection(db_user='root', db_password='1Secret1', host_name='34.68.212.129', db_name='banking_app')
    mysql_cur = mysql_conn.cursor()

    mysql_cur.execute('SELECT * FROM test_table;')
    result = mysql_cur.fetchall()

    for row in result:
        print(row)

    # Load DB to pandas for analysis
    mysql_pandas = pd.read_sql('SELECT * FROM test_table;', con=mysql_conn)

    print(mysql_pandas.head())


if __name__ == '__main__':
    main()
