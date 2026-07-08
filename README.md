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

Run these from a second terminal (no venv required). All commands are single-line.

**Check the server is up:**

```bash
curl -s http://localhost:9000/mcp
```

**List available tools:**

```bash
curl -s -X POST http://localhost:9000/mcp -H "Content-Type: application/json" -H "Accept: application/json, text/event-stream" -d '{"jsonrpc":"2.0","id":1,"method":"tools/list","params":{}}'
```

**Call `search_markdown`:**

```bash
curl -s -X POST http://localhost:9000/mcp -H "Content-Type: application/json" -H "Accept: application/json, text/event-stream" -d '{"jsonrpc":"2.0","id":2,"method":"tools/call","params":{"name":"search_markdown","arguments":{"query":"test","limit":3}}}'
```

Responses are returned as SSE (`text/event-stream`) — lines prefixed with `data:`. This is expected.

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
| `tool_api/requirements.txt` | Pinned dependencies for the venv |
