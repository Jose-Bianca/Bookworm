CREATE Table books (
	ISBN Varchar,
	BookTitle VARCHAR,
	BookAuthor Varchar,
	YearOfPublication int,
	Publisher Varchar,
	ImageURLS Varchar,
	ImageURLM Varchar,
	ImageURLL Varchar
);

copy books(ISBN, BookTitle, BookAuthor, YearOfPublication,Publisher,ImageURLS,ImageURLM, ImageURLL)
	from ''
	delimiter ';'
	escape '\'
	CSV HEADER;
