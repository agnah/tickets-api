"""Se sumo el campo nro de GDE a modelo de tickets

Revision ID: a62f232aaffe
Revises: fd2553377845
Create Date: 2023-11-25 18:19:22.816134

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a62f232aaffe'
down_revision = 'fd2553377845'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('ticket', sa.Column('nro_gde', sa.String(length=256), nullable=True))
    op.execute("ALTER TABLE tickets.ticket CHANGE nro_gde nro_gde varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL AFTER id")

    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('ticket', 'nro_gde')
    # ### end Alembic commands ###
