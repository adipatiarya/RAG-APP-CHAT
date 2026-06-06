from sqlalchemy import text

from app.models.faq import Faq
from sqlalchemy.ext.asyncio import AsyncSession

class FaqService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def insert(self, content: str, embedding: list[float]):
        faq = Faq(content=content, embedding=embedding)
        self.session.add(faq)
        await self.session.commit()
        return faq

    async def delete(self, faq_id: int):
        faq = self.session.get(Faq, faq_id)
        if faq:
            self.session.delete(faq)
            self.session.commit()
            return True
        return False

    async def search(self, query_vector: list[float], top_k: int = 5):
        sql = text("""
            SELECT id, content
            FROM faq
            ORDER BY embedding <-> :vec
            LIMIT :top_k
        """)
        result = await self.session.execute(sql, {"vec": query_vector, "top_k": top_k})
        rows = result.fetchall()
        return rows