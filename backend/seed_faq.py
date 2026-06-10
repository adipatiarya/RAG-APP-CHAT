import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.core.config import settings
from app.models.faq import FaqCreate

from app.repositories.embeded.embed import get_embedding
from app.services.faq_service import FaqService
from app.api.deps import AsyncSessionLocal


# Dummy FAQ data tentang toko baju
FAQ_DATA = [
    {
        "content": "Berapa jam operasional toko kami? Toko baju kami buka setiap hari dari jam 10 pagi sampai jam 9 malam. Kami tutup pada hari Tahun Baru dan Hari Raya."
    },
    {
        "content": "Apakah toko menerima pembayaran dengan kartu kredit? Ya, kami menerima semua jenis kartu kredit utama termasuk Visa, Mastercard, dan American Express. Kami juga menerima transfer bank dan e-wallet."
    },
    {
        "content": "Bagaimana kebijakan pengembalian barang? Anda dapat mengembalikan barang dalam waktu 14 hari setelah pembelian. Barang harus dalam kondisi asli dengan tag masih terpasang dan kwitansi pembelian."
    },
    {
        "content": "Apakah ada layanan tailoring di toko? Ya, kami menyediakan layanan tailoring profesional. Biaya mulai dari Rp 50.000 hingga Rp 200.000 tergantung jenis penyesuaian. Waktu pengerjaan sekitar 7-10 hari kerja."
    },
    {
        "content": "Bagaimana cara bergabung dengan program loyalitas kami? Daftar gratis di kasir atau melalui aplikasi mobile kami. Dapatkan 1 poin untuk setiap Rp 1.000 yang dibelanjakan dan tukarkan poin dengan diskon atau produk gratis."
    },
    {
        "content": "Apakah ada diskon untuk pembelian dalam jumlah besar? Ya, kami menawarkan diskon khusus untuk pembelian grosir mulai dari 10 item atau lebih. Hubungi manajer toko untuk mendapatkan harga grosir terbaik."
    },
    {
        "content": "Bagaimana dengan ukuran pakaian? Kami memiliki ukuran dari XS hingga XXXL untuk sebagian besar produk. Kami juga menyediakan layanan custom size untuk produk tertentu dengan pesanan minimal 5 item."
    },
    {
        "content": "Apakah produk kami asli dan berkualitas? Semua produk kami 100% original dan bergaransi keaslian. Kami bekerja sama dengan brand ternama dan distributor resmi untuk memastikan kualitas terbaik."
    },
    {
        "content": "Bagaimana cara tracking pesanan online? Setiap pesanan online akan diberikan nomor tracking yang dapat dipantau melalui website kami atau aplikasi mobile dalam 24 jam setelah checkout."
    },
    {
        "content": "Apakah ada biaya pengiriman? Untuk pembelian di atas Rp 500.000, pengiriman gratis ke seluruh Jakarta. Untuk kota lain ada biaya pengiriman yang berbeda tergantung lokasi, mulai dari Rp 25.000 hingga Rp 150.000."
    }
]


async def seed_faq():
    """Seed dummy FAQ data dengan embedding"""
    
    async with AsyncSessionLocal() as session:
        faq_service = FaqService(session)
        
        for faq in FAQ_DATA:
            content = faq["content"]
            faq_create = FaqCreate(content=content, project_name="toko_baju")
            #print(f"Processing FAQ: {faq_create.content}")
            data = await faq_service.insert(faq_create)
            print(f"Inserted FAQ with ID: {data.id} and content")     


if __name__ == "__main__":
    asyncio.run(seed_faq())
