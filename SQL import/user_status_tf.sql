BEGIN;

DROP TABLE IF EXISTS user_status_tf;

COMMIT;
BEGIN;

CREATE TABLE user_status_tf
(
  userid     CHAR(32) NOT NULL,
  term       text NOT NULL,
  cnt        integer
);

COPY user_status_tf
FROM '/tmp/user_status_tf.csv' CSV ENCODING 'UTF-8';

CREATE INDEX user_status_tf_userid_indx ON user_status_tf (userid);
CREATE INDEX user_status_tf_term_indx ON user_status_tf (term);

COMMIT;

VACUUM;

ANALYZE;

