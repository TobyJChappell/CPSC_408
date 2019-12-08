--author: Toby Chappell
--date: 12/9/19
--assignment: Final Project Unfiltered Database Schema

CREATE TABLE Title(
	title_id VARCHAR(9) PRIMARY KEY,
	type VARCHAR(63),
	primary_title VARCHAR(255),
	original_title VARCHAR(255),
	is_adult BIT,
	start_year INT,
	end_year INT,
	runtime INT,
	genres VARCHAR(255)
);

CREATE TABLE Name(
	name_id VARCHAR(15) PRIMARY KEY,
	primary_name VARCHAR(255),
	birth_year INT,
	death_year INT,
	profession VARCHAR(255),
	known_for VARCHAR(255)
);

CREATE TABLE Rating(
	title_id VARCHAR(9),
	avg_rating FLOAT(2),
	num_votes INT,
	FOREIGN KEY (title_id) REFERENCES Title (title_id)
	ON UPDATE CASCADE
	ON DELETE CASCADE
);

CREATE TABLE Aka(
	title_id VARCHAR(15),
	ordering INT,
	title VARCHAR(255),
	region VARCHAR(63),
	language VARCHAR(63),
	types VARCHAR(255),
	attributes VARCHAR(255),
	is_original_title BIT,
	FOREIGN KEY (title_id) REFERENCES Title (title_id)
	ON UPDATE CASCADE
	ON DELETE CASCADE
);

CREATE TABLE Crew(
	title_id VARCHAR(15),
	directors VARCHAR(255),
	writers VARCHAR(255),
	FOREIGN KEY (title_id) REFERENCES Title (title_id)
	ON UPDATE CASCADE
	ON DELETE CASCADE
);

CREATE TABLE Episode(
	title_id VARCHAR(15),
	parent_title_id VARCHAR(15),
	season INT,
	episode INT,
	FOREIGN KEY (title_id) REFERENCES Title (title_id)
	ON UPDATE CASCADE
	ON DELETE CASCADE,
	FOREIGN KEY (parent_title_id) REFERENCES Title (title_id)
	ON UPDATE CASCADE
	ON DELETE CASCADE
);

CREATE TABLE Principal(
	title_id VARCHAR(15),
	ordering INT,
	name_id VARCHAR(15),
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
