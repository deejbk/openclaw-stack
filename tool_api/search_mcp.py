"""
MCP server wrapping knowledge base search for OpenClaw.

Exposes the search_markdown tool over streamable-http on 0.0.0.0:9000.
Delegates to the same ripgrep logic used by the FastAPI /search endpoint.
"""

from pathlib import Path
import subprocess

from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel

KNOWLEDGE_DIR = Path.home() / "openclaw" / "knowledge"

mcp = FastMCP("kb-search")


class Match(BaseModel):
    file: str
    line: int
    text: str


class SearchResult(BaseModel):
    query: str
    knowledge_dir: str
    count: int
    matches: list[Match]


@mcp.tool()
def search_markdown(query: str, limit: int = 8) -> SearchResult:
    """Search the OpenClaw markdown knowledge base using ripgrep.

    Args:
        query: Search term to find across all markdown files.
        limit: Maximum number of results to return (default: 8).

    Returns:
        Structured results with query metadata and matching lines.
        Each match includes file path, line number, and matched text.
    """
    if not KNOWLEDGE_DIR.exists():
        return SearchResult(
            query=query,
            knowledge_dir=str(KNOWLEDGE_DIR),
            count=0,
            matches=[],
        )

    cmd = [
        "rg",
        "--ignore-case",
        "--line-number",
        "--with-filename",
        "--max-count", "20",
        query,
        str(KNOWLEDGE_DIR),
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode not in (0, 1):
        raise RuntimeError(result.stderr.strip() or "ripgrep search failed")

    matches: list[Match] = []
    for line in result.stdout.splitlines():
        parts = line.split(":", 2)
        if len(parts) == 3:
            filename, line_number, text = parts
            matches.append(Match(file=filename, line=int(line_number), text=text.strip()))

    matches = matches[:limit]

    return SearchResult(
        query=query,
        knowledge_dir=str(KNOWLEDGE_DIR),
        count=len(matches),
        matches=matches,
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(mcp.streamable_http_app(), host="0.0.0.0", port=9000)
