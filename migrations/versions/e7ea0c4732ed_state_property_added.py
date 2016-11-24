"""state property added

Revision ID: e7ea0c4732ed
Revises: 2804a921b1fb
Create Date: 2016-11-24 07:44:54.566000

"""

# revision identifiers, used by Alembic.
revision = 'e7ea0c4732ed'
down_revision = '2804a921b1fb'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('states',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('state', sa.String(length=10), nullable=True),
    sa.Column('issue_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['issue_id'], ['issues.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('state')
    op.add_column('issues', sa.Column('state', sa.String(length=10), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('issues', 'state')
    op.create_table('state',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('state', sa.VARCHAR(length=10), nullable=True),
    sa.Column('issue_id', sa.INTEGER(), nullable=True),
    sa.ForeignKeyConstraint(['issue_id'], [u'issues.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('states')
    ### end Alembic commands ###
