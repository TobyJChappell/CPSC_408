--author: Toby Chappell
--date: 12/?/19
--assignment: Final Project Filtered Database Schema
--Filtered to movies only

DROP TABLE F_Crew;
DROP TABLE F_Principal;
DROP TABLE F_Rating;
DROP TABLE F_Name;
DROP TABLE F_Title;

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
WHERE t.type = 'movie' AND t.start_year >= 1887 AND t.start_year <= 2020 AND a.language = 'en' AND a.ordering = 1
LIMIT 10000;

CREATE TABLE F_Name(
	name_id VARCHAR(15) PRIMARY KEY,
	primary_name VARCHAR(255) NOT NULL,
	birth_year INT,
	death_year INT,
	profession VARCHAR(255) NOT NULL,
	known_for VARCHAR(255) NOT NULL
);

INSERT INTO F_Name
SELECT *
FROM Name
WHERE primary_name != '\\N' AND known_for != '\\N' AND profession != '\\N'
LIMIT 10000;

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
JOIN F_Title AS t ON t.title_id = r.title_id
LIMIT 10000;

CREATE TABLE F_Crew(
	title_id VARCHAR(15),
	directors VARCHAR(255),
	writers VARCHAR(255),
	FOREIGN KEY (title_id) REFERENCES Title (title_id)
	ON UPDATE CASCADE
	ON DELETE CASCADE
);

INSERT INTO F_Crew
SELECT c.title_id, c.directors, c.writers
FROM Crew AS c
JOIN F_Title AS t ON t.title_id = c.title_id
LIMIT 10000;

CREATE TABLE F_Principal(
	title_id VARCHAR(15),
	name_id VARCHAR(15),
	ordering INT,
	category VARCHAR(255),
	job VARCHAR(255),
	characters VARCHAR(255),
	FOREIGN KEY (title_id) REFERENCES Title (title_id)
	ON UPDATE CASCADE
	ON DELETE CASCADE,
	FOREIGN KEY (name_id) REFERENCES Name (name_id)
	ON UPDATE CASCADE
	ON DELETE CASCADE
);

INSERT INTO F_Principal
SELECT p.title_id, p.name_id, p.ordering, p.category, p.job, p.characters
FROM Principal AS p
JOIN F_Title AS t ON t.title_id = p.title_id
JOIN F_Name AS n ON n.name_id = p.name_id
LIMIT 10000;
