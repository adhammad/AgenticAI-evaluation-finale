import pytest

from src.config import CHROMA_DIR, PDF_DIR
from src.tools import retrieve_documents

pytestmark = pytest.mark.skipif(
    not CHROMA_DIR.exists()
    or not PDF_DIR.exists()
    or not any(PDF_DIR.glob("*.pdf")),
    reason="Corpus ou vectorstore Informatique manquant (lancez download_pdfs.py puis ingest.py)",
)


def test_retrieve_documents_returns_sourced_passages():
    result = retrieve_documents.invoke({"query": "Qu'est-ce qu'un algorithme ?"})
    assert "Source:" in result
    assert len(result) > 0
