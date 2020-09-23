"""'directory_info'

Revision ID: 210fb2b208ed
Revises: 
Create Date: 2020-09-15 10:17:18.995262

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '210fb2b208ed'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    db = op.get_bind()

    fix_process = db.execute(
        "SELECT column_name FROM information_schema.columns WHERE table_name = 'directory_info';").fetchone()
    if not fix_process:
        db.execute("""\
CREATE TABLE directory_info (
	directory_no serial NOT NULL,
	directory_name TEXT,
	parent_directory_no int,
	directory_info int,
	reg_date timestamp DEFAULT now()
) WITH (fillfactor=80);

ALTER TABLE directory_info ADD CONSTRAINT directory_info_pkey PRIMARY KEY (directory_no);

CREATE INDEX directory_info_parent_directory_no_idx ON directory_info USING btree (parent_directory_no);
CREATE INDEX directory_info_directory_owner_idx ON directory_info USING btree (directory_owner);
CREATE INDEX directory_info_directory_name_idx ON directory_info USING btree (directory_name);
CREATE INDEX directory_info_directory_name_idx_gin ON directory_info USING gin (directory_name gin_trgm_ops);

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
""")


def downgrade():
    pass
