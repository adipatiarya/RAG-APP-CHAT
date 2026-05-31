from fastapi import FastAPI
from app.api.main import api_router
from app.core.config import settings
from app.core.exception import DuplicateEntryError
from app.exception import duplicate_entry_handler, global_exception_handler
from app.api.deps import AsyncSessionLocal, get_role_service

from app.seeders.role_permission import initial_permissions, initial_role, initial_user
async def lifespan(_):
    # Startup logic
    print("🚀 FastAPI server is starting...")
    # misalnya: buka koneksi DB, inisialisasi cache, dll
    async with AsyncSessionLocal() as session:
        await initial_permissions(session)
        role = await initial_role(session)
        await initial_user(session, role.name)
        print(f'Generated Superuser cek email and passwoord in .env')
    yield  # <-- di sini aplikasi berjalan

    # Shutdown logic
    print("🛑 FastAPI server is shutting down...")
    # misalnya: tutup koneksi DB, flush cache, dll


app = FastAPI(openapi_url=f"{settings.API_V1_STR}/openapi.json", lifespan=lifespan)


app.add_exception_handler(DuplicateEntryError, duplicate_entry_handler)
app.add_exception_handler(Exception, global_exception_handler)

app.include_router(api_router, prefix=settings.API_V1_STR)

# Lifespan context manager
