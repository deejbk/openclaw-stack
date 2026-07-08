#!/usr/bin/env python3
"""Smoke test for the MCP server — initialize, list tools, call search_markdown."""
import httpx
import json

BASE = "http://localhost:9000/mcp"
HEADERS = {
    "Content-Type": "application/json",
    "Accept": "application/json, text/event-stream",
}


def mcp_post(payload, session_id=None):
    headers = {**HEADERS}
    if session_id:
        headers["Mcp-Session-Id"] = session_id
    r = httpx.post(BASE, headers=headers, json=payload, timeout=10)
    sid = r.headers.get("mcp-session-id")
    # responses come as SSE — extract the data line
    body = None
    for line in r.text.splitlines():
        if line.startswith("data: "):
            body = json.loads(line[6:])
            break
    if body is None and r.text.strip():
        body = json.loads(r.text)
    return sid, body


def main():
    # 1. Initialize
    sid, resp = mcp_post({
        "jsonrpc": "2.0", "id": 1, "method": "initialize",
        "params": {
            "protocolVersion": "2024-11-05",
            "capabilities": {},
            "clientInfo": {"name": "test-client", "version": "1.0"},
        },
    })
    print(f"session_id : {sid}")
    print(f"initialize : {json.dumps(resp, indent=2)}\n")

    # 2. tools/list
    _, resp = mcp_post({"jsonrpc": "2.0", "id": 2, "method": "tools/list", "params": {}}, sid)
    print(f"tools/list : {json.dumps(resp, indent=2)}\n")

    # 3. tools/call — search_markdown
    _, resp = mcp_post({
        "jsonrpc": "2.0", "id": 3, "method": "tools/call",
        "params": {"name": "search_markdown", "arguments": {"query": "test", "limit": 3}},
    }, sid)
    print(f"tools/call : {json.dumps(resp, indent=2)}")


if __name__ == "__main__":
    main()
