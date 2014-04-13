BEGIN;

DROP TABLE IF EXISTS user_status;

COMMIT;
BEGIN;

CREATE TABLE user_status 
(
  userid     CHAR(32) NOT NULL,
  postdate   VARCHAR NOT NULL,
  posttext   TEXT
);

COPY user_status
FROM '/tmp/user_status.csv' DELIMITER ',' CSV ENCODING 'LATIN1' ESCAPE '/' HEADER;

CREATE INDEX useridindx ON user_status USING btree (userid);

CLUSTER useridindx ON user_status;

COMMIT;

VACUUM;

ANALYZE;

