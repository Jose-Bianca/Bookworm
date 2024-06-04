CREATE Table ratings(
	UserID int,
	ISBN Varchar,
	BookRating int
);

copy ratings(USerID,ISBN,BookRating)
	from 'C:/Users/josep/OneDrive/Universitet/2. Semester/Databases and information systems/archive/books_data/ratings.csv'
	delimiter ';'
	CSV HEADER;