CREATE EXTENSION pg_trgm;
CREATE EXTENSION pgcrypto;
CREATE EXTENSION intarray;

CREATE TABLE user_info (
    user_no serial NOT NULL,
    user_id text NOT NULL,
    user_passwd text,
    user_name text,
    user_email text,
    user_phone text,
    user_enabled smallint DEFAULT 1,
    login_fail_count smallint DEFAULT 0,
    passwd_update_date timestamp with time zone DEFAULT now(),
    passwd_reset_key text,
    passwd_reset_ready smallint,
    extra_info jsonb DEFAULT '{}'::jsonb,
    modify_date timestamp with time zone DEFAULT now(),
    reg_date timestamp with time zone DEFAULT now(),
    is_enable smallint DEFAULT 1
)
WITH (fillfactor=70);

ALTER TABLE user_info ADD CONSTRAINT user_info_pkey PRIMARY KEY (user_no);

CREATE INDEX user_info_user_id_idx ON user_info USING btree (user_id);
CREATE INDEX user_info_user_name_idx ON user_info USING btree (user_name) WITH (fillfactor=90);
CREATE INDEX user_info_user_name_idx_gin ON user_info USING gin (user_name gin_trgm_ops);
CREATE INDEX user_info_user_email_idx ON user_info USING btree (user_email) WITH (fillfactor=80);
CREATE INDEX user_info_user_email_idx_gin ON user_info USING gin (user_email gin_trgm_ops);
CREATE INDEX user_info_is_enable_idx ON user_info USING btree (is_enable);

CREATE TABLE directory_info (
	directory_no serial NOT NULL,
	directory_name TEXT,
	parent_directory_no int,
	reg_date timestamp DEFAULT now()
) WITH (fillfactor=80);

ALTER TABLE directory_info ADD CONSTRAINT directory_info_pkey PRIMARY KEY (directory_no);

CREATE INDEX directory_info_parent_directory_no_idx ON directory_info USING btree (parent_directory_no);
CREATE INDEX directory_info_directory_name_idx ON directory_info USING btree (directory_name);
`

CREATE TABLE user_directory (
	user_directory_no serial NOT NULL,
	user_no int,
	directory_no int
)

CREATE INDEX user_directory_user_directory_no_idx ON user_directory USING btree (user_directory_no);
CREATE INDEX user_directory_user_no_idx ON user_directory USING btree (user_no);
CREATE INDEX user_directory_directory_no_idx ON user_directory USING btree (directory_no);

ALTER TABLE user_directory
ADD CONSTRAINT user_directory_user_no_fkey
FOREIGN KEY (user_no)
REFERENCES user_info (user_no)
ON UPDATE NO ACTION
ON DELETE NO ACTION;

ALTER TABLE user_directory
ADD CONSTRAINT user_directory_directory_no_fkey
FOREIGN KEY (directory_no)
REFERENCES directory_info (directory_no)
ON UPDATE NO ACTION
ON DELETE NO ACTION;

CREATE TABLE file_info (
	file_no serial NOT NULL,
	file_name TEXT,
	raw_name TEXT,
	directory_no int,
	reg_date timestamp DEFAULT now()
) WITH (fillfactor=80);

ALTER TABLE file_info ADD CONSTRAINT file_info_pkey PRIMARY KEY (file_no);

CREATE INDEX file_info_file_no_idx ON file_info USING btree (file_no);
CREATE INDEX file_info_file_name_idx ON file_info USING btree (file_name);
CREATE INDEX file_info_file_name_idx_gin ON file_info USING gin (file_name gin_trgm_ops);
CREATE INDEX file_info_directory_no_idx ON file_info USING btree (directory_no);

ALTER TABLE file_info
ADD CONSTRAINT file_info_directory_no_fkey
FOREIGN KEY (directory_no)
REFERENCES directory_info (directory_no)
ON UPDATE NO ACTION
ON DELETE NO ACTION;