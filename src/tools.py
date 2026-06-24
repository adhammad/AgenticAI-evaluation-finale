from pathlib import Path

from langchain.tools import tool

from src.config import RETRIEVAL_K
from src.vectorstore import get_vectorstore


@tool
def classify_technical_domain(query: str) -> dict:
    """Classe une question d'informatique selon son domaine technique.

    Args:
        query: la question ou les mots-cles a analyser.
    """
    normalized = query.lower()
    domains = {
        "programmation": ["code", "programme", "programmation", "python", "java", "javascript"],
        "algorithmique": ["algorithme", "complexite", "pseudocode", "tri", "recherche"],
        "bases_de_donnees": ["base de donnees", "sql", "nosql", "postgres", "mysql", "index"],
        "systemes": ["systeme", "os", "linux", "windows", "processus", "memoire"],
        "reseaux": ["reseau", "tcp", "udp", "ip", "dns", "http", "socket"],
        "cybersecurite": ["securite", "cyber", "malware", "chiffrement", "authentification", "attaque"],
        "debogage": ["erreur", "bug", "debogage", "trace", "exception", "stack trace"],
        "cloud": ["cloud", "aws", "azure", "gcp", "deploiement", "containers"],
    }
    scores = {
        domain: sum(1 for keyword in keywords if keyword in normalized)
        for domain, keywords in domains.items()
    }
    best_domain = max(scores, key=scores.get)
    if scores[best_domain] == 0:
        best_domain = "general"
    matched_keywords = [
        keyword
        for keywords in domains.values()
        for keyword in keywords
        if keyword in normalized
    ]
    return {
        "domain": best_domain,
        "matched_keywords": matched_keywords,
        "scores": scores,
    }


@tool
def extract_technical_keywords(query: str) -> list[str]:
    """Extrait les mots-cles techniques Informatique d'une question.

    Args:
        query: la question ou la requete utilisateur.
    """
    normalized = query.lower()
    keywords = [
        "python",
        "java",
        "javascript",
        "algorithm",
        "algorithme",
        "sql",
        "nosql",
        "database",
        "base de donnees",
        "reseau",
        "tcp",
        "udp",
        "linux",
        "windows",
        "cloud",
        "api",
        "securite",
        "cybersecurite",
        "debug",
        "bug",
        "exception",
        "docker",
        "git",
    ]
    return [keyword for keyword in keywords if keyword in normalized]


@tool
def retrieve_documents(query: str) -> str:
    """Recherche dans la base documentaire d'informatique les passages les plus
    pertinents pour une question.

    Args:
        query: la question ou les mots-cles a rechercher.
    """
    vectorstore = get_vectorstore()
    docs = vectorstore.similarity_search(query, k=RETRIEVAL_K)
    if not docs:
        return "Aucun document pertinent trouve."
    formatted = []
    for doc in docs:
        source = Path(doc.metadata.get("source", "inconnu")).name
        page = doc.metadata.get("page", "?")
        formatted.append(f"[Source: {source}, page {page}]\n{doc.page_content}")
    return "\n\n---\n\n".join(formatted)


TOOLS = [retrieve_documents, classify_technical_domain, extract_technical_keywords]
TOOLS_BY_NAME = {t.name: t for t in TOOLS}
