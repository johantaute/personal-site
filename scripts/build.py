"""Build only public assets and generate a CSP matching the inline scripts."""
from pathlib import Path
import base64
import hashlib
import re
import shutil

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "public"
OUTPUT = ROOT / "dist"

def script_hashes(html):
    html = html.replace("\r\n", "\n").replace("\r", "\n")
    hashes = []
    for match in re.finditer(r"<script\b([^>]*)>(.*?)</script\s*>", html, re.I | re.S):
        if re.search(r"\bsrc\s*=", match.group(1), re.I):
            raise ValueError("External scripts require an explicit policy review.")
        digest = hashlib.sha256(match.group(2).encode("utf-8")).digest()
        hashes.append("'sha256-" + base64.b64encode(digest).decode("ascii") + "'")
    return sorted(set(hashes))

def build():
    if not (SOURCE / "index.html").is_file():
        raise ValueError("public/index.html is required.")
    for path in SOURCE.rglob("*"):
        if path.is_symlink():
            raise ValueError("Public assets must not contain symlinks.")
        if path.name.startswith(".") and path.name != ".well-known":
            raise ValueError("Hidden files must not be published.")
        if path.suffix.lower() in {".pem", ".key", ".env"}:
            raise ValueError("Credentials must not be published.")
    if OUTPUT.is_symlink():
        raise ValueError("dist must not be a symlink.")
    if OUTPUT.exists():
        shutil.rmtree(OUTPUT)
    shutil.copytree(SOURCE, OUTPUT)
    hashes = sorted({h for file in SOURCE.rglob("*.html") for h in script_hashes(file.read_text(encoding="utf-8"))})
    scripts = " ".join(hashes)
    policy = "; ".join([
        "default-src 'self'",
        "script-src "+ (scripts if hashes else "'none'"),
        "script-src-attr 'none'",
        "style-src 'self'",
        "font-src 'self'",
        "img-src 'self'",
        "connect-src 'none'",
        "frame-src 'none'",
        "object-src 'none'",
        "base-uri 'self'",
        "frame-ancestors 'none'",
        "form-action 'none'",
        "upgrade-insecure-requests",
    ])
    headers = [
        "/*",
        "  X-Content-Type-Options: nosniff",
        "  X-Frame-Options: DENY",
        "  Referrer-Policy: strict-origin-when-cross-origin",
        "  Permissions-Policy: camera=(), microphone=(), geolocation=()",
        "  Strict-Transport-Security: max-age=31536000",
        "  Content-Security-Policy: " + policy,
    ]
    if any(len(line) > 2000 for line in headers):
        raise ValueError("Cloudflare header line limit exceeded.")
    (OUTPUT / "_headers").write_text("\n".join(headers) + "\n", encoding="utf-8")
    print(f"Built public assets with {len(hashes)} inline script hashes.")

if __name__ == "__main__":
    build()
