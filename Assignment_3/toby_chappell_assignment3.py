"""
PRAGMA foreign_keys = ON;

CREATE TABLE Customer(
	customer_id INT PRIMARY KEY,
	ssn INT,
	first_name VARCHAR(20),
	last_name VARCHAR(20));

CREATE TABLE Account_xref(
	customer_id INT,
	account_num INT,
	FOREIGN KEY (customer_id) REFERENCES Customer(customer_id)
	ON UPDATE CASCADE
	ON DELETE CASCADE
	FOREIGN KEY (account_num) REFERENCES Account(account_num)
	ON UPDATE CASCADE
	ON DELETE CASCADE);

CREATE TABLE Account(
	account_num INT PRIMARY KEY,
	account_type VARCHAR(20),
	balance FLOAT(2));

CREATE TABLE Transaction_log(
	time_stamp TIMESTAMP,
	trans_id INT,
	account_num INT,
	trans_type VARCHAR(20),
	trans_amount FLOAT(2)
	FOREIGN KEY (account_num) REFERENCES Account(account_num)
	ON UPDATE NO ACTION
	ON DELETE NO ACTION);
"""

import pymysql
import pandas
import random

def main():
	mysql_conn =  create_mysql_connection(db_user='root', db_password='1Secret1', host_name='34.68.212.129', db_name='banking_app')
	mysql_cur = mysql_conn.cursor()
	selection = 1
	prompt = """Hello, welcome to BanksRUs! You can do the following:
	1. New Customer
	2. Create Account
	3. Check Balance
	4. Deposit Money
	5. Withdraw Money
	6. Transfer Money
	7. Quit
Please select an option: """

	while selection != 7:
		selection = check_choice(input(prompt))
		if selection == 1:
			add_customer(mysql_conn, mysql_cur)
		elif selection == 2:
			create_account(mysql_conn, mysql_cur)
		elif selection == 3:
			check_balance(mysql_conn, mysql_cur)
		elif selection == 4:
			deposit_money(mysql_conn, mysql_cur)
		elif selection == 5:
			withdraw_money(mysql_conn, mysql_cur)
		elif selection == 6:
			transfer_money(mysql_conn, mysql_cur)
	print("Have a nice day!")

# Add customer to database
# @param mysql_cur
# @param mysql_conn
def add_customer(mysql_conn, mysql_cur):
	customer_ids = pandas.read_sql('SELECT customer_id FROM Customer;', con=mysql_conn)
	id = check_customer_random(input("Customer ID: "), customer_ids)
	ssn = check_int(input("Social Security Number: "))
	fn = input("First Name: ")
	ln = input("Last Name: ")
	insert_sql = '''INSERT INTO Customer VALUES(?, ?, ?, ?)'''
	insert_vals = (id, ssn, fn, ln)
	mysql_cur.execute(insert_sql, insert_vals)

# Add account provided customer_id
# @param mysql_cur
# @param mysql_conn
def create_account(mysql_conn, mysql_cur):
	id = check_customer_user(input("Customer ID: "))
	account_nums = pandas.read_sql('SELECT customer_id FROM Customer;', con=mysql_conn)
	num = check_account_random(random.randint(1, 9999), account_nums)
	type = check_type(input("Account Type: "))
	balance = check_float(input("Balance: "))
	insert_ref_sql = '''INSERT INTO Account_xref VALUES(?, ?)'''
	insert_ref_vals = (id, num)
	sqlite_cur.execute(insert_ref_sql, insert_ref_vals)
	insert_account_sql = '''INSERT INTO Account VALUES(?, ?, ?)'''
	insert_account_vals = (num, type, balance)
	mysql_cur.execute(insert_account_sql, insert_account_vals)

# Outputs balance for every account of customer
# @param mysql_cur
def check_balance(mysql_conn, mysql_cur):
	id = check_customer_user(input("Customer ID: "))
	retrieve_sql = '''SELECT a.account_type, a.balance
						FROM Customer AS c
						LEFT JOIN Account_xref AS r ON c.customer_id == r.customer_id
						LEFT JOIN Account AS a ON r.account_num == a.account_num
						WHERE Customer = ?'''
	retrieve_vals = (id)
	mysql_cur.execute(retrieve_sql, retrieve_vals)
	result = mysql_cur.fetchall()
	for row in result:
		print(row)

# Deposit money into an account given customer_id, account_num, and amount to deposit
# @param mysql_cur
def deposit_money(mysql_conn, mysql_cur):
	id = check_customer_user(input("Customer ID: "))
	account = check_account_user(input("Account Number: "), id)
	amount = check_int(input("Amount to Deposit: "))
	update_sql = '''UPDATE Account
					SET balance = balance + ?
					WHERE account_num = ?'''
	update_vals = (amount, account)
	mysql_cur.execute(update_sql, update_vals)

# Withdraw money into an account given customer_id, account_num, and amount to withdraw
# @param mysql_cur
def withdraw_money(mysql_conn, mysql_cur):
	id = check_customer_user(input("Customer ID: "))
	account = check_account_user(input("Account Number: "), id)
	retrieve_sql = '''SELECT balance
						FROM Account
						WHERE account_num = ?'''
	retrieve_vals = (account)
	mysql_cur.execute(retrieve_sql, retrieve_vals)
	balance = 1 #sql statement
	amount = check_withdraw(input("Amount to Withdraw: "), balance)
	update_sql = '''UPDATE Account
                	SET balance = balance - ?
                	WHERE account_num = ?'''
	update_vals = (amount, account)
	mysql_cur.execute(update_sql, update_vals)

# Transfer money between two accounts account given customer_id, 2 account_num's, and amount to deposit/withdraw
# @param mysql_cur
def transfer_money(mysql_conn, mysql_cur):
	id = check_customer_user(input("Customer ID: "))
	account_w = check_account_user(input("Account Number to Withdraw: "), id)
	account_d = check_account_user(input("Account Number to Deposit: "), id)
	retrieve_sql = '''SELECT balance
						FROM Account
						WHERE account_num = ?'''
	retrieve_vals = (account)
	mysql_cur.execute(retrieve_sql, retrieve_vals)
	balance = 1 #sql statement
	amount = check_withdraw(input("Amount to withdraw: "), balance)
	update_withdraw_sql = '''UPDATE Account
								SET balance = balance - ?
                     			WHERE account_num = ?'''
	update_withdraw_vals = (amount, account_w)
	mysql_cur.execute(update_withdraw_sql, update_withdraw_vals)
	update_deposit_sql = '''UPDATE Account
							SET balance = balance + ?
                     		WHERE account_num = ?'''
	update_deposit_vals = (amount, account_d)
	mysql_cur.execute(update_deposit_sql, update_deposit_vals)

# Checks if selection is valid
# @param c Selection
# @return c Valid selction
def check_choice(c):
	while not c.isdigit() or int(c) > 7 or int(c) < 1:
		c = input("Please input a valid option (1-7): ")
	return int(c)

# Makes sure that randomly generated customer id doesn't exist
# @param c Randomly generated customer id
# @return c Valid customer id
def check_customer_random(c, ids):
	while c in ids:
		c = random.randint(1, 9999)
	return c

# Checks if user inputted account number is valid
# @param c Customer ID
# @return c Valid customer id
def check_customer_user(c):
	while not c.isdigit(): #check if customer id exists
		c = input("Please input a valid integer (greater than 0): ")
	return int(c)

# Makes sure that randomly generated account number doesn't exist
# @param a Randomly generated account number
# @return a Valid account num
def check_account_random(a, nums):
	while a in nums:
		a = random.randint(1, 9999)
	return a

# Checks if user inputted account number is valid and belongs to that customer
# @param a Account Number
# @param c Customer ID
# @return a Valid account num
def check_account_user(a, c):
	while not a.isdigit(): #check if account number exists and belongs to customer
		a = input("Please input a valid integer (greater than 0): ")
	return int(a)

# Checks if account type is valid
# t Account Type
# @return t Valid account type
def check_type(t):
	while t != "checking" and t != "savings":
		t = input("Please input a valid type (checking, savings): ")
	return t

# Checks to make sure transaction is valid (greater than balance in account)
# w Withdraw amount
# b Balance
# @return w Valid withdraw amouont
def check_withdraw(w, b):
	while not w.isdigit() or int(w) < b:
		w = input("Please input a valid amount (greater than or equal to ", b, ": ")
	return int(w)

# Checks to make sure value is an integer
# i Integer
# @return i Valid int
def check_int(i):
	while not i.isdigit() or int(i) < 0:
		i = input("Please input a valid integer (greater than or equal to 0): ")
	return int(i)

# Creates connection with MySQL server
# @param db_user Username
# @param db_password Password
# @param host_name Server IP Address
# @param db_name Name of Database
# @return conn MySQL Connection
def create_mysql_connection(db_user, db_password, host_name, db_name):
    conn = None
    try:
        conn = pymysql.connect(user=db_user, password=db_password, host=host_name, db=db_name)
    except:
        print('connection failed')
    return conn

if __name__== "__main__":
	main()
