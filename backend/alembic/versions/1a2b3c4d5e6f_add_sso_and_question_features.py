"""Add SSO and Question features

Revision ID: 1a2b3c4d5e6f
Revises: cfc683876939
Create Date: 2025-08-03 16:30:00.123456

"""
from alembic import op
import sqlalchemy as sa

revision = '1a2b3c4d5e6f'
down_revision = 'cfc683876939'
branch_labels = None
depends_on = None

def upgrade() -> None:
    op.create_table('sso_configurations',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('institution_name', sa.String(), nullable=False),
    sa.Column('domain', sa.String(), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.Column('idp_entity_id', sa.String(), nullable=True),
    sa.Column('idp_sso_url', sa.String(), nullable=True),
    sa.Column('idp_x509_cert', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('institution_name')
    )
    op.create_index(op.f('ix_sso_configurations_domain'), 'sso_configurations', ['domain'], unique=True)
    op.create_index(op.f('ix_sso_configurations_id'), 'sso_configurations', ['id'], unique=False)

    op.create_table('user_memory',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('condensed_history', sa.Text(), nullable=True),
    sa.Column('last_updated', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('user_id')
    )
    
    op.add_column('questions', sa.Column('discipline', sa.String(), nullable=True))
    op.add_column('questions', sa.Column('upvotes', sa.Integer(), nullable=True))
    op.add_column('questions', sa.Column('downvotes', sa.Integer(), nullable=True))
    op.create_index(op.f('ix_questions_discipline'), 'questions', ['discipline'], unique=False)

def downgrade() -> None:
    op.drop_index(op.f('ix_questions_discipline'), table_name='questions')
    op.drop_column('questions', 'downvotes')
    op.drop_column('questions', 'upvotes')
    op.drop_column('questions', 'discipline')
    
    op.drop_table('user_memory')
    
    op.drop_index(op.f('ix_sso_configurations_id'), table_name='sso_configurations')
    op.drop_index(op.f('ix_sso_configurations_domain'), table_name='sso_configurations')
    op.drop_table('sso_configurations')