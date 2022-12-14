"""empty message

Revision ID: 238399aca68d
Revises: 3dafd91e977a
Create Date: 2022-10-23 15:35:00.686418

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '238399aca68d'
down_revision = '3dafd91e977a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('answers', schema=None) as batch_op:
        batch_op.add_column(sa.Column('user_id', sa.Integer(), server_default='1', nullable=True))
        batch_op.create_foreign_key(batch_op.f('fk_answers_user_id_users'), 'users', ['user_id'], ['id'], ondelete='CASCADE')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('answers', schema=None) as batch_op:
        batch_op.drop_constraint(batch_op.f('fk_answers_user_id_users'), type_='foreignkey')
        batch_op.drop_column('user_id')

    # ### end Alembic commands ###
