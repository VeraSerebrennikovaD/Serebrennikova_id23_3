from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.db.session import get_db
from app.models.corpus import Corpus
from app.schemas.corpus_schemas import CorpusCreate, CorpusOut

router = APIRouter()

@router.post("/upload_corpus", response_model=CorpusOut, summary = "Создать новый корпус")
async def upload_corpus(corpus_data: CorpusCreate, db: AsyncSession = Depends(get_db)):
    """
    Загружает новый корпус в базу данных.
    """
    try:
        new_corpus = Corpus(title=corpus_data.title, content=corpus_data.content)
        db.add(new_corpus)
        await db.commit()
        await db.refresh(new_corpus)
        return new_corpus
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Ошибка при добавлении корпуса: {str(e)}")

@router.get("/corpuses", response_model=list[CorpusOut], summary = "Вывести корпуса")
async def get_corpuses(db: AsyncSession = Depends(get_db)):
    """
    Возвращает список всех корпусов.
    """
    result = await db.execute(select(Corpus))
    corpuses = result.scalars().all()
    return corpuses