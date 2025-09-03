from pydantic import BaseModel

class Request(BaseModel):
    url: str
    title: str
    description: str
    tags: list[str]
    category_id: str