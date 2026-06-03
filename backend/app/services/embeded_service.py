from typing import Any

from sqlmodel import select

from app.repositories.embeded.embed_crud import EmbedCrud
from app.repositories.embeded.embed import get_embedding

from app.models.document import Document


class EmbededService:
     def __init__(self, embed: EmbedCrud ):
          self.embed  = embed

     async def chat(self, text: str):
          query_embed = get_embedding(text)
          result = await self.embed.session.execute(
               select(Document).order_by(Document.embedding.cosine_distance(query_embed)).limit(3)
          )
          docs = result.scalars().all()
          context = "\n".join([doc.content for doc in docs])
          return f"""
          Pertanyaan: {text}
          Dokumen terkait: {context} 
          Jawablah dengan bahasa yang sopan dan ringkas.
          """

