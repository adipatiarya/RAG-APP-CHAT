from sqlalchemy.ext.asyncio import AsyncSession

from app.models.document import Document
from app.repositories.cruds.crud import Crud

class EmbedCrud(Crud[Document]):
    def __init__(self, session: AsyncSession):
         super().__init__(session, Document)
    
    