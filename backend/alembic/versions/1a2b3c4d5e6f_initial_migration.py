"""initial migration

Revision ID: 1a2b3c4d5e6f
Revises: 
Create Date: 2026-07-12 12:12:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '1a2b3c4d5e6f'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1. Create asset_categories table
    op.create_table(
        'asset_categories',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('description', sa.String(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_asset_categories_id'), 'asset_categories', ['id'], unique=False)
    op.create_index(op.f('ix_asset_categories_name'), 'asset_categories', ['name'], unique=True)

    # 2. Create departments table
    op.create_table(
        'departments',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('parent_department_id', sa.UUID(), nullable=True),
        sa.Column('head_user_id', sa.UUID(), nullable=True),
        sa.Column('status', sa.String(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_departments_id'), 'departments', ['id'], unique=False)
    op.create_index(op.f('ix_departments_name'), 'departments', ['name'], unique=True)

    # 3. Create users table
    op.create_table(
        'users',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('email', sa.String(), nullable=False),
        sa.Column('hashed_password', sa.String(), nullable=False),
        sa.Column('role', sa.String(), nullable=False),
        sa.Column('department_id', sa.UUID(), nullable=True),
        sa.Column('promoted_by', sa.UUID(), nullable=True),
        sa.Column('status', sa.String(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_id'), 'users', ['id'], unique=False)
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)

    # 4. Create assets table
    op.create_table(
        'assets',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('asset_tag', sa.String(length=20), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('serial_number', sa.String(length=255), nullable=True),
        sa.Column('category_id', sa.UUID(), nullable=False),
        sa.Column('current_status', sa.String(length=50), nullable=False),
        sa.Column('is_bookable', sa.Boolean(), nullable=False),
        sa.Column('custom_fields', postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.ForeignKeyConstraint(['category_id'], ['asset_categories.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('serial_number')
    )
    op.create_index(op.f('ix_assets_asset_tag'), 'assets', ['asset_tag'], unique=True)
    op.create_index(op.f('ix_assets_id'), 'assets', ['id'], unique=False)
    op.create_index(op.f('ix_assets_name'), 'assets', ['name'], unique=False)

    # 5. Create allocations table with partial unique index for active allocations
    op.create_table(
        'allocations',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('asset_id', sa.UUID(), nullable=False),
        sa.Column('employee_id', sa.UUID(), nullable=False),
        sa.Column('department_id', sa.UUID(), nullable=True),
        sa.Column('allocated_by_id', sa.UUID(), nullable=True),
        sa.Column('allocated_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('expected_return_date', sa.Date(), nullable=True),
        sa.Column('actual_return_date', sa.DateTime(timezone=True), nullable=True),
        sa.Column('return_condition', sa.String(length=100), nullable=True),
        sa.Column('return_notes', sa.Text(), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=False),
        sa.ForeignKeyConstraint(['asset_id'], ['assets.id'], ),
        sa.ForeignKeyConstraint(['department_id'], ['departments.id'], ),
        sa.ForeignKeyConstraint(['employee_id'], ['users.id'], ),
        sa.ForeignKeyConstraint(['allocated_by_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_allocations_id'), 'allocations', ['id'], unique=False)
    # Database-level guarantee that an asset can only have ONE active allocation at a time:
    op.create_index(
        'ix_active_allocation_per_asset',
        'allocations',
        ['asset_id'],
        unique=True,
        postgresql_where=sa.text('is_active = true')
    )

    # 6. Create maintenance_requests table
    op.create_table(
        'maintenance_requests',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('asset_id', sa.UUID(), nullable=False),
        sa.Column('raised_by_id', sa.UUID(), nullable=False),
        sa.Column('description', sa.Text(), nullable=False),
        sa.Column('priority', sa.String(length=20), nullable=False),
        sa.Column('status', sa.String(length=20), nullable=False),
        sa.Column('approved_by_id', sa.UUID(), nullable=True),
        sa.Column('technician_id', sa.UUID(), nullable=True),
        sa.Column('resolution_notes', sa.Text(), nullable=True),
        sa.Column('photo_url', sa.String(length=500), nullable=True),
        sa.Column('resolved_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['asset_id'], ['assets.id'], ),
        sa.ForeignKeyConstraint(['raised_by_id'], ['users.id'], ),
        sa.ForeignKeyConstraint(['approved_by_id'], ['users.id'], ),
        sa.ForeignKeyConstraint(['technician_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_maintenance_requests_id'), 'maintenance_requests', ['id'], unique=False)

    # 7. Create transfers table
    op.create_table(
        'transfers',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('asset_id', sa.UUID(), nullable=False),
        sa.Column('from_employee_id', sa.UUID(), nullable=False),
        sa.Column('to_employee_id', sa.UUID(), nullable=False),
        sa.Column('status', sa.String(length=20), nullable=False),
        sa.Column('requested_by_id', sa.UUID(), nullable=False),
        sa.Column('approved_by_id', sa.UUID(), nullable=True),
        sa.Column('reason', sa.Text(), nullable=False),
        sa.Column('resolved_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['asset_id'], ['assets.id'], ),
        sa.ForeignKeyConstraint(['from_employee_id'], ['users.id'], ),
        sa.ForeignKeyConstraint(['to_employee_id'], ['users.id'], ),
        sa.ForeignKeyConstraint(['requested_by_id'], ['users.id'], ),
        sa.ForeignKeyConstraint(['approved_by_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_transfers_id'), 'transfers', ['id'], unique=False)

    # 8. Add circular/interdependent foreign keys for users and departments
    op.create_foreign_key('fk_departments_parent_department', 'departments', 'departments', ['parent_department_id'], ['id'])
    op.create_foreign_key('fk_departments_head_user', 'departments', 'users', ['head_user_id'], ['id'])

    op.create_foreign_key('fk_users_department', 'users', 'departments', ['department_id'], ['id'])
    op.create_foreign_key('fk_users_promoted_by', 'users', 'users', ['promoted_by'], ['id'])


def downgrade() -> None:
    # Drop foreign keys first to avoid referential integrity violations
    op.drop_constraint('fk_users_promoted_by', 'users', type_='foreignkey')
    op.drop_constraint('fk_users_department', 'users', type_='foreignkey')
    op.drop_constraint('fk_departments_head_user', 'departments', type_='foreignkey')
    op.drop_constraint('fk_departments_parent_department', 'departments', type_='foreignkey')

    # Drop tables
    op.drop_index(op.f('ix_transfers_id'), table_name='transfers')
    op.drop_table('transfers')

    op.drop_index(op.f('ix_maintenance_requests_id'), table_name='maintenance_requests')
    op.drop_table('maintenance_requests')

    op.drop_index('ix_active_allocation_per_asset', table_name='allocations')
    op.drop_index(op.f('ix_allocations_id'), table_name='allocations')
    op.drop_table('allocations')

    op.drop_index(op.f('ix_assets_name'), table_name='assets')
    op.drop_index(op.f('ix_assets_id'), table_name='assets')
    op.drop_index(op.f('ix_assets_asset_tag'), table_name='assets')
    op.drop_table('assets')

    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_index(op.f('ix_users_id'), table_name='users')
    op.drop_table('users')

    op.drop_index(op.f('ix_departments_name'), table_name='departments')
    op.drop_index(op.f('ix_departments_id'), table_name='departments')
    op.drop_table('departments')

    op.drop_index(op.f('ix_asset_categories_name'), table_name='asset_categories')
    op.drop_index(op.f('ix_asset_categories_id'), table_name='asset_categories')
    op.drop_table('asset_categories')
