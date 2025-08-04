"""Initial schema

Revision ID: cfc683876939
Revises: 
Create Date: 2025-08-03 14:26:13.123456

"""
from alembic import op
import sqlalchemy as sa

revision = 'cfc683876939'
down_revision = None
branch_labels = None
depends_on = None

def upgrade() -> None:
    op.create_table('questions',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('content', sa.Text(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_questions_id'), 'questions', ['id'], unique=False)
    
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    op.create_index(op.f('ix_users_id'), 'users', ['id'], unique=False)
    
    op.create_table('identities',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('provider', sa.String(), nullable=False),
    sa.Column('provider_user_id', sa.String(), nullable=False),
    sa.Column('password_hash', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('provider_user_id')
    )
    op.create_index(op.f('ix_identities_id'), 'identities', ['id'], unique=False)

    op.create_table('responses',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('question_id', sa.Integer(), nullable=False),
    sa.Column('user_answer', sa.Text(), nullable=False),
    sa.Column('is_correct', sa.Boolean(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['question_id'], ['questions.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_responses_id'), 'responses', ['id'], unique=False)

def downgrade() -> None:
    op.drop_index(op.f('ix_responses_id'), table_name='responses')
    op.drop_table('responses')
    op.drop_index(op.f('ix_identities_id'), table_name='identities')
    op.drop_table('identities')
    op.drop_index(op.f('ix_users_id'), table_name='users')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_table('users')
    op.drop_index(op.f('ix_questions_id'), table_name='questions')
    op.drop_table('questions')