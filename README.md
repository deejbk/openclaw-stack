# OpenClaw Tool API

Exposes the knowledge base over two interfaces:
- **FastAPI** — REST endpoint at `http://localhost:8000/search`
- **MCP server** — streamable-http at `http://localhost:9000/mcp`, tool: `search_markdown`

Both use the same ripgrep search over `/home/dj/openclaw/knowledge`.

---

## Prerequisites

- Python venv at `/home/dj/openclaw/tool_api/.venv` (do not recreate)
- `ripgrep` (`rg`) installed and on PATH
- Knowledge directory exists at `/home/dj/openclaw/knowledge`

Validate the environment:

```bash
/home/dj/openclaw/tool_api/.venv/bin/python -c "import mcp; print('mcp ok')"
```

---

## Activate the venv

All commands below assume the venv is active. Activate once per session:

```bash
cd /home/dj/openclaw/tool_api
source .venv/bin/activate
```

---

## FastAPI server (port 8000)

```bash
uvicorn app:app --host 0.0.0.0 --port 8000
```

Test:

```bash
curl http://localhost:8000/health
curl "http://localhost:8000/search?q=test"
```

---

## MCP server (port 9000)

```bash
python tool_api/search_mcp.py
```

> Run from project root `/home/dj/openclaw` with the venv active.

Expected output:

```
INFO:     Started server process [...]
INFO:     Waiting for application startup.
StreamableHTTP session manager started
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:9000 (Press CTRL+C to quit)
```

---

## Test the MCP server

The MCP streamable-http protocol requires a session handshake before any request. Raw curl will always fail with "Missing session ID" — use the test script instead.

Run from project root with the venv active:

```bash
python tool_api/test_mcp.py Jeeves 5
```

Arguments: `query` (default: `test`), `limit` (default: `3`).

The script initializes a session, lists tools, then calls `search_markdown` with the given query.

---

## Port conflicts

If you get `[Errno 98] address already in use`:

```bash
sudo ss -tanp | grep ':9000'
sudo fuser -k 9000/tcp
```

Then restart the server.

---

## File reference

| File | Purpose |
|---|---|
| `tool_api/app.py` | FastAPI REST app — do not modify |
| `tool_api/search_mcp.py` | MCP server wrapping the same search logic |
| `tool_api/test_mcp.py` | Smoke test script for the MCP server |
| `tool_api/requirements.txt` | Pinned dependencies for the venv |
