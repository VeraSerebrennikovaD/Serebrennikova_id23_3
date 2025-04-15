# project/app/api/search.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
import time
from app.db.session import get_db
from app.models.corpus import Corpus
from app.services.fuzzy_search import levenshtein_distance, damerau_levenshtein_distance

router = APIRouter()

@router.post("/search_algorithm", summary = "Алгоритмы поиска")
async def search_algorithm(
    query: str,
    algorithm: str,
    corpus_id: int,
    db: AsyncSession = Depends(get_db)
):
    """
    query: слово, которое ищем
    algorithm: "levenshtein" или "damerau_levenshtein" (в примере)
    corpus_id: id корпуса
    """
    # Найдем корпус
    corpus = await db.get(Corpus, corpus_id)
    if not corpus:
        raise HTTPException(status_code=404, detail="Корпус не найден")

    # Разобьем на слова
    words = corpus.content.split()

    # Вызовем выбранный алгоритм
    start_time = time.time()
    distances = []
    if algorithm == "levenshtein":
        for w in words:
            dist = levenshtein_distance(query, w)
            distances.append((w, dist))
    elif algorithm == "damerau_levenshtein":
        for w in words:
            dist = damerau_levenshtein_distance(query, w)
            distances.append((w, dist))
    else:
        raise HTTPException(status_code=400, detail="Неизвестный алгоритм")

    # Посчитаем время
    end_time = time.time()
    elapsed = end_time - start_time

    # Найдем минимальное расстояние
    distances.sort(key=lambda x: x[1])
    result = distances[:10] # например, возьмем топ-10 самых близких слов

    return {
        "query": query,
        "algorithm": algorithm,
        "execution_time": elapsed,
        "top_matches": result
    }
