DROP TABLE IF EXISTS user_status;

commit;

CREATE TABLE user_status (
	userid char(32) NOT NULL,
	postdate varchar NOT NULL,
	posttext text
);

COPY user_status FROM '/tmp/user_status.csv' DELIMITER ',' CSV ENCODING 'WIN1252' ESCAPE '/' HEADER;

commit;
