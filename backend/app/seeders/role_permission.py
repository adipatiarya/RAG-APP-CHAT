
from app.api.deps import get_user_service, get_role_service
from app.models.user import UserCreate, UserUpdate
from app.models.role import RoleCreate
from app.core.config import settings
from sqlalchemy.ext.asyncio import AsyncSession

from app.utils import all_perms

async def initial_permissions(sess: AsyncSession):
    serv = get_role_service(sess)
    result = []
    for _, perms in all_perms().items():
        for perm_name, _ in perms.items():
           dat = await serv.permission_crud.get_by_name_or_id(perm_name)
           if not dat:
               result.append(perm_name)
    print(f"Permission updated {len(result)}")

    await serv.create_permissions(result)
 

async def initial_role(sess: AsyncSession):
    result = []
    
    default_role = settings.DEFAULT_ROLE
    service = get_role_service(sess)
    
    perms = await service.permission_crud.list_all()
    for p in perms:
        result.append(p.name)

    role = await service.role_crud.get_by_name_or_id(default_role)
    if role is None:
        print(f"Role {default_role} akan dibuat")
        role_in = RoleCreate(name=default_role, permission_strs=result, description='Ini adalah role superuser')
        role = await service.create_role(role_in)
    return role
   
async def initial_user(sess: AsyncSession, role_name):
    default_email = settings.FIRST_SUPERUSER
    default_password = settings.FIRST_SUPERUSER_PASSWORD 
    service_user = get_user_service(sess)
    user = await service_user.user_crud.get_by_email(default_email)
    if user is None:
        print('Create user')
        user_in = UserCreate(email=default_email, password=default_password, role=role_name, is_superuser=True)
        user = await service_user.create_user(user_in)
    user_in = UserUpdate(email=default_email, password=default_password, role=role_name, is_superuser=True)
    user = await service_user.update_user(user, user_in)
    return user