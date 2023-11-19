from datetime import datetime
from enum import Enum, unique

from pydantic import BaseModel


@unique
class CONTENT_TYPE(str, Enum):
    Plaintext = "text/plain"
    # Code = "text/code"
    # HTML = "text/html"
    # Markdown = "text/markdown"


class Paste(BaseModel):
    id: int
    title: str
    content_type: CONTENT_TYPE
    content: str
    creation_time: datetime
    author_id: int


class PasteView(BaseModel):
    id: int
    title: str
    author_id: int
    content_type: CONTENT_TYPE
    content: str


class PasteList(BaseModel):
    id: int
    author_id: int
    title: str
    content: str
    creation_time: datetime
