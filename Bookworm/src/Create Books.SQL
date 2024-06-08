CREATE TABLE IF NOT EXISTS books(id char(4),
BookTitle varchar,
BookAuthor varchar,
YearOfPublication int,
Publisher varchar,
Rating varchar,
CONSTRAINT books_pk PRIMARY KEY (id));

copy  books(id,BookTitle,BookAuthor,YearOfPublication , Publisher, Rating)
            from 'C:\Users\josep\OneDrive\Dokumenter\GitHub\Website-project\Bookworm\tmp\books3.csv'
            delimiter ';'
            escape '\'
            CSV HEADER;
