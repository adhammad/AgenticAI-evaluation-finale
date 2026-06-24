import pytest

from src.tools import classify_technical_domain, extract_technical_keywords


def test_classify_technical_domain_programming():
    result = classify_technical_domain.invoke({"query": "Comment debugger du code Python ?"})
    assert result["domain"] == "programmation"
    assert "python" in result["matched_keywords"]


def test_classify_technical_domain_networks():
    result = classify_technical_domain.invoke({"query": "Explique TCP et UDP dans un reseau"})
    assert result["domain"] == "reseaux"
    assert result["scores"]["reseaux"] > 0


def test_extract_technical_keywords_finds_matches():
    result = extract_technical_keywords.invoke({"query": "API REST avec Python et SQL"})
    assert "python" in result
    assert "sql" in result


def test_extract_technical_keywords_empty_when_no_match():
    result = extract_technical_keywords.invoke({"query": "Quel est le meilleur sport ?"})
    assert result == []
