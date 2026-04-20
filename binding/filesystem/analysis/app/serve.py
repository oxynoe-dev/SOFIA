"""serve.py — Static file server for the H2A dashboard.

Serves JSON from analysis/data/ and the dashboard HTML.
POST /refresh triggers analysis.py to regenerate all data.

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

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
APP_DIR = Path(__file__).resolve().parent
ANALYSIS_PY = Path(__file__).resolve().parent.parent.parent / "analysis.py"
DASHBOARD = Path(__file__).resolve().parent.parent.parent / "analysis.html"

INSTANCE_PATHS: list[str] = []
PORT = 8042


# Mapping endpoint → file
ENDPOINT_FILES = {
    "/mirror": "mirror.json",
    "/lens": "lens.json",
    "/probe": "probe.json",
}


class Handler(BaseHTTPRequestHandler):

    def do_GET(self):
        path = urlparse(self.path).path

        # Serve dashboard
        if path == "/":
            filepath = DASHBOARD
            if filepath.is_file():
                self._serve_file(filepath)
                return
            self.send_error(404, "dashboard.html not found")
            return

        # Serve JSON endpoints
        if path in ENDPOINT_FILES:
            filepath = DATA_DIR / ENDPOINT_FILES[path]
            if filepath.is_file():
                self._serve_file(filepath)
                return
            self._json_response(404, {"error": f"{ENDPOINT_FILES[path]} not found — run POST /refresh"})
            return

        # Serve legend
        if path == "/legend":
            legend = Path(__file__).resolve().parent.parent / "legend" / "legend.html"
            if not legend.is_file():
                legend = Path(__file__).resolve().parent.parent.parent / "legend.html"
            if legend.is_file():
                self._serve_file(legend)
                return
            self.send_error(404)
            return

        # Serve static files (CSS, JS, etc.) from app/ or legacy root
        for base in [APP_DIR, APP_DIR.parent.parent]:
            filepath = base / path.lstrip("/")
            if filepath.is_file():
                self._serve_file(filepath)
                return

        self.send_error(404)

    def do_POST(self):
        path = urlparse(self.path).path

        if path in ("/refresh", "/run", "/audit"):
            self._run_refresh()
        else:
            self.send_error(404)

    def _run_refresh(self):
        """Run analysis.py to regenerate all JSON."""
        try:
            cmd = [sys.executable, str(ANALYSIS_PY)] + INSTANCE_PATHS
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
            if result.returncode != 0:
                self._json_response(500, {"error": result.stderr.strip()})
                return

            # Return the refreshed probe data (most useful for dashboard)
            probe_path = DATA_DIR / "probe.json"
            if probe_path.is_file():
                data = probe_path.read_text(encoding="utf-8")
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.send_header("Content-Length", str(len(data.encode())))
                self.end_headers()
                self.wfile.write(data.encode())
            else:
                self._json_response(200, {"status": "ok", "output": result.stdout.strip()})

        except subprocess.TimeoutExpired:
            self._json_response(504, {"error": "timeout (120s)"})
        except Exception as e:
            self._json_response(500, {"error": str(e)})


    def _serve_file(self, filepath: Path):
        mime = mimetypes.guess_type(str(filepath))[0] or "application/octet-stream"
        data = filepath.read_bytes()
        self.send_response(200)
        self.send_header("Content-Type", mime)
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def _json_response(self, code, obj):
        body = json.dumps(obj).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format, *args):
        msg = str(args)
        if "POST" in msg or "/refresh" in msg:
            super().log_message(format, *args)


def run_server(instance_paths: list[Path], port: int = PORT):
    """Start the HTTP server."""
    global INSTANCE_PATHS
    INSTANCE_PATHS = [str(p) for p in instance_paths]

    server = HTTPServer(("127.0.0.1", port), Handler)
    names = ", ".join(p.name for p in instance_paths)
    print(f"✓ H2A Dashboard")
    print(f"  http://localhost:{port}")
    print(f"  Instances: {names}")
    print(f"  GET /mirror /lens /probe /legend")
    print(f"  POST /refresh → regenerates all data")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n✓ Stopped.")
        server.server_close()


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Serve H2A dashboard")
    parser.add_argument("instances", nargs="+", help="Instance paths")
    parser.add_argument("--port", type=int, default=PORT)
    args = parser.parse_args()

    paths = [Path(p).resolve() for p in args.instances]
    run_server(paths, args.port)
