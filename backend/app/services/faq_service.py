from sqlalchemy import text, select, and_

from app.models.faq import Faq, FaqCreate
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.embeded.embed import get_embedding

class FaqService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def insert(self, faq_in: FaqCreate)-> Faq:
        faq = Faq.model_validate(faq_in, update={"embedding": get_embedding(faq_in.content)})
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
        """Search FAQ using vector similarity with pgvector"""
        # Convert list to pgvector string format
        vec_str = "[" + ",".join(map(str, query_vector)) + "]"
        
        # Using raw SQL dengan proper pgvector casting
        sql = text("""
            SELECT 
                id, 
                content,
                (1 - ((embedding <-> CAST(:vec AS vector))::float / 2)) as similarity_score
            FROM faq
            WHERE deleted_at IS NULL
            ORDER BY embedding <-> CAST(:vec AS vector)
            LIMIT :top_k
        """)
        result = await self.session.execute(sql, {"vec": vec_str, "top_k": top_k})
        rows = result.fetchall()
        return rows