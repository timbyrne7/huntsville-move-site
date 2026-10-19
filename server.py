#!/usr/bin/env python3
"""Rocket City Move — local preview server (standard library only).

Serves the static prototype and captures form submissions so the lead funnel is
visible end to end:
    GET  /                 static site
    POST /api/lead         every form on the site (appended to leads.jsonl/.csv)
    POST /api/alert        price alerts (appended to alerts.jsonl)
    GET  /_leads           human-readable view of captured submissions
    GET  /health           {"ok": true, ...}

Run:  python3 server.py [--port 8080] [--host 0.0.0.0]
"""

import argparse
import csv
import html
import json
import os
import sys
from datetime import datetime, timezone
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse, parse_qs

ROOT = os.path.dirname(os.path.abspath(__file__))
# Captured leads must survive a redeploy, so allow them to live outside the app folder
# (e.g. LEADS_DIR=/data on a mounted Railway volume). Defaults to the project folder.
LEADS_DIR = os.environ.get("LEADS_DIR") or ROOT
if LEADS_DIR != ROOT:
    os.makedirs(LEADS_DIR, exist_ok=True)
LEADS = os.path.join(LEADS_DIR, "leads.jsonl")
LEADS_CSV = os.path.join(LEADS_DIR, "leads.csv")
ALERTS = os.path.join(LEADS_DIR, "alerts.jsonl")

MIME = {
    ".html": "text/html; charset=utf-8", ".css": "text/css; charset=utf-8",
    ".js": "application/javascript; charset=utf-8", ".json": "application/json; charset=utf-8",
    ".svg": "image/svg+xml", ".png": "image/png", ".jpg": "image/jpeg",
    ".ico": "image/x-icon", ".txt": "text/plain; charset=utf-8", ".csv": "text/csv; charset=utf-8",
}

FIELDS = ["ts", "form", "page", "name", "email", "phone", "address", "zip", "timeline",
          "price_range", "loan_type", "credit_band", "employer", "military", "work_location",
          "area", "max_price", "min_beds", "district", "budget", "from_city", "consent"]


def append_jsonl(path, record):
    with open(path, "a", encoding="utf-8") as fh:
        fh.write(json.dumps(record, ensure_ascii=False) + "\n")


def append_csv(record):
    new = not os.path.exists(LEADS_CSV)
    with open(LEADS_CSV, "a", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=FIELDS, extrasaction="ignore")
        if new:
            w.writeheader()
        w.writerow({k: ("" if record.get(k) is None else record.get(k)) for k in FIELDS})


class Handler(SimpleHTTPRequestHandler):
    server_version = "RocketCityMovePreview/0.1"

    def __init__(self, *a, **kw):
        super().__init__(*a, directory=ROOT, **kw)

    # ---------- helpers ----------
    def _json(self, payload, code=200):
        body = json.dumps(payload).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def _read_json(self):
        try:
            n = int(self.headers.get("Content-Length") or 0)
            raw = self.rfile.read(n) if n else b"{}"
            return json.loads(raw.decode("utf-8") or "{}")
        except Exception:
            return {}

    def end_headers(self):
        self.send_header("X-Content-Type-Options", "nosniff")
        # Prototype previews are edited constantly: never let the browser serve a stale
        # copy of a page, stylesheet or script.
        ext = os.path.splitext(urlparse(self.path).path)[1].lower()
        if ext in ("", ".html", ".js", ".css", ".json") or self.path in ("/", "/_leads"):
            self.send_header("Cache-Control", "no-store, must-revalidate")
        super().end_headers()

    def guess_type(self, path):
        ext = os.path.splitext(path)[1].lower()
        return MIME.get(ext, super().guess_type(path))

    # ---------- routes ----------
    def _leads_allowed(self):
        """Local preview only: loopback Host header, or ?token=<LEADS_TOKEN> if set."""
        tok = os.environ.get("LEADS_TOKEN", "")
        if tok and parse_qs(urlparse(self.path).query).get("token", [""])[0] == tok:
            return True
        host = (self.headers.get("Host") or "").split(":")[0].strip("[]").lower()
        return host in ("localhost", "127.0.0.1", "::1", "0.0.0.0")

    def do_GET(self):
        path = urlparse(self.path).path
        if path == "/health":
            return self._json({"ok": True, "time": datetime.now(timezone.utc).isoformat(),
                               "leads": sum(1 for _ in open(LEADS, encoding="utf-8")) if os.path.exists(LEADS) else 0})
        if path in ("/_leads", "/_leads/"):
            if not self._leads_allowed():
                return self._json({"error": "not found"}, 404)
            return self._leads_page()
        # Never serve captured submissions as static files. The tunnel proxies from
        # 127.0.0.1, so a loopback check is not enough - gate on the Host header.
        if path.lower().startswith("/leads."):
            return self._json({"error": "not served"}, 403)
        if path == "/":
            self.path = "/index.html"
        return super().do_GET()

    def do_POST(self):
        path = urlparse(self.path).path
        payload = self._read_json()
        if path not in ("/api/lead", "/api/alert"):
            return self._json({"ok": False, "error": "unknown endpoint"}, 404)
        payload.setdefault("ts", datetime.now(timezone.utc).isoformat())
        payload["ip"] = self.client_address[0]
        if path == "/api/lead":
            append_jsonl(LEADS, payload)
            append_csv(payload)
            print(f"[lead] {payload.get('form')} :: {payload.get('email')} :: {payload.get('page')}", flush=True)
            return self._json({"ok": True, "id": payload["ts"]})
        append_jsonl(ALERTS, payload)
        print(f"[alert] {payload.get('email')} :: {payload.get('area')}", flush=True)
        return self._json({"ok": True, "id": payload["ts"]})

    def _leads_page(self):
        rows = []
        if os.path.exists(LEADS):
            with open(LEADS, encoding="utf-8") as fh:
                rows = [json.loads(l) for l in fh if l.strip()]
        rows.reverse()
        keys = ["ts", "form", "email", "name", "phone", "price_range", "timeline", "area",
                "work_location", "district", "page", "ip"]
        body = ["<!DOCTYPE html><html><head><meta charset='utf-8'><title>Captured leads</title>",
                "<style>body{font:14px/1.5 system-ui,sans-serif;margin:28px;color:#0f1720}",
                "table{border-collapse:collapse;width:100%}th,td{border-bottom:1px solid #e2e8f0;padding:7px 9px;text-align:left;vertical-align:top}",
                "th{font-size:12px;text-transform:uppercase;color:#64748b}code{background:#f1f5f9;padding:2px 5px;border-radius:4px}",
                ".h{background:#f8fafc;padding:14px 18px;border-radius:12px;margin-bottom:18px}</style></head><body>",
                f"<div class='h'><h2 style='margin:0 0 6px'>Captured submissions — {len(rows)} total</h2>",
                f"<p style='margin:0'>Stored in <code>leads.jsonl</code> and <code>leads.csv</code> in the project folder. "
                f"Price alerts go to <code>alerts.jsonl</code>. This view is a prototype convenience — in production these go to your CRM.</p></div>",
                "<table><thead><tr>" + "".join(f"<th>{k}</th>" for k in keys) + "</tr></thead><tbody>"]
        for r in rows:
            body.append("<tr>" + "".join(f"<td>{html.escape(str(r.get(k, '')))}</td>" for k in keys) + "</tr>")
        body.append("</tbody></table></body></html>")
        out = "\n".join(body).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(out)))
        self.end_headers()
        self.wfile.write(out)

    def log_message(self, fmt, *args):
        if "/assets/" in self.path or self.path in ("/favicon.ico",):
            return
        sys.stderr.write("%s - %s\n" % (self.address_string(), fmt % args))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--port", type=int, default=int(os.environ.get("PORT", 8080)))
    ap.add_argument("--host", default=os.environ.get("HOST", "0.0.0.0"))
    args = ap.parse_args()
    httpd = ThreadingHTTPServer((args.host, args.port), Handler)
    print(f"Rocket City Move prototype serving {ROOT}")
    print(f"  local:    http://127.0.0.1:{args.port}/")
    print(f"  leads:    http://127.0.0.1:{args.port}/_leads")
    print("  Ctrl-C to stop")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nstopped")


if __name__ == "__main__":
    main()
