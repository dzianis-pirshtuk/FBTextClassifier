BEGIN;

DROP TABLE IF EXISTS user_status_caps;

COMMIT;
BEGIN;

CREATE TABLE user_status_caps
(
  userid     CHAR(32) NOT NULL,
  caps        integer
);

COPY user_status_caps
FROM '/tmp/user_status_caps.csv' CSV ENCODING 'UTF-8';

CREATE INDEX user_status_caps_userid_indx ON user_status_caps (userid);

COMMIT;

VACUUM;

ANALYZE;

