--author: Toby Chappell
--date: 9/27/19
--assignment: Lab 2

--1. How many records are in the cars data
SELECT COUNT(*) as num_cars
FROM cars;

--2. How many cars originated in the US?
SELECT COUNT(*) as num_us
FROM cars
WHERE origin = 'US';

--3.	How many cars were built in years 70-75?
SELECT COUNT(*) as num_70_75
FROM cars
WHERE year BETWEEN 70 AND 75;

--4.	How many cars get more than 30 MPG?
SELECT COUNT(*) as mpg_30
FROM cars
WHERE mpg > 30;

--5.	Are there any cars with more horsepower than displacement? If so, what models?
SELECT model
FROM cars
WHERE horsepower > displacement;

--6.	How many car models have an MPG lower than 11?
SELECT COUNT(*) as mpg_11
FROM cars
WHERE mpg < 11;

--7.	Where were the cars from #6 built? (Hint: use a subquery)
SELECT DISTINCT origin
FROM cars
WHERE mpg < 11;

--8.	Which car manufacturer origin has the lowest average horsepower?
SELECT origin, horsepower
FROM cars
GROUP BY origin
ORDER BY horsepower;

--9.	How many cars made in the US have MPG under 20?
SELECT COUNT(*) as mpg_20
FROM cars
WHERE origin = 'US' AND mpg < 20;

--10.	How much horsepower does a ford fiesta have?
SELECT horsepower
FROM cars
WHERE model = 'ford fiesta';

--11.	Which number of cylinders has the highest average HP?
SELECT cylinders, horsepower
FROM cars
GROUP BY cylinders
ORDER BY horsepower DESC;

--12.	What countries have 4-cylinder cars?
SELECT DISTINCT origin
FROM cars
WHERE cylinders = 4;

--13.	How many cars that weigh under 2000 get an MPG lower than 30?
SELECT COUNT(*) as weight_2000_mpg_30
FROM cars
WHERE weight < 2000 AND mpg < 30;

--14.	How many cylinders do the cars that get over 40 MPG have?
SELECT DISTINCT cylinders
FROM cars
WHERE mpg > 40;

--15.	What countries did the cars in #13 originate in?
SELECT DISTINCT origin
FROM cars
WHERE mpg < 30 AND weight < 2000;

--16.	What is the percentage (out of all the data) of cars that originate in the US?
SELECT COUNT(*)*100.0/(SELECT COUNT(*) FROM cars) as percent_us
FROM cars
WHERE origin = 'US';

--17.	What is the percentage (out of all the data) of cars have 8 cylinders?
SELECT COUNT(*)*100.0/(SELECT COUNT(*) FROM cars) as percent_8_cylinders
FROM cars
WHERE cylinders = 8;

--18.	Write a query to return the average displacement per origin+cylinder combo. What is the result?
SELECT origin, cylinders, AVG(displacement)
FROM cars
GROUP BY origin, cylinders;

--19.	Write a query to only return the cylinders and average displacement, where the origin is Japan, from the query in #18. (Hint: use a subquery)
SELECT cylinders, AVG(displacement)
FROM cars
WHERE origin = 'Japan'
GROUP BY cylinders

--20.	Find the model of the car that has the max horsepower in the US. (Hint: use a subquery)
SELECT model, horsepower
FROM cars
WHERE origin = 'US'
GROUP BY model
ORDER BY horsepower DESC;
