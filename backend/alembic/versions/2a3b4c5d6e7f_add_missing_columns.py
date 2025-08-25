"""Add missing columns: options and feedback

Revision ID: 2a3b4c5d6e7f
Revises: 1a2b3c4d5e6f
Create Date: 2025-08-25 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

revision = '2a3b4c5d6e7f'
down_revision = '1a2b3c4d5e6f'
branch_labels = None
depends_on = None

def upgrade() -> None:
    # Add missing columns to questions table
    op.add_column('questions', sa.Column('options', sa.Text(), nullable=True))
    op.add_column('questions', sa.Column('topics', sa.Text(), nullable=True))
    op.add_column('questions', sa.Column('disciplines', sa.Text(), nullable=True))
    op.add_column('questions', sa.Column('body_systems', sa.Text(), nullable=True))
    op.add_column('questions', sa.Column('specialties', sa.Text(), nullable=True))
    op.add_column('questions', sa.Column('question_type', sa.String(), nullable=True))
    op.add_column('questions', sa.Column('age_group', sa.String(), nullable=True))
    op.add_column('questions', sa.Column('acuity', sa.String(), nullable=True))
    op.add_column('questions', sa.Column('pathophysiology', sa.Text(), nullable=True))
    
    # Add missing column to responses table
    op.add_column('responses', sa.Column('feedback', sa.Text(), nullable=True))

def downgrade() -> None:
    # Remove added columns
    op.drop_column('responses', 'feedback')
    op.drop_column('questions', 'pathophysiology')
    op.drop_column('questions', 'acuity')
    op.drop_column('questions', 'age_group')
    op.drop_column('questions', 'question_type')
    op.drop_column('questions', 'specialties')
    op.drop_column('questions', 'body_systems')
    op.drop_column('questions', 'disciplines')
    op.drop_column('questions', 'topics')
    op.drop_column('questions', 'options')