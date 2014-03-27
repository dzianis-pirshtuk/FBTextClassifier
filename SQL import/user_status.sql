DROP TABLE IF EXISTS user_status;

COMMIT;

CREATE TABLE user_status 
(
  userid     CHAR(32) NOT NULL,
  postdate   VARCHAR NOT NULL,
  posttext   text
);

COPY user_status
FROM '/tmp/user_status.csv' DELIMITER ',' CSV ENCODING 'WIN1252' ESCAPE '/' HEADER;
COMMIT;

CREATE INDEX useridindx ON user_status USING btree (userid);

CLUSTER useridindx ON user_status;

COMMIT;

SET AUTOCOMMIT TRUE;

VACUUM;

ANALYZE;

SET AUTOCOMMIT FALSE;
