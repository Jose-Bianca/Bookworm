CREATE Table books (
	ISBN Varchar,
	"Book-Title" VARCHAR,
	"Book-Author" Varchar,
	"Year-Of-Publication" int,
	Publisher Varchar,
	ImageURLS Varchar,
	ImageURLM Varchar,
	ImageURLL Varchar
);

copy books(USerID,ISBN,BookRating)
	from 'C:\Users\josep\OneDrive\Universitet\2. Semester\Databases and information systems\archive\books_data\books.csv'
	delimiter ';'
	CSV HEADER;
