from pydantic import BaseModel

class CorpusBase(BaseModel):
    title: str
    content: str

class CorpusCreate(CorpusBase):
    pass

class CorpusOut(CorpusBase):
    id: int

    class Config:
        orm_mode = True
