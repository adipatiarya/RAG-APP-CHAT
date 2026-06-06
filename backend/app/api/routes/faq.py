from fastapi import APIRouter, Path, Query, status
from app.api.deps import  CurrentUser, SessionDep
from app.models.faq import FaqCreate, FaqPublic
from app.repositories.embeded.embed import get_embedding

router = APIRouter(prefix="/faqs", tags=["Faq"])

@router.post("", 
    status_code=status.HTTP_201_CREATED, 
    response_model=FaqPublic,

)
async def create_faq(*, session: SessionDep, body: FaqCreate, current_user: CurrentUser) -> None:
    
    embed = get_embedding(body.content)
    print(embed)
    
    return FaqPublic(
        content=body.content,
        project_name='tex'
  )