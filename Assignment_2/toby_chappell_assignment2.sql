--author: Toby Chappell
--date: 10/7/19
--assignment: Assignment 2

DROP TABLE IF EXISTS Customers;
DROP TABLE IF EXISTS Customer_Address;
PRAGMA foreign_keys = ON;

--1.	Create a table called Customers with the following structure:
--		Customer ID – this is a primary key
--		Customer first name
--		Customer last name
--		Customer age
CREATE TABLE Customers(
	c_id INT PRIMARY KEY NOT NULL,
	first_name VARCHAR(50),
	last_name VARCHAR(50),
	age INT
);

--2.	Insert 3 full customer records into the table
INSERT INTO Customers VALUES(1, 'Abby', 'Wong', 49);
INSERT INTO Customers VALUES(2, 'Iris', 'Henderson', 94);
INSERT INTO Customers VALUES(3, 'Bob', 'Smith', 63);

--3.	You gain a new customer but only know their first name is Jim, and their last name is Terf. Insert this customer into your table - don’t forget to give him a primary key
INSERT INTO Customers VALUES(4, 'Jim', 'Terf', NULL);

--4.	Update all customer’s names to be upper case
UPDATE Customers
SET first_name = UPPER(first_name);

--5.	Create a table called Customer_Address with the following structure:
--		Customer ID – this is a foreign key to the Customers table
--		Street number
--		Street name
--		City
--		State
--		Zip
CREATE TABLE Customer_Address(
	ca_id INT NOT NULL,
	street_number INT,
	street_name VARCHAR(50),
	city VARCHAR(50),
	ca_state VARCHAR(50),
	zip INT,
	FOREIGN KEY (ca_id) REFERENCES Customers(c_id)
	ON UPDATE CASCADE
	ON DELETE CASCADE
);

--6.	Insert an address for each of the customers you made in step 2 – make sure to adhere to foreign key rules
INSERT INTO Customer_Address VALUES(1, 1600, 'Clifton Rd.', 'Atlanta', 'GA', 30333);
INSERT INTO Customer_Address VALUES(2, 1, 'University Dr.', 'Orange', 'CA', 92866);
INSERT INTO Customer_Address VALUES(3, 2920, 'Zoo Dr.', 'San Diego', 'CA', 92101);

--7.	Update Jim Terf’s customer ID to be something different
UPDATE Customers
SET c_id = 5
WHERE UPPER(first_name) = 'JIM' AND UPPER(last_name) = 'TERF';
--Could also do WHERE statement on Jim's current id, ie. WHERE id = 4

--8.	Delete one of the records you made in step 2.
DELETE FROM Customers
WHERE c_id = 1;
