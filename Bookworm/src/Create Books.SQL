CREATE TABLE IF NOT EXISTS books(id char(4),
BookTitle varchar,
BookAuthor varchar,
YearOfPublication int,
Publisher varchar,
Rating varchar,
CONSTRAINT nft_pk PRIMARY KEY (id));

copy  books(id,BookTitle,BookAuthor,YearOfPublication , Publisher, Rating)
            from 'C:\PATH\TO\PROJECT\dis-nft-project\tmp\attributes.csv'
            delimiter ';'
            escape '\'
            CSV HEADER;
