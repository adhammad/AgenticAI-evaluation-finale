"""Telecharge les 4 PDF de la base documentaire informatique dans
data/pdfs_informatique/.

Lancer avec : uv run python download_pdfs.py
"""
import urllib.request
from pathlib import Path

PDF_DIR = Path(__file__).resolve().parent / "data" / "pdfs_informatique"

SOURCES = {
    "informatique_fondamentaux.pdf": (
        "https://fr.wikipedia.org/api/rest_v1/page/pdf/Informatique"
    ),
    "algorithmes.pdf": (
        "https://fr.wikipedia.org/api/rest_v1/page/pdf/Algorithme"
    ),
    "reseaux_informatiques.pdf": (
        "https://fr.wikipedia.org/api/rest_v1/page/pdf/R%C3%A9seau_informatique"
    ),
    "bases_de_donnees.pdf": (
        "https://fr.wikipedia.org/api/rest_v1/page/pdf/Base_de_donn%C3%A9es"
    ),
}


def download_all() -> None:
    PDF_DIR.mkdir(parents=True, exist_ok=True)
    for filename, url in SOURCES.items():
        dest = PDF_DIR / filename
        if dest.exists():
            print(f"OK (deja present) : {filename}")
            continue
        request = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(request, timeout=60) as response:
            dest.write_bytes(response.read())
        size_kb = dest.stat().st_size / 1024
        print(f"Telecharge : {filename} ({size_kb:.0f} KB)")


if __name__ == "__main__":
    download_all()
