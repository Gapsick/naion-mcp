import os
from dotenv import load_dotenv
from fastmcp import FastMCP
from tavily import AsyncTavilyClient
import httpx
from bs4 import BeautifulSoup

load_dotenv()

mcp = FastMCP("naion-search-tools")
tavily = AsyncTavilyClient(api_key=os.getenv("TAVILY_API_KEY"))


@mcp.tool()
async def web_search(query: str) -> str:
    """웹에서 정보를 검색합니다. 모르는 고유명사, 회사, 사람, 장소 등을 검색할 때 사용하세요.

    Args:
        query: 검색어 (한국어 또는 영어)
    """
    result = await tavily.search(query, include_answer=True, max_results=3)
    answer = result.get("answer", "")
    results = [
        {"title": r["title"], "content": r["content"]}
        for r in result.get("results", [])
    ]
    return f"요약: {answer}\n\n상세:\n" + "\n".join(
        f"- {r['title']}: {r['content'][:300]}" for r in results
    )


@mcp.tool()
async def web_crawl(url: str) -> str:
    """특정 URL의 페이지 내용을 가져옵니다. 회사 홈페이지, 채용 페이지 등을 읽을 때 사용하세요.

    Args:
        url: 크롤링할 페이지 URL
    """
    async with httpx.AsyncClient(timeout=10, follow_redirects=True) as client:
        headers = {"User-Agent": "Mozilla/5.0 (compatible; naion-bot/1.0)"}
        response = await client.get(url, headers=headers)
        response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    # 불필요한 태그 제거
    for tag in soup(["script", "style", "nav", "footer", "header"]):
        tag.decompose()

    text = soup.get_text(separator="\n", strip=True)

    # 빈 줄 정리 후 앞 3000자만
    lines = [l for l in text.splitlines() if l.strip()]
    return "\n".join(lines)[:3000]


if __name__ == "__main__":
    import uvicorn
    app = mcp.http_app(transport="sse")
    uvicorn.run(app, host="127.0.0.1", port=8001)
