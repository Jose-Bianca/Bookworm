CREATE Table users(
	UserID int,
	Location Varchar,
	Age Varchar
);

copy users(UserID,Location,Age)
    From 'C:\Users\josep\OneDrive\Universitet\2. Semester\Databases and information systems\archive\books_data.SQL\users.csv'
    delimiter ';'
escape '\'
    CSV HEADER;

