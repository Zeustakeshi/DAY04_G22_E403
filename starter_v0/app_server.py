from __future__ import annotations

import json
import os
import sys
from http.server import HTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
from typing import Any
import urllib.parse

from env_loader import load_lab_env
from providers import make_provider
from tools import TOOL_FUNCTIONS, load_tool_declarations, to_openai_tools
from versioning import artifact_version_dict, build_artifact_version
from chat import run_model_tool_loop, trim_history

ROOT = Path(__file__).parent
ARTIFACTS_DIR = ROOT / "artifacts"
STATIC_DIR = ROOT / "static"

load_lab_env(ROOT)

class AgentRequestHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(STATIC_DIR), **kwargs)

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        if parsed.path == "/api/tools":
            self.send_json_response(self.get_tools_info())
        elif parsed.path == "/api/versions":
            self.send_json_response(self.get_versions_info())
        else:
            if parsed.path == "/" or parsed.path == "":
                self.path = "/index.html"
            super().do_GET()

    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)
        if parsed.path == "/api/chat":
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length)
            try:
                data = json.loads(body.decode("utf-8"))
                response_data = self.handle_chat(data)
                self.send_json_response(response_data)
            except Exception as exc:
                self.send_json_response({"error": str(exc)}, status=500)
        else:
            self.send_error(404, "Not Found")

    def send_json_response(self, data: Any, status: int = 200):
        body = json.dumps(data, ensure_ascii=False, indent=2).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def get_tools_info(self) -> dict[str, Any]:
        tools_path = ARTIFACTS_DIR / "tools.yaml"
        declarations = load_tool_declarations(tools_path)
        return {"tools": declarations}

    def get_versions_info(self) -> dict[str, Any]:
        version_log_path = ARTIFACTS_DIR / "version_log.csv"
        versions = []
        if version_log_path.exists():
            lines = version_log_path.read_text(encoding="utf-8").splitlines()
            if len(lines) > 1:
                header = lines[0].split(",")
                for line in lines[1:]:
                    if line.strip():
                        parts = line.split(",")
                        if len(parts) >= len(header):
                            item = dict(zip(header, parts))
                            versions.append(item)
        return {"versions": versions}

    def handle_chat(self, data: dict[str, Any]) -> dict[str, Any]:
        user_message = data.get("message", "").strip()
        history = data.get("history", [])
        version_label = data.get("version", "v3")
        provider_name = data.get("provider", "openrouter")
        history_window = data.get("history_window", 5)
        max_tool_rounds = data.get("max_tool_rounds", 4)

        system_prompt_path = ARTIFACTS_DIR / "system_prompt.md"
        tools_path = ARTIFACTS_DIR / "tools.yaml"

        system_prompt = system_prompt_path.read_text(encoding="utf-8")
        tool_declarations = load_tool_declarations(tools_path)
        openai_tools = to_openai_tools(tool_declarations)

        provider = make_provider(provider_name)
        selected_model = getattr(provider, "default_model", None)
        artifact_ver = build_artifact_version(version_label, system_prompt_path, tools_path)

        messages = [
            {"role": "system", "content": system_prompt},
            *trim_history(history, history_window),
            {"role": "user", "content": user_message},
        ]

        result = run_model_tool_loop(
            provider=provider,
            messages=messages,
            tools=openai_tools,
            model=selected_model,
            max_tool_rounds=max_tool_rounds,
        )

        result["artifact_version"] = artifact_version_dict(artifact_ver)
        result["model"] = selected_model
        return result

def run_server(port: int = 8000):
    STATIC_DIR.mkdir(parents=True, exist_ok=True)
    server_address = ("", port)
    httpd = HTTPServer(server_address, AgentRequestHandler)
    print(f"🚀 Research Agent Server running at http://localhost:{port}")
    httpd.serve_forever()

if __name__ == "__main__":
    port = 8000
    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
        except ValueError:
            pass
    run_server(port)
