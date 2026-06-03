from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.embeded.embed import get_embedding
from app.models.document import DocumentCreate, Document
from app.api.deps import get_embeded_service

dummy_answers = [
    "Untuk daftar ulang siswa, silakan ke ruang TU dengan membawa formulir.",
    "Jam operasional sekolah adalah pukul 07.00 sampai 15.00.",
    "Ujian Matematika dijadwalkan hari Senin minggu depan.",
    "Pembayaran SPP dilakukan setiap tanggal 10 di bank mitra.",
    "Perpustakaan buka setiap hari kerja kecuali Jumat sore.",
    "Guru wali kelas dapat dihubungi melalui WhatsApp resmi sekolah.",
    "Pengambilan rapor dilakukan di aula pada akhir semester.",
    "Kegiatan ekstrakurikuler dimulai pukul 15.30 setelah jam pelajaran.",
    "Surat izin sakit harus ditandatangani orang tua dan diserahkan ke TU.",
    "Pendaftaran lomba cerdas cermat ditutup pada tanggal 20 bulan ini."
]

async def initial_answers(sess: AsyncSession):
    for ans in dummy_answers:
        doc_in = DocumentCreate(content=ans)
        embed = get_embedding(ans)
        user_model = Document.model_validate(doc_in, update={"embedding":embed})

        service = get_embeded_service(sess)
        await service.embed.add(user_model)
    print('Model inserted')
