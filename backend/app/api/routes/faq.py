import asyncio
import csv
import json

from fastapi import APIRouter, File, Path, Query, UploadFile, status, WebSocket, WebSocketDisconnect, Depends
from fastapi.responses import JSONResponse, StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.deps import CurrentUser, SessionDep, get_db
from app.models.faq import Faq, FaqCreate, FaqPublic
from app.repositories.embeded.embed import get_embedding
from app.services.faq_service import FaqService
from openai import OpenAI
from app.core.config import settings

# Initialize OpenAI client
llm_client = OpenAI(api_key=settings.OPENAI_API_KEY)

router = APIRouter(prefix="/faqs", tags=["Faq"])

async def process_csv(file: UploadFile, session: SessionDep, current_user: CurrentUser):
    contents = await file.read()
    decoded = contents.decode("utf-8").splitlines()
    reader = csv.DictReader(decoded)
    total = sum(1 for _ in reader)  # hitung total baris
    decoded = contents.decode("utf-8").splitlines()
    reader = csv.DictReader(decoded)
    
    for i, row in enumerate(reader, start=1):
        content = row.get("content")
        if content:
            embed = get_embedding(content)
            print('Prosess')

        # kirim progres ke client
        progress = int(i / total * 100)
        yield f"data: {progress}\n\n"
        await asyncio.sleep(0)  # biar non-blocking


@router.post("/upload", status_code=status.HTTP_201_CREATED)
async def upload_faq_csv_stream(
    *,
    session: SessionDep,
    current_user: CurrentUser,
    file: UploadFile = File(...)
):
    if not file.filename.endswith(".csv"):
        return StreamingResponse(iter(["data: error\n\n"]), media_type="text/event-stream")

    return StreamingResponse(
        process_csv(file, session, current_user),
        media_type="text/event-stream"
    )

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


@router.websocket("/chat")
async def websocket_chat(websocket: WebSocket, session: SessionDep):
    await websocket.accept()
    faq_service = FaqService(session)
    
    try:
        while True:
            data = await websocket.receive_text()
            
            # Generate embedding dari input user
            embedding = get_embedding(data)
            
            # Search FAQ yang mirip (RAG)
            relevant_faqs = await faq_service.search(embedding, top_k=3)
            
            # Format FAQs untuk prompt
            faqs_context = "\n\n".join([
                f"Q: {faq[1]}\nScore: {faq[2]:.2%}" 
                for faq in relevant_faqs
            ]) if relevant_faqs else "Tidak ada FAQ yang relevan"
            
            # Buat system prompt dengan tone santai
            system_prompt = f"""Halo! 👋 Aku adalah assistant untuk toko baju kamu. 
Aku siap membantu menjawab semua pertanyaanmu tentang toko, produk, jam operasional, pembayaran, dan lainnya.

Berdasarkan FAQ di bawah ini, coba jawab pertanyaan dengan santai, ramah, dan jelas ya. Kalau ada yang kurang jelas, tanyakan lagi!

FAQ:
{faqs_context}"""
            # Call OpenAI API
            try:
                llm_response = llm_client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": data}
                    ],
                    temperature=0.7,
                    max_tokens=500
                )
                answer = llm_response.choices[0].message.content
                
            except Exception as e:
                answer = f"Error calling LLM: {str(e)}"
            
            # # Format response
            # response = {
            #     "user_query": data,
            #     "answer": answer,
            #     "relevant_faqs": [
            #         {
            #             "id": str(faq[0]),  # Convert UUID to string
            #             "content": faq[1],
            #             "similarity_score": round(faq[2], 2)
            #         }
            #         for faq in relevant_faqs
            #     ] if relevant_faqs else [],
            #     "faq_count": len(relevant_faqs) if relevant_faqs else 0
            # }
            
            await websocket.send_text(answer)
            
    except WebSocketDisconnect:
        pass