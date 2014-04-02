BEGIN;

DROP TABLE IF EXISTS user_status_len;

COMMIT;
BEGIN;

CREATE TABLE user_status_len
(
  userid     CHAR(32) NOT NULL,
  leng        integer
);

COPY user_status_len
FROM '/tmp/user_status_len.csv' CSV ENCODING 'UTF-8';

CREATE INDEX user_status_len_userid_indx ON user_status_len (userid);

COMMIT;

VACUUM;

ANALYZE;

