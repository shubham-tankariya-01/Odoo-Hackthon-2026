from typing import List, Tuple
from uuid import UUID
from app.schemas.department import DepartmentCreate, DepartmentUpdate
from app.models.department import Department
from app.repositories.department_repository import DepartmentRepository
from app.repositories.user_repository import UserRepository
from app.utils.exceptions import ConflictException, NotFoundException, ValidationException
from app.utils.constants import DepartmentStatus

class DepartmentService:
    def __init__(self, dept_repo: DepartmentRepository, user_repo: UserRepository):
        self.dept_repo = dept_repo
        self.user_repo = user_repo

    async def get_all(self, status: str = None, skip: int = 0, limit: int = 100) -> Tuple[List[dict], int]:
        # For simplicity, returning raw models directly in real app we might construct the rich response
        departments = await self.dept_repo.get_all(skip, limit)
        total = len(departments) # Simple length for hackathon
        
        result = []
        for dept in departments:
            if status and dept.status != status:
                continue
            head_user = await self.user_repo.get_by_id(dept.head_user_id) if dept.head_user_id else None
            children = await self.dept_repo.get_children(dept.id)
            member_count = await self.dept_repo.get_member_count(dept.id)
            
            result.append({
                "id": dept.id,
                "name": dept.name,
                "parent_department_id": dept.parent_department_id,
                "head_user_id": dept.head_user_id,
                "head_name": head_user.name if head_user else None,
                "status": dept.status,
                "child_departments": [{"id": c.id, "name": c.name} for c in children],
                "member_count": member_count,
                "created_at": dept.created_at,
                "updated_at": dept.updated_at
            })
        return result, total

    async def get_by_id(self, dept_id: UUID) -> dict:
        dept = await self.dept_repo.get_by_id(dept_id)
        if not dept:
            raise NotFoundException("Department not found")
            
        head_user = await self.user_repo.get_by_id(dept.head_user_id) if dept.head_user_id else None
        children = await self.dept_repo.get_children(dept.id)
        member_count = await self.dept_repo.get_member_count(dept.id)
        
        return {
            "id": dept.id,
            "name": dept.name,
            "parent_department_id": dept.parent_department_id,
            "head_user_id": dept.head_user_id,
            "head_name": head_user.name if head_user else None,
            "status": dept.status,
            "child_departments": [{"id": c.id, "name": c.name} for c in children],
            "member_count": member_count,
            "created_at": dept.created_at,
            "updated_at": dept.updated_at
        }

    async def create(self, data: DepartmentCreate) -> Department:
        existing = await self.dept_repo.get_by_name(data.name)
        if existing:
            raise ConflictException("Department name already exists")
            
        if data.head_user_id:
            head = await self.user_repo.get_by_id(data.head_user_id)
            if not head or head.status != "active":
                raise ValidationException("Invalid or inactive head user")
                
        if data.parent_department_id:
            parent = await self.dept_repo.get_by_id(data.parent_department_id)
            if not parent:
                raise ValidationException("Invalid parent department")
                
        dept_in = data.model_dump(exclude_unset=True)
        return await self.dept_repo.create(dept_in)

    async def update(self, dept_id: UUID, data: DepartmentUpdate) -> Department:
        dept = await self.dept_repo.get_by_id(dept_id)
        if not dept:
            raise NotFoundException("Department not found")
            
        if data.name and data.name != dept.name:
            existing = await self.dept_repo.get_by_name(data.name)
            if existing:
                raise ConflictException("Department name already exists")
                
        if data.head_user_id:
            head = await self.user_repo.get_by_id(data.head_user_id)
            if not head or head.status != "active":
                raise ValidationException("Invalid or inactive head user")
                
        if data.parent_department_id:
            if data.parent_department_id == dept_id:
                raise ValidationException("Department cannot be its own parent")
            parent = await self.dept_repo.get_by_id(data.parent_department_id)
            if not parent:
                raise ValidationException("Invalid parent department")
                
        if data.status == DepartmentStatus.INACTIVE:
            # Check for active users/allocations - for hackathon, just active users
            count = await self.dept_repo.get_member_count(dept.id)
            if count > 0:
                raise ConflictException(f"Cannot deactivate department with {count} active users")
                
        dept_in = data.model_dump(exclude_unset=True)
        return await self.dept_repo.update(dept, dept_in)
