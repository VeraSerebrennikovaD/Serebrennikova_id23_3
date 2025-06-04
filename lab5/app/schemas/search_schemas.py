from pydantic import BaseModel
from typing import Optional, Dict

class AsyncSearchRequest(BaseModel):
    query: str
    algorithm: str
    corpus_id: int

class TaskLaunchResponse(BaseModel):
    task_id: str

class TaskStatusResponse(BaseModel):
    status: str
    result: Optional[Dict] = None