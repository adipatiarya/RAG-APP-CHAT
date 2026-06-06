import os

from sentence_transformers import SentenceTransformer
from huggingface_hub import snapshot_download

current_dir = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(current_dir, "all-MiniLM-L6-v2")
model = SentenceTransformer(model_path)

def get_embedding(text: str) -> list[float]:
    embedding = model.encode(text, batch_size=32).tolist()
    return embedding

def download_model() -> None:
    # download sekali ke folder lokal
    snapshot_download(
        repo_id="sentence-transformers/all-MiniLM-L6-v2",
        local_dir=model_path
    )