from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from typing import List
from app.schemas.audit import AuditCycleCreate, AuditCycleUpdate, AuditCycleResponse
from app.controllers.audit_controller import AuditController
from app.dependencies.database import get_db

router = APIRouter(prefix="/audits", tags=["Audits"])


@router.post("/", response_model=AuditCycleResponse)
async def create_audit_cycle(
        cycle_in: AuditCycleCreate, db: AsyncSession = Depends(get_db)):
    """Create an audit cycle and auto-populate audit findings."""
    return await AuditController.create_cycle(cycle_in, db)


@router.get("/", response_model=List[AuditCycleResponse])
async def get_audit_cycles(db: AsyncSession = Depends(get_db)):
    """List all audit cycles."""
    return await AuditController.get_cycles(db)


@router.get("/{cycle_id}", response_model=AuditCycleResponse)
async def get_audit_cycle(cycle_id: UUID, db: AsyncSession = Depends(get_db)):
    """Get a single audit cycle and its progress."""
    return await AuditController.get_cycle(cycle_id, db)


@router.patch("/{cycle_id}", response_model=AuditCycleResponse)
async def update_audit_cycle(
        cycle_id: UUID, cycle_in: AuditCycleUpdate, db: AsyncSession = Depends(get_db)):
    """Update metadata for an open audit cycle."""
    return await AuditController.update_cycle(cycle_id, cycle_in, db)


@router.patch("/{cycle_id}/close", response_model=AuditCycleResponse)
async def close_audit_cycle(
        cycle_id: UUID, db: AsyncSession = Depends(get_db)):
    """Close the audit cycle (fails if there are pending items)."""
    return await AuditController.close_cycle(cycle_id, db)
