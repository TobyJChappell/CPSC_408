# author: Toby Chappell
# date: 11/20/19
# assignment: Assignment 3

import pymysql
import pandas
import random
from datetime import datetime

def main():
	mysql_conn = create_mysql_connection(db_user='root', db_password='1Secret1', host_name='34.68.212.129', db_name='banking_app')
	mysql_cur = mysql_conn.cursor()
	selection = 1
	prompt = """\nHello, welcome to BanksRUs! You can do the following:
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
		if selection == 7:
			break
		elif selection == 1:
			add_customer(mysql_conn, mysql_cur)
		elif get_ids(mysql_conn).size == 0:
			print("No customers listed in database, please select option 1")
		else:
			if selection == 2:
				create_account(mysql_conn, mysql_cur, id=-1)
			elif selection == 3:
				check_balance(mysql_conn, mysql_cur)
			elif selection == 4:
				deposit_money(mysql_conn, mysql_cur)
			elif selection == 5:
				withdraw_money(mysql_conn, mysql_cur)
			elif selection == 6:
				transfer_money(mysql_conn, mysql_cur)
	print("Have a nice day!\n")
	mysql_cur.close()
	mysql_conn.close()

# Add customer to database
# @param mysql_cur
# @param mysql_conn
def add_customer(mysql_conn, mysql_cur):
	id = check_customer_random(random.randint(1, 9999), get_ids(mysql_conn))
	ssn = check_int(input("Social Security Number: "))
	fn = input("First Name: ").lower().capitalize()
	ln = input("Last Name: ").lower().capitalize()
	insert_sql = 'INSERT INTO Customer VALUES(%s, %s, %s, %s)'
	insert_vals = (id, ssn, fn, ln)
	mysql_cur.execute(insert_sql, insert_vals)
	print("Your Customer Id is: ", id)
	print("Please add an account to associate with your id")
	create_account(mysql_conn, mysql_cur, id)

# Add account provided customer_id
# @param mysql_cur
# @param mysql_conn
# @param id -1 if customer already has an account
def create_account(mysql_conn, mysql_cur, id):
	if id == -1:
		id = check_customer_user(input("Customer ID: "), get_ids(mysql_conn))
	num = check_account_random(random.randint(1, 9999), get_nums(mysql_conn))
	type = check_type(input("Account Type: "))
	balance = check_float(input("Balance: "))
	insert_account_sql = 'INSERT INTO Account VALUES(%s, %s, %s)'
	insert_account_vals = (num, type, balance)
	mysql_cur.execute(insert_account_sql, insert_account_vals)
	insert_ref_sql = 'INSERT INTO Account_xref VALUES(%s, %s)'
	insert_ref_vals = (id, num)
	mysql_cur.execute(insert_ref_sql, insert_ref_vals)
	print("Your Account Id is: ", num)

# Outputs balance for every account of customer
# @param mysql_cur
def check_balance(mysql_conn, mysql_cur):
	id = check_customer_user(input("Customer ID: "), get_ids(mysql_conn))
	retrieve_sql = '''SELECT a.account_num, a.account_type, a.balance
						FROM Customer AS c
						LEFT JOIN Account_xref AS r ON c.customer_id = r.customer_id
						LEFT JOIN Account AS a ON r.account_num = a.account_num
						WHERE c.customer_id = %s'''
	retrieve_vals = (id)
	mysql_cur.execute(retrieve_sql, retrieve_vals)
	result = mysql_cur.fetchall()
	for row in result:
		print(row)

# Deposit money into an account given customer_id, account_num, and amount to deposit
# @param mysql_cur
def deposit_money(mysql_conn, mysql_cur):
	id = check_customer_user(input("Customer ID: "), get_ids(mysql_conn))
	account = check_account_user(input("Account Number: "), get_nums_from_id(id, mysql_conn))
	amount = check_int(input("Amount to Deposit: "))
	update_sql = '''UPDATE Account
					SET balance = balance + %s
					WHERE account_num = %s'''
	update_vals = (amount, account)
	mysql_cur.execute(update_sql, update_vals)
	insert_log(mysql_cur, datetime.now(), id, account, 'Deposit', amount)

# Withdraw money into an account given customer_id, account_num, and amount to withdraw
# @param mysql_cur
def withdraw_money(mysql_conn, mysql_cur):
	id = check_customer_user(input("Customer ID: "), get_ids(mysql_conn))
	account = check_account_user(input("Account Number: "), get_nums_from_id(id, mysql_conn))
	retrieve_sql = '''SELECT balance
						FROM Account
						WHERE account_num = %s'''%account
	balance = pandas.read_sql(retrieve_sql, con=mysql_conn).values.item(0)
	if balance == 0:
		print("Sorry, no money in this account to withdraw.")
		return
	amount = check_withdraw(input("Amount to Withdraw: "), balance)
	update_sql = '''UPDATE Account
                	SET balance = balance - %s
                	WHERE account_num = %s'''
	update_vals = (amount, account)
	mysql_cur.execute(update_sql, update_vals)
	insert_log(mysql_cur, datetime.now(), id, account, 'Withdraw', amount)

# Transfer money between two accounts account given customer_id, 2 account_num's, and amount to deposit/withdraw
# @param mysql_cur
def transfer_money(mysql_conn, mysql_cur):
	id = check_customer_user(input("Customer ID: "), get_ids(mysql_conn))
	retrieve_sql = '''SELECT COUNT(account_num)
						FROM Account_xref
						WHERE customer_id = %s'''%id
	number_of_accounts = pandas.read_sql(retrieve_sql, con=mysql_conn).values.item(0)
	if number_of_accounts < 2:
		print("Sorry, you do not have enough accounts to transfer.")
		return
	account_w = check_account_user(input("Account Number to Withdraw: "), get_nums_from_id(id, mysql_conn))
	retrieve_sql = '''SELECT balance
						FROM Account
						WHERE account_num = %s'''%account_w
	balance = pandas.read_sql(retrieve_sql, con=mysql_conn).values.item(0)
	if balance == 0:
		print("Sorry, no money in this account to withdraw.")
		return
	account_d = check_account_user(input("Account Number to Deposit: "), get_nums_from_id(id, mysql_conn))
	amount = check_withdraw(input("Amount to withdraw: "), balance)
	update_withdraw_sql = '''UPDATE Account
								SET balance = balance - %s
                     			WHERE account_num = %s'''
	update_withdraw_vals = (amount, account_w)
	mysql_cur.execute(update_withdraw_sql, update_withdraw_vals)
	insert_log(mysql_cur, datetime.now(), id, account_w, 'Withdraw', amount)
	update_deposit_sql = '''UPDATE Account
							SET balance = balance + %s
                     		WHERE account_num = %s'''
	update_deposit_vals = (amount, account_d)
	mysql_cur.execute(update_deposit_sql, update_deposit_vals)
	insert_log(mysql_cur, datetime.now(), id, account_d, 'Deposit', amount)

def insert_log(mysql_cur, time, id, num, type, amount):
	insert_sql = 'INSERT INTO Transaction_log VALUES(%s, %s, %s, %s, %s)'
	insert_vals = (time, id, num, type, amount)
	mysql_cur.execute(insert_sql, insert_vals)

# Retruns list of all customer ids
# @param mysql_conn
# @return list
def get_ids(mysql_conn):
	return pandas.read_sql('SELECT customer_id FROM Customer;', con=mysql_conn).values

# Returns list of all account numbers
# @param mysql_conn
# @return list
def get_nums(mysql_conn):
	return pandas.read_sql('SELECT account_num FROM Account;', con=mysql_conn).values

def get_nums_from_id(c, mysql_conn):
	retrieve_sql = '''SELECT a.account_num
						FROM Account AS a
						JOIN Account_xref AS r ON r.account_num = a.account_num
						WHERE r.customer_id = %s'''%c
	return pandas.read_sql(retrieve_sql, con=mysql_conn).values

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
def check_customer_user(c, ids):
	while not c.isdigit() or not int(c) in ids:
		print("Please input a valid customer id (", end=" ")
		for id in ids:
			print(id, end=" ")
		print("):", end=" ")
		c = input()
	return int(c)

# Makes sure that randomly generated account number doesn't exist
# @param a Randomly generated account number
# @return a Valid account num
def check_account_random(a, nums):
	while a in nums:
		a = random.randint(1, 9999)
	return a

# Checks if user inputted account number belongs to that customer
# @param a Account Number
# @param c Customer ID
# @return a Valid account num
def check_account_user(a, nums_from_id):
	while not a.isdigit() or not int(a) in nums_from_id:
		print("Please input a valid account number (", end=" ")
		for num_from_id in nums_from_id:
			print(num_from_id, end=" ")
		print("):", end=" ")
		a = input()
	return int(a)

# Checks if account type is valid
# t Account Type
# @return t Valid account type
def check_type(t):
	while t.lower() != "checking" and t.lower() != "savings":
		t = input("Please input a valid type (Checking, Savings): ")
	return t.lower().capitalize()

# Checks to make sure transaction is valid (greater than balance in account)
# w Withdraw amount
# b Balance
# @return w Valid withdraw amouont
def check_withdraw(w, b):
	while not w.isdigit() or int(w) > b:
		w = input("Please input a valid amount (less than or equal to " + str(b) + "): ")
	return int(w)

# Checks to make sure value is an integer
# i Integer
# @return i Valid int
def check_int(i):
	while not i.isdigit() or int(i) < 0:
		i = input("Please input a valid integer (greater than or equal to 0): ")
	return int(i)

# Checks to make sure value is an float
# f Float
# @return f Valid float
def check_float(f):
	while not f.replace('.', '', 1).isdigit()  or float(f) < 0:
		f = input("Please input a valid float (greater than or equal to 0): ")
	return float(f)

# Creates connection with MySQL server
# @param db_user Username
# @param db_password Password
# @param host_name Server IP Address
# @param db_name Name of Database
# @return conn MySQL Connection
def create_mysql_connection(db_user, db_password, host_name, db_name):
    conn = None
    try:
        conn = pymysql.connect(user=db_user, password=db_password, host=host_name, db=db_name, autocommit=True)
    except:
        print('connection failed')
    return conn

if __name__== "__main__":
	main()
