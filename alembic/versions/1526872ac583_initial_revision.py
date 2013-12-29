"""initial revision

Revision ID: 1526872ac583
Revises: None
Create Date: 2013-12-28 16:52:49.921652

"""

# revision identifiers, used by Alembic.
revision = '1526872ac583'
down_revision = None

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('responses',
    sa.Column('id', sa.String(), nullable=False),
    sa.Column('size', sa.Integer(), nullable=True),
    sa.Column('time', sa.Float(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('requests',
    sa.Column('id', sa.String(), nullable=False),
    sa.Column('path', sa.String(), nullable=True),
    sa.Column('method', sa.String(), nullable=True),
    sa.Column('params', postgresql.HSTORE(), nullable=True),
    sa.Column('size', sa.Integer(), nullable=True),
    sa.Column('time', sa.Float(), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_requests_timestamp', 'requests', ['timestamp'], unique=False)
    ### end Alembic commands ###
    op.execute(
        'CREATE VIEW querystats AS SELECT '
        'req.method, '
        'req.path, '
        'req.params, '
        'req.timestamp, '
        'req.size AS req_size, '
        'req.time AS req_time, '
        'res.time AS res_time, '
        'res.size AS res_size '
        'FROM requests req '
        'LEFT JOIN responses res ON req.id = res.id;'
    )


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_requests_timestamp', 'requests')
    op.drop_table('requests')
    op.drop_table('responses')
    ### end Alembic commands ###
    op.drop_view('querystats')
