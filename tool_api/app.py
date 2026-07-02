from pathlib import Path
import subprocess

from fastapi import FastAPI, Query

app = FastAPI(title="OpenClaw Tool API")

KNOWLEDGE_DIR = Path.home() / "openclaw" / "knowledge"


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/search")
def search(q: str = Query(..., min_length=1)):
    if not KNOWLEDGE_DIR.exists():
        return {
            "query": q,
            "knowledge_dir": str(KNOWLEDGE_DIR),
            "error": "knowledge directory not found",
            "matches": [],
        }

    cmd = [
        "rg",
        "--ignore-case",
        "--line-number",
        "--with-filename",
        "--max-count",
        "20",
        q,
        str(KNOWLEDGE_DIR),
    ]

    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
    )

    if result.returncode not in (0, 1):
        return {
            "query": q,
            "knowledge_dir": str(KNOWLEDGE_DIR),
            "error": result.stderr.strip(),
            "matches": [],
        }

    matches = []
    for line in result.stdout.splitlines():
        parts = line.split(":", 2)
        if len(parts) == 3:
            filename, line_number, text = parts
            matches.append(
                {
                    "file": filename,
                    "line": int(line_number),
                    "text": text.strip(),
                }
            )

    return {
        "query": q,
        "knowledge_dir": str(KNOWLEDGE_DIR),
        "count": len(matches),
        "matches": matches,
    }
