BEGIN;

DROP TABLE IF EXISTS user_demog;

CREATE TABLE user_demog
(
  userid                  VARCHAR(32) NOT NULL,
  gender                  bool,
  birthday                date DEFAULT NULL,
  age                     smallint,
  relationship_status     smallint,
  interested_in           smallint,
  mf_relationship         bool,
  mf_dating               bool,
  mf_random               bool,
  mf_friendship           bool,
  mf_whatever             bool,
  mf_networking           bool,
  locale                  VARCHAR(5),
  network_size            int,
  timezone                int
);

COPY user_demog
FROM '/tmp/demog_proc.csv' DELIMITER ',' CSV ENCODING 'LATIN1' ESCAPE '/' HEADER NULL AS '';

CREATE INDEX user_demog_userid_indx ON user_demog (userid);

CLUSTER user_demog_userid_indx ON user_demog;

COMMIT;

VACUUM;

ANALYZE;
