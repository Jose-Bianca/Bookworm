CREATE TABLE IF NOT EXISTS Attributes(id char(4),
type varchar,
gender varchar,
skin_tone int,
count varchar,
accessories varchar,
CONSTRAINT nft_pk PRIMARY KEY (id));

copy  Attributes(id,type,gender, skin_tone, count, accessories)
            from 'C:\PATH\TO\PROJECT\dis-nft-project\tmp\attributes.csv'
            delimiter ';'
            escape '\'
            CSV HEADER;
