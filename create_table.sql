CREATE TABLE Crp
(
Crp INTEGER AUTO_INCREMENT UNIQUE,
Name TEXT,
adres TEXT,
places TEXT,
PRIMARY KEY (Crp)
);

CREATE TABLE DrNobet
(
Crp INTEGER,
period TEXT,
id INTEGER UNIQUE,
location TEXT,
day INTEGER
);

CREATE TABLE DrNobInfo
(
Crp INTEGER,
id INTEGER,
period TEXT,
friday_shifts INTEGER,
total_shifts INTEGER,
we_shifts INTEGER,
inf_loc TEXT,
vacation_days TEXT,
mustdays TEXT,
on_days TEXT,
off_days TEXT
);

CREATE TABLE NobetleRun
(
Crp INTEGER,
period TEXT,
run INTEGER,
objective FLOAT,
status TEXT,
calc_duration FLOAT
);

CREATE TABLE User
(
Crp INTEGER,
id INTEGER AUTO_INCREMENT UNIQUE,
type TEXT,
Name TEXT,
Surname TEXT,
mail TEXT,
password TEXT,
PRIMARY KEY (id)
);
