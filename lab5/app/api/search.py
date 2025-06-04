from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
import time
from app.db.session import get_db
from app.models.corpus import Corpus
from app.services.fuzzy_search import levenshtein_distance, damerau_levenshtein_distance
from app.celery import celery_app
from app.celery.tasks import fuzzy_search_task

from app.schemas.search_schemas import (
    AsyncSearchRequest,
    TaskLaunchResponse,
    TaskStatusResponse,
)

router = APIRouter(prefix="/search", tags=["Search"])

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
    corpus = await db.get(Corpus, corpus_id)
    if not corpus:
        raise HTTPException(status_code=404, detail="Корпус не найден")

    words = corpus.content.split()

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

    end_time = time.time()
    elapsed = end_time - start_time

    distances.sort(key=lambda x: x[1])
    result = distances[:10] # например, возьмем топ-10 самых близких слов

    return {
        "query": query,
        "algorithm": algorithm,
        "execution_time": elapsed,
        "top_matches": result
    }


@router.post(
    "/async",
    response_model=TaskLaunchResponse,
    summary="Старт асинхронного поиска (Celery)",
)
async def start_async_search(payload: AsyncSearchRequest):
    """
    Запускает задачу Celery и возвращает её `task_id`.
    """
    task = fuzzy_search_task.delay(
        payload.query,
        payload.algorithm,
        payload.corpus_id,
    )
    return {"task_id": task.id}


@router.get(
    "/tasks/{task_id}",
    response_model=TaskStatusResponse,
    summary="Статус / результат Celery-задачи",
)
async def get_task_status(task_id: str):
    """
    Проверяет состояние Celery-задачи и (если она завершена) отдаёт результат.
    """
    task = celery_app.AsyncResult(task_id)

    if task.state == "PENDING":
        return {"status": "PENDING", "result": None}

    if task.state == "FAILURE":
        # task.result содержит traceback, выводим кратко
        raise HTTPException(status_code=500, detail=str(task.result))

    # Для состояний STARTED, SUCCESS и т.д.
    return {"status": task.state, "result": task.result}