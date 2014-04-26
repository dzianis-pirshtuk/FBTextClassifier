BEGIN;

DROP TABLE IF EXISTS big5;

CREATE TABLE big5
(
  userid                  CHAR(32) NOT NULL,
  openness                real NOT NULL,
  conscientiousness       real NOT NULL,
  extroversion            real NOT NULL,
  agreeableness           real NOT NULL,
  neuroticism             real NOT NULL,
  item_level              smallint NOT NULL,
  blocks                  smallint NOT NULL,
  datetaken               date
);

COPY big5
FROM '/tmp/big5_proc.csv' DELIMITER ',' CSV ENCODING 'LATIN1' ESCAPE '/' HEADER NULL AS '';

CREATE INDEX big5_userid_indx ON big5 (userid);

COMMIT;

VACUUM;

ANALYZE;
