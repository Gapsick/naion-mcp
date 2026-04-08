# naion-mcp

MCP server providing web_search and web_crawl tools via SSE transport.

## Tools

- **web_search** — Search the web using Tavily API
- **web_crawl** — Fetch and extract text content from a URL

## Setup

```bash
pip install -r requirements.txt
```

Create `.env`:
```
TAVILY_API_KEY=your_api_key
```

## Run

```bash
python server.py
```

Server runs on `http://127.0.0.1:8001/sse`

## Usage

Connect from any MCP client:

```python
from mcp.client.sse import sse_client
from mcp import ClientSession

async with sse_client("http://127.0.0.1:8001/sse") as (read, write):
    async with ClientSession(read, write) as session:
        await session.initialize()
        result = await session.call_tool("web_search", {"query": "search query"})
```
