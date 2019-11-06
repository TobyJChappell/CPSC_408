DROP TABLE IF EXISTS Person;
DROP TABLE IF EXISTS Frequents;
DROP TABLE IF EXISTS Eats;
DROP TABLE IF EXISTS Serves;
DROP TABLE IF EXISTS Customers;
DROP TABLE IF EXISTS Customer_address;
DROP TABLE IF EXISTS Account_info;

CREATE TABLE Person(
	name VARCHAR(50),
	age INT,
	gender VARCHAR(10)
);

CREATE TABLE Frequents(
	name VARCHAR(50),
	pizzeria VARCHAR(20)
);

CREATE TABLE Eats(
	name VARCHAR(50),
	pizza VARCHAR(10)
);

CREATE TABLE Serves(
	pizzeria VARCHAR(20),
	pizza VARCHAR(10),
	price INT
);

--Pizzeria's frequented by males under the age of 18
SELECT DISTINCT f.pizzeria
FROM Frequents AS f
JOIN Person AS p ON f.name = p.name
WHERE UPPER(p.gender) = 'MALE' AND p.age < 18;

--Name of females that eat mushroom or pepperoni pizza
SELECT DISTINCT p.name
FROM Person AS p
JOIN Eats AS e ON p.name = e.name
WHERE p.gender = 'FEMALE' AND e.pizza IN ('mushroom', 'pepperoni');

--Average price Joe pays for all the pizzerias he frequents
SELECT AVG(s.price)
FROM Frequents AS f
JOIN Serves AS s ON s.pizzeria = f.pizzeria
GROUP BY f.name
HAVING f.name = 'Joe';



CREATE TABLE Customers(
	customer_id INT,
	first_name VARCHAR(10),
	last_name VARCHAR(10),
	account_num INT
);

CREATE TABLE Customer_address(
	customer_id INT,
	city VARCHAR(10),
	state VARCHAR(10),
	zip INT
);

CREATE TABLE Account_info(
	account_num INT,
	date_created VARCHAR(10),
	card_nums INT
);

--Return result set of Customer first name, last name, zip, and card number
SELECT c.first_name, c.last_name, ca.zip, a.card_nums
FROM Customers AS c
LEFT JOIN Customer_address AS ca ON c.customer_id = ca.customer_id
LEFT JOIN Account_info AS ai ON c.account_num = ai.account_num
