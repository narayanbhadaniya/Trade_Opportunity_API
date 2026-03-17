import httpx


async def fetch_news(sector: str):
    # fallback mock data (reliable)
    news = [
        f"Recent 2025 reports show {sector} sector growth in India",
        f"Investments in {sector} industry are decreasing rapidly"
    ]

    print("NEWS:", news)
    return news