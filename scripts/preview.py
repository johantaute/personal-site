"""Serve the built website on loopback only, with its security headers."""
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
from functools import partial
import argparse
from urllib.parse import urlsplit, parse_qs
ROOT = Path(__file__).resolve().parents[1]
class Preview(SimpleHTTPRequestHandler):
    def do_GET(self):
        if urlsplit(self.path).path == "/__review":
            body = b'<html lang="en"><head><title>Mobile review</title><meta name="viewport" content="width=device-width,initial-scale=1"><style>body{background:#d9e0da;font:16px system-ui;padding:24px}iframe{width:390px;height:740px;border:0;background:white}a{color:#152b36}nav{margin-bottom:20px}</style></head><body><nav>390px mobile preview | <a href="/">Desktop site</a></nav><iframe title="Mobile website preview" src="/"></iframe></body></html>'
            page = parse_qs(urlsplit(self.path).query).get('page', ['/'])[0]
            if page not in {'/', '/services/', '/approach/', '/about/', '/contact/', '/sample-report/'}: page = '/'
            body = body.replace(b'src="/"', ('src="' + page + '"').encode())
            self.send_response(200);self.send_header("Content-Type", "text/html; charset=utf-8");self.send_header("Content-Length", str(len(body)));self.end_headers();self.wfile.write(body)
        else:
            super().do_GET()
    def end_headers(self):
        for line in (ROOT / 'dist' / '_headers').read_text().splitlines()[1:]:
            key, value = line.strip().split(':', 1)
            if key in ('Strict-Transport-Security','X-Frame-Options'):
                continue
            if key == 'Content-Security-Policy':
                value = value.replace('; upgrade-insecure-requests', '').replace("frame-src 'none'", "frame-src 'self'").replace("frame-ancestors 'none'", "frame-ancestors 'self'")
                if urlsplit(self.path).path == '/__review':
                    value = value.replace("style-src 'self'", "style-src 'self' 'unsafe-inline'")
            self.send_header(key, value.strip())
        self.send_header('X-Robots-Tag', 'noindex, nofollow')
        super().end_headers()
if __name__ == '__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--port',type=int,default=4173);args=parser.parse_args()
    print(f'Preview: http://127.0.0.1:{args.port}', flush=True)
    ThreadingHTTPServer(('127.0.0.1', args.port), partial(Preview, directory=str(ROOT / 'dist'))).serve_forever()
