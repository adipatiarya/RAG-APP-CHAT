import asyncio
import csv

from fastapi import APIRouter, File, Path, Query, UploadFile, status
from fastapi.responses import JSONResponse, StreamingResponse
from app.api.deps import  CurrentUser, SessionDep
from app.models.faq import Faq, FaqCreate, FaqPublic
from app.repositories.embeded.embed import get_embedding

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