--author: Toby Chappell
--date: 12/9/19
--assignment: Final Project Filtered Database Schema
--Filtered to movies (english) released in the past 20 years as well as a limit of 10,000 records on people

--Information on Title
--title_id = Used to link tables
--title = Name of movie
--start_year = Year movie was released
--genres = Genre of movie
CREATE TABLE F_Title(
	title_id VARCHAR(9) PRIMARY KEY,
	title VARCHAR(255),
	start_year INT,
	genres VARCHAR(255)
);

INSERT INTO F_Title
SELECT t.title_id, a.title, t.start_year, t.genres
FROM Title AS t
JOIN Aka AS a ON t.title_id = a.title_id
WHERE t.type = 'movie' AND t.genres != '\\N' AND t.start_year >= 2000 AND t.start_year <= 2020 AND a.language = 'en' AND a.ordering = 1;

--Information on Name
--name_id = Used to link tables
--primary_name = Name of person
--birth_year = Year person was born
--death_year = Year person died if applicable
--profession = Profession of person
--known_for = Movies person is known for
CREATE TABLE F_Name(
	name_id VARCHAR(15) PRIMARY KEY,
	primary_name VARCHAR(255),
	birth_year INT,
	death_year INT,
	profession VARCHAR(255),
	known_for VARCHAR(255)
);

INSERT INTO F_Name
SELECT n.name_id, n.primary_name, n.birth_year, n.death_year, n.profession, n.known_for
FROM Name AS n
JOIN Principal AS p ON p.name_id = n.name_id
JOIN F_Title AS t ON p.title_id = t.title_id
GROUP BY n.name_id
LIMIT 10000;

--Information on Rating
--avg_rating = Average rating of movie
--num_votes = Number of votes given to movie
CREATE TABLE F_Rating(
	title_id VARCHAR(9),
	avg_rating FLOAT(2),
	num_votes INT,
	FOREIGN KEY (title_id) REFERENCES F_Title (title_id)
	ON UPDATE CASCADE
	ON DELETE CASCADE
);

INSERT INTO F_Rating
SELECT r.title_id, r.avg_rating, r.num_votes
FROM Rating AS r
JOIN F_Title AS t ON t.title_id = r.title_id;

--Relates Title to Name
--category = Role person
--characters = Role that actor/actress plays
CREATE TABLE F_Principal(
	title_id VARCHAR(15),
	name_id VARCHAR(15),
	ordering INT,
	category VARCHAR(255),
	job VARCHAR(255),
	characters VARCHAR(255),
	primary_name VARCHAR(255),
	title VARCHAR(255),
	FOREIGN KEY (title_id) REFERENCES Title (title_id)
	ON UPDATE CASCADE
	ON DELETE CASCADE,
	FOREIGN KEY (name_id) REFERENCES Name (name_id)
	ON UPDATE CASCADE
	ON DELETE CASCADE
);

INSERT INTO F_Principal
SELECT p.title_id, p.name_id, p.ordering, p.category, p.job, p.characters, n.primary_name, t.title
FROM Principal AS p
JOIN F_Title AS t ON t.title_id = p.title_id
JOIN F_Name AS n ON n.name_id = p.name_id
LIMIT 10000;
