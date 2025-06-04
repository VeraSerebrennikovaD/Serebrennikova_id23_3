import time
from typing import Dict, List
from celery import shared_task
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy import create_engine

from app.models.corpus import Corpus
from app.services.fuzzy_search import (
    levenshtein_distance,
    damerau_levenshtein_distance,
)

engine = create_engine("sqlite:///./app/db/database.db")

@shared_task(bind=True)
def fuzzy_search_task(self, query: str, algorithm: str, corpus_id: int) -> Dict:
    start = time.perf_counter()

    with Session(engine) as session:
        corpus: Corpus | None = session.get(Corpus, corpus_id)
        if not corpus:
            return {"error": f"Corpus {corpus_id} not found"}

        words = corpus.content.split()
        distances: List[tuple[str, int]] = []

        fn = (
            levenshtein_distance
            if algorithm == "levenshtein"
            else damerau_levenshtein_distance
        )

        for w in words:
            distances.append((w, fn(query, w)))

    distances.sort(key=lambda x: x[1])
    result = distances[:10]

    return {
        "query": query,
        "algorithm": algorithm,
        "execution_time": round(time.perf_counter() - start, 3),
        "top_matches": result,
    }
