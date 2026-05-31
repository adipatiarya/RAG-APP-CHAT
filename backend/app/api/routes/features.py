
from typing import Dict

from fastapi import APIRouter
from pydantic import BaseModel
from app.utils import all_perms
from app.api.deps import SessionDep, get_role_service

router = APIRouter(tags=["Features"], prefix="/permissions")

class Resp(BaseModel):
    permissions:Dict[str, Dict[str,bool]] = all_perms()

@router.get("", response_model=Resp)
async def permissions(sess: SessionDep) -> None:

   service = get_role_service(sess)
   
   all_perms = await service.permission_crud.list_all()
   
   temp = []

   for p in all_perms:
       x = p.name.split("_")
       temp.append(x[2])     
   modules = list(set(temp))
   
   datax= {
        resource: {f"can_{action}_{resource}": False for action in ['create','view','update','delete']}
        for resource in modules
    }
   return Resp (
        permissions=datax
    )