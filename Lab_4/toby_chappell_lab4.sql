--author: Toby Chappell
--date: 10/30/19
--assignment: Lab 4

/*
DATABASE CODE

.mode csv

CREATE TABLE Orders(
	receipt_number INT,
	num_ordered INT,
	item_id VARCHAR(20)
);

.import orders.csv Orders

CREATE TABLE Bakery_Goods(
	item_id VARCHAR(20),
	flavor VARCHAR(20),
	food VARCHAR(20),
	price FLOAT(2)
);

.import bakery_goods.csv Bakery_Goods

CREATE TABLE Receipts(
	receipt_number INT,
	day DATE,
	customer_id INT
);

.import receipts.csv Receipts

CREATE TABLE customers(
	customer_id INT,
	last_name VARCHAR(20),
	first_name VARCHAR(20)
);

.import customers.csv Customers
*/

--1.	How many receipts did KIP ARNN have? (answer should be 9)
SELECT COUNT(*)
FROM Customers AS c
JOIN Receipts AS r ON c.Customer_id = r.Customer_id
WHERE UPPER(c.first_name) = 'KIP' AND UPPER(c.last_name) = 'ARNN';


--2.	Return the receipt_number, item_id, and price of the receipt that had the highest priced item. (answer should be 51991,26-8x10,15.95) (receipt_number could be different)
SELECT o.receipt_number, o.item_id, MAX(b.price)
FROM Orders AS o
JOIN Bakery_Goods AS b ON o.item_id = b.item_id;

--3.	Find the top 5 busiest dates for the bakery. (HINT: which days had the highest number of items ordered? Use the SUM function with GROUP BY)
SELECT r.day
FROM Receipts AS r
JOIN Orders AS o ON r.receipt_number = o.receipt_number
GROUP BY r.day
ORDER BY SUM(o.num_ordered) DESC
LIMIT 5;

--4.	What was the total price of the order with receipt number 51991? Return only the summed price. (HINT: use a subquery) (answer should be $86.30)
SELECT SUM(b.price * o.num_ordered) AS total_price
FROM Receipts AS r
LEFT JOIN Orders AS o ON r.receipt_number = o.receipt_number
LEFT JOIN Bakery_Goods AS b ON o.item_id = b.item_id
GROUP BY r.receipt_number
HAVING r.receipt_number = 51991;

--5.	How many unique foods were ordered on ‘29-Oct-2007’? (HINT: use a subquery and join to the subquery) (answer should be 7)
SELECT COUNT(*)
FROM(
	SELECT b.food
	FROM Receipts AS r
	LEFT JOIN Orders AS o ON r.receipt_number = o.receipt_number
	LEFT JOIN Bakery_Goods AS b ON o.item_id = b.item_id
	GROUP BY r.day, b.food
	HAVING r.day = '29-Oct-07');

--6.	What is the name of the customer who had the most orders(receipts)?(RUPERT HELING)
SELECT c.first_name, c.last_name
FROM Customers AS c
JOIN Receipts AS r ON c.customer_id = r.customer_id
GROUP BY c.first_name, c.last_name
ORDER BY COUNT(r.receipt_number) DESC
LIMIT 1;
