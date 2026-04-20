#!/usr/bin/env python3
"""serve-analysis.py — Local server for the H2A analysis dashboard.

Usage:
    python serve-analysis.py <instance-path> [<instance-path> ...] [--port 8042]

Serves analysis.html and provides a /run endpoint to re-execute analysis.py.
Zero external dependency — Python 3.10+ stdlib only.
"""
from __future__ import annotations

import json
import mimetypes
import subprocess
import sys
from http.server import HTTPServer, BaseHTTPRequestHandler
from pathlib import Path
from urllib.parse import urlparse

PORT = 8042
HERE = Path(__file__).resolve().parent
ANALYSIS_PY = HERE / "analysis.py"
AUDIT_PY = HERE / "audit-instance.py"
ANALYSIS_JSON = HERE / "analysis.json"

INSTANCE_PATHS: list[str] = []


class Handler(BaseHTTPRequestHandler):

    def do_GET(self):
        path = urlparse(self.path).path
        if path == "/":
            path = "/analysis.html"

        # Serve from filesystem/ or from sofia root (for doc/)
        filepath = HERE / path.lstrip("/")
        if not filepath.is_file():
            filepath = HERE.parent.parent / path.lstrip("/")
        if not filepath.is_file():
            self.send_error(404)
            return

        mime = mimetypes.guess_type(str(filepath))[0] or "application/octet-stream"
        data = filepath.read_bytes()
        self.send_response(200)
        self.send_header("Content-Type", mime)
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_POST(self):
        path = urlparse(self.path).path
        if path == "/run":
            self._run_analysis()
        elif path == "/audit":
            self._run_audit()
        else:
            self.send_error(404)

    def _run_analysis(self):
        try:
            cmd = [sys.executable, str(ANALYSIS_PY)]
            cmd += INSTANCE_PATHS
            cmd += ["--output", str(ANALYSIS_JSON)]
            result = subprocess.run(
                cmd, capture_output=True, text=True, timeout=60
            )
            if result.returncode != 0:
                self._json_response(500, {"error": result.stderr.strip()})
                return

            data = ANALYSIS_JSON.read_text(encoding="utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(data.encode())))
            self.end_headers()
            self.wfile.write(data.encode())

        except subprocess.TimeoutExpired:
            self._json_response(504, {"error": "timeout (60s)"})
        except Exception as e:
            self._json_response(500, {"error": str(e)})

    def _run_audit(self):
        try:
            results = {}
            for inst_path in INSTANCE_PATHS:
                name = Path(inst_path).name
                cmd = [sys.executable, str(AUDIT_PY), inst_path, "--format", "json"]
                result = subprocess.run(
                    cmd, capture_output=True, text=True, timeout=120
                )
                if result.returncode != 0:
                    results[name] = {"error": result.stderr.strip()}
                    continue

                # Read the 5 JSON files produced by audit
                audits_dir = Path(inst_path) / "shared" / "audits"
                inst_data = {}
                for audit_file in audits_dir.glob("audit-*.json"):
                    key = audit_file.stem.removeprefix("audit-")
                    inst_data[key] = json.loads(audit_file.read_text(encoding="utf-8"))
                results[name] = inst_data

            body = json.dumps(results, ensure_ascii=False, indent=2).encode()
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        except subprocess.TimeoutExpired:
            self._json_response(504, {"error": "timeout (120s)"})
        except Exception as e:
            self._json_response(500, {"error": str(e)})

    def _json_response(self, code, obj):
        body = json.dumps(obj).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format, *args):
        msg = str(args)
        if "/run" in msg or "POST" in msg or self.command == "POST":
            super().log_message(format, *args)


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Serve H2A analysis dashboard")
    parser.add_argument("instances", nargs="+", help="Path(s) to SOFIA instance root(s)")
    parser.add_argument("--port", type=int, default=PORT, help=f"Port (default: {PORT})")
    args = parser.parse_args()

    global INSTANCE_PATHS
    INSTANCE_PATHS = []
    for p in args.instances:
        resolved = Path(p).resolve()
        marker = resolved / "sofia.md"
        if not marker.is_file():
            # Fallback: try voix.md (legacy)
            marker = resolved / "voix.md"
        if not marker.is_file():
            print(f"  ⚠ Instance ignoree (pas de sofia.md) : {resolved}", file=sys.stderr)
            continue
        INSTANCE_PATHS.append(str(resolved))

    if not INSTANCE_PATHS:
        print("✗ Aucune instance valide trouvee.", file=sys.stderr)
        sys.exit(1)

    server = HTTPServer(("127.0.0.1", args.port), Handler)
    names = ", ".join(Path(p).name for p in INSTANCE_PATHS)
    print(f"✓ H2A Analysis Dashboard")
    print(f"  http://localhost:{args.port}")
    print(f"  Instances: {names}")
    print(f"  Bouton 'Analyser' dans le dashboard pour relancer")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n✓ Arret.")
        server.server_close()


if __name__ == "__main__":
    main()
