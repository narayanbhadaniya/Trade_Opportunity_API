from fastapi import FastAPI, Request, HTTPException, Header
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.middleware import SlowAPIMiddleware
from slowapi.errors import RateLimitExceeded
from fastapi.responses import JSONResponse
from app.services.data_fetcher import fetch_news
from app.services.ai_analyzer import analyze_with_ai
from app.utils.auth import verify_token  
from app.storage.memory_store import sessions



app = FastAPI()

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_middleware(SlowAPIMiddleware)

@app.exception_handler(RateLimitExceeded)
async def rate_limit_handler(request, exc):
    return JSONResponse(
        status_code=429,
        content={"detail": "Rate limit exceeded"}
    )

@app.get("/analyze/{sector}")
@limiter.limit("5/minute")
async def analyze(request: Request, sector: str, token: str = Header(...)):


    if not sector.isalpha():
        raise HTTPException(status_code=400, detail="Invalid sector")

    try:
        payload = verify_token(token)
        user = payload.get("user", "guest")
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")

    if user not in sessions:
        sessions[user] = {
            "requests": 0
        }

    sessions[user]["requests"] += 1

    print(f"User: {user}, Requests: {sessions[user]['requests']}")

    news = await fetch_news(sector)

    if not news:
        raise HTTPException(status_code=404, detail="No data found")

    report = await analyze_with_ai(sector, news)

    return {
        "sector": sector,
        "user": user,
        "requests_made": sessions[user]["requests"],
        "report": report
    }