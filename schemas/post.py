from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class PostIn(BaseModel):
    title: str
    content: str
    published: bool = True
    published_at: Optional[datetime] = None


class PostUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    published: Optional[bool] = None
    published_at: Optional[datetime] = None
