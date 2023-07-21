import os
from fastapi import FastAPI, status, Depends, HTTPException, Header, Response

def get_api_key(
    api_key: str = Header(None),
):
    if api_key != os.environ.get("API_KEY"):
        raise HTTPException(status_code=400, detail="Invalid API Key")
    return api_key