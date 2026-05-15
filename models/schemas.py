from pydantic import BaseModel, Field
from typing import List

# Definition of the request from the user
class TextRequest(BaseModel):
    text: str = Field(
        ...,
        min_length=15,
        description="Text or script to be processed.",
    )

class SummarizedResponse(BaseModel):
    summary: str
    success: bool = True


class TitlesResponse(BaseModel):
    titles: List[str]
    success: bool = True


class HashtagsResponse(BaseModel):
    hashtags: List[str]
    success: bool = True


class TranslateResponse(BaseModel):
    translated: str
    success: bool = True