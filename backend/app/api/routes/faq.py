from fastapi import APIRouter, Path, Query, status
from app.api.deps import  CurrentUser, SessionDep
from app.models.faq import FaqCreate, FaqPublic


router = APIRouter(prefix="/faqs", tags=["Faq"])

@router.post("", 
    status_code=status.HTTP_201_CREATED, 
    response_model=FaqPublic,

)
async def create_faq(*, session: SessionDep, body: FaqCreate, current_user: CurrentUser) -> None:
  faq_in = FaqCreate(
    content='yes'
  )
  return FaqPublic(
    content=faq_in.content,
    project_name=faq_in.project_name
  )