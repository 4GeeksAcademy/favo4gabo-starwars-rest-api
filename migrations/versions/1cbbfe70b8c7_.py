"""empty message

Revision ID: 1cbbfe70b8c7
Revises: 474280d0003c
Create Date: 2023-11-02 17:57:07.938780

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1cbbfe70b8c7'
down_revision = '474280d0003c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('people',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('eye_color', sa.String(length=100), nullable=False),
    sa.Column('skin_color', sa.String(length=100), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('eye_color'),
    sa.UniqueConstraint('name'),
    sa.UniqueConstraint('skin_color')
    )
    op.create_table('planets',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('rotation_period', sa.String(length=100), nullable=False),
    sa.Column('climate', sa.String(length=100), nullable=False),
    sa.Column('terrain', sa.String(length=100), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('climate'),
    sa.UniqueConstraint('name'),
    sa.UniqueConstraint('rotation_period'),
    sa.UniqueConstraint('terrain')
    )
    op.create_table('favorites',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('people_id', sa.Integer(), nullable=True),
    sa.Column('planets_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['people_id'], ['people.id'], ),
    sa.ForeignKeyConstraint(['planets_id'], ['planets.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('favorites')
    op.drop_table('planets')
    op.drop_table('people')
    # ### end Alembic commands ###