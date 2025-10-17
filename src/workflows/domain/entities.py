from pydantic import BaseModel
from typing import Dict, Any, List, Optional

class Event(BaseModel):
    title: str
    appoinment_datetime: str
    description: Optional[str] = None
    attendees: List[str]

class EmbeddingConfig(BaseModel):
    model_name: str = "text-embedding-3-large"
    distance_metric: str = "cosine"
    vector_size: int = 3072  

class SearchResult(BaseModel):
    text: str
    metadata: Dict[str, Any]
    score: float
