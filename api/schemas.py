from pydantic import BaseModel
from typing import List, Optional

class TopProduct(BaseModel):
    product_name: str
    mentions: int

class ChannelActivity(BaseModel):
    date: str
    message_count: int
    avg_views: Optional[float]

class MessageSearchResult(BaseModel):
    message_id: int
    channel_name: str
    message_text: str
    message_date: str

class VisualContentStat(BaseModel):
    channel_name: str
    total_images: int
    promotional: int
    product_display: int
    lifestyle: int
    other: int
