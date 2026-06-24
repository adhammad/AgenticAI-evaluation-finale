# Evaluation finale - Agentic RAG (Informatique)

Systeme RAG agentique construit avec LangGraph (sans `create_agent`), sur le
theme de l'informatique : programmation, algorithmes, systemes, reseaux,
bases de donnees, debogage et cybersecurite.

## Stack

- LLM : Ollama local `llama3.2:3b`
- Embeddings : HuggingFace `sentence-transformers/all-MiniLM-L6-v2`
- Vectorstore : Chroma (persiste dans `data/chroma_db/`)
- Orchestration : LangGraph (`StateGraph`)

## Installation

```bash
uv sync --group dev
```

Assurez-vous qu'Ollama est lance et que le modele est disponible :

```bash
ollama serve
ollama pull llama3.2:3b
```

## Base documentaire

4 guides publics sur un corpus documentaire specialise en informatique :

```bash
uv run python download_pdfs.py   # telecharge les PDF dans data/pdfs_informatique/
uv run python ingest.py          # construit le vectorstore Chroma
```

## Utilisation

```bash
uv run python main.py
```

Chat interactif avec memoire conversationnelle (un `thread_id` par session).

## Architecture du graphe

```bash
uv run python generate_graph.py
```

Genere `graph.mmd` (et `graph.png` si internet disponible). Le graphe suit le
pattern Agentic RAG retrieve -> grade -> generate/rewrite :

- `agent` : le LLM decide d'appeler `retrieve_documents` ou de repondre.
- `tools` : execute les outils demandes.
- `grade_documents` : evalue la pertinence des documents recuperes.
- `rewrite_query` : reformule la question si les documents ne sont pas
  pertinents (jusqu'a 2 fois), puis retourne a `agent`.

La memoire conversationnelle est assuree par un `InMemorySaver` (checkpointer)
indexe par `thread_id`.

## Outils

- `classify_technical_domain(query)` : identifie le domaine technique dominant.
- `extract_technical_keywords(query)` : extrait les mots-cles Informatique d'une question.
- `retrieve_documents(query)` : recherche semantique dans la base documentaire.

## Tests

```bash
uv run pytest -v
```

## Evaluation

```bash
uv run python -m evaluation.run_evaluation
```

Execute 10 questions simples + 10 questions complexes, mesure le temps de
reponse et enregistre les sources recuperees dans
`evaluation/results/results.csv`.
