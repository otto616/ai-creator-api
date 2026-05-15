from fastapi import APIRouter, HTTPException, Request
from models.schemas import TextRequest, SummarizedResponse, TitlesResponse, HashtagsResponse, TranslateResponse
from services.huggingface_service import sum_text_with_ai, generate_viral_titles, generate_hashtags, translate_english
from limiter import limiter

# Router creation
router = APIRouter()

@router.post("/summarize", response_model=SummarizedResponse)
@limiter.limit("8/minute")
def create_summary(request: TextRequest, body: TextRequest):
    try:
        # Validated text by Pydantic to our AI sum func.
        result_text = sum_text_with_ai(body.text)
        return SummarizedResponse(summary=result_text, success=True)
    except Exception as e:
        # If something fails with Hugging Face, error
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/titles", response_model=TitlesResponse)
@limiter.limit("8/minute")
def create_viral_titles(request: TextRequest, body: TextRequest):
    try:
        # Re-use TextRequest for Pydantic validation
        result_titles = generate_viral_titles(body.text)
        return TitlesResponse(titles=result_titles, success=True)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/hashtags", response_model=HashtagsResponse)
@limiter.limit("8/minute")
def create_hashtags(request: TextRequest, body: TextRequest):
    try:
        result_hashtags = generate_hashtags(body.text)
        return HashtagsResponse(hashtags=result_hashtags, success=True)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/translate", response_model=TranslateResponse)
@limiter.limit("8/minute")
def create_translate(request: TextRequest, body: TextRequest):
    try:
        result_translated = translate_english(body.text)
        return TranslateResponse(translated=result_translated, success=True)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
