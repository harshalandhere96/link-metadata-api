
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from app.extractor import MetadataError, extract_metadata

app = FastAPI(
    title="Link Metadata Extraction API",
    description="Extract metadata from publicly accessible webpages.",
    version="1.0.0",
)


class ExtractRequest(BaseModel):
    url: str = Field(
        ...,
        min_length=8,
        max_length=2048,
        description="Public HTTP or HTTPS webpage URL",
    )


@app.get("/")
def root():
    return {
        "message": "Link Metadata Extraction API",
        "docs": "/docs",
        "health": "/health",
    }


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.post("/extract")
def extract(request: ExtractRequest):
    try:
        return extract_metadata(request.url)
    except MetadataError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
