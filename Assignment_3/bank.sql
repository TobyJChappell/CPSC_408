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
	ON DELETE CASCADE,
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
	trans_amount FLOAT(2),
	FOREIGN KEY (account_num) REFERENCES Account(account_num)
	ON UPDATE NO ACTION
	ON DELETE NO ACTION);
