# author: Toby Chappell
# date: 12/?/19
# assignment: Final Project Backend

import pymysql
import pandas
import random
from datetime import datetime

def main():
	mysql_conn = create_mysql_connection(db_user='root', db_password='1Secret1', host_name='34.68.212.129', db_name='imdb_data')
	mysql_cur = mysql_conn.cursor()
	selection = 1
	prompt = """\nYou have the following options:
	1. New Movie
	2. Delete Movie
	3. New Name
	4. Delete Name
	5. Quit
Please select an option: """
	while selection != 5:
		selection = check_choice(input(prompt))
		if selection == 5:
			break
		elif selection == 1:
			add_movie(mysql_conn, mysql_cur)
		elif selection == 2:
			delete_movie(mysql_conn, mysql_cur)
		elif selection == 3:
			add_name(mysql_conn, mysql_cur)
		elif selection == 4:
			delete_name(mysql_conn, mysql_cur)
	print("Have a nice day!\n")
	mysql_cur.close()
	mysql_conn.close()

# Add movie to database
# @param mysql_cur
# @param mysql_conn
def add_movie(mysql_conn, mysql_cur):
	id = get_random_movie_id(get_movie_ids(mysql_conn))
	title = input("Title: ")
	year = check_year(input("Year Released: "))
	genre = check_genre(input("Genre: "))
	insert_sql = 'INSERT INTO F_Title VALUES(%s, %s, %s, %s)'
	insert_vals = (id, title, year, genre)
	mysql_cur.execute(insert_sql, insert_vals)
	print("The Movie ID is: ", id)

# Delete movie from database
# @param mysql_cur
# @param mysql_conn
def delete_movie(mysql_conn, mysql_cur):
	ids = get_movie_ids(mysql_conn)
	id = input("Please enter the Movie ID you want to delete: ")
	while not id in ids:
		id = input("Please enter a valid Movie ID: ")
	insert_sql = 'DELETE FROM F_Title WHERE title_id = %s'
	insert_vals = (id)
	mysql_cur.execute(insert_sql, insert_vals)

# Add name to database
# @param mysql_cur
# @param mysql_conn
def add_name(mysql_conn, mysql_cur):
	id = get_random_name_id(get_name_ids(mysql_conn))
	name = input("Name: ")
	b_year = check_year(input("Birth Year: "))
	if input("Is death year applicable (yes if true): ")[0].lower() == "y":
		d_year = check_year(input("Death Year: "))
		while d_year <  b_year:
			d_year = check_year(input("Please input a year after birth year: "))
	else:
		d_year = None
	profession = input("Profession: ")
	known_for = check_known_for(input("Known for (Movie ID): "), get_movie_ids(mysql_conn))
	insert_sql = 'INSERT INTO F_Name VALUES(%s, %s, %s, %s, %s, %s)'
	insert_vals = (id, name, b_year, d_year, profession, known_for)
	mysql_cur.execute(insert_sql, insert_vals)
	print("The Name Id is: ", id)

# Delete name from database
# @param mysql_cur
# @param mysql_conn
def delete_name(mysql_conn, mysql_cur):
	ids = get_name_ids(mysql_conn)
	id = input("Please enter the Name ID you want to delete: ")
	while not id in ids:
		id = input("Please enter a valid Name ID: ")
	insert_sql = 'DELETE FROM F_Name WHERE name_id = %s'
	insert_vals = (id)
	mysql_cur.execute(insert_sql, insert_vals)

# Retruns list of all customer ids
# @param mysql_conn
# @return list
def get_movie_ids(mysql_conn):
	return pandas.read_sql('SELECT title_id FROM F_Title;', con=mysql_conn).values

# Returns list of all account numbers
# @param mysql_conn
# @return list
def get_name_ids(mysql_conn):
	return pandas.read_sql('SELECT name_id FROM F_Name;', con=mysql_conn).values

# Checks if selection is valid
# @param c Selection
# @return c Valid selction
def check_choice(c):
	while not c.isdigit() or int(c) > 5 or int(c) < 1:
		c = input("Please input a valid option (1-5): ")
	return int(c)

# Generates random movie id that doesn't exist
# @param ids List of current movie ids
# @return c Valid movie id
def get_random_movie_id(ids):
	c = ("tt" + str(random.randint(1000000, 9999999)))
	while c in ids:
		c = ("tt" + str(random.randint(1000000, 9999999)))
	return c

# Generates random name id that doesn't exist

# @return c Valid name id
def get_random_name_id(ids):
	c = ("nm" + str(random.randint(1000000, 9999999)))
	while c in ids:
		c = ("nm" + str(random.randint(1000000, 9999999)))
	return c

# Checks to make sure value is a valid year
# y Integer
# @return y Valid year
def check_year(y):
	while not y.isdigit():
		y = input("Please input a valid year: ")
	return int(y)

# Checks to make sure value is a valid genre
# g Genre
# @return g Valid genre
def check_genre(g):
	genres = ["Action", "Adult", "Adventure", "Animation", "Biography", "Comedy", "Crime", "Documentary", "Drama", "Family", "Fantasy", "History", "Horror", "Music", "Musical", "Mystery", "Romance", "Sci-Fi", "Sport", "Thriller", "War", "Western"]
	while not g.lower().capitalize() in genres:
		print("Please input a valid genre (", end=" ")
		for genre in genres:
			print(genre, end=" ")
		print("):", end=" ")
		g = input()
	return g.lower().capitalize()

# Checks to make sure value is a valid movie id
# i Movie ID
# @return y Valid year
def check_known_for(i, ids):
	while i != "\\N" and not i in ids:
		i = input("Please input a valid Movie ID (\\N if not applicable): ")
	if i == "\\N":
		return None
	return i

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
