"""'file_info'

Revision ID: 1d0e8b6d7add
Revises: 210fb2b208ed
Create Date: 2020-09-17 15:48:25.414411

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1d0e8b6d7add'
down_revision = '210fb2b208ed'
branch_labels = None
depends_on = None


def upgrade():
    db = op.get_bind()

    fix_process = db.execute(
        "SELECT column_name FROM information_schema.columns WHERE table_name = 'file_info';").fetchone()
    if not fix_process:
        db.execute("""\
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
""")


def downgrade():
    pass
