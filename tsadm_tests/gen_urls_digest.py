# $Id: gen_urls_digest.py 12186 2014-11-30 18:38:36Z jrms $

import http.client
import sys

from . import get_url, parse_content, get_digest

if __name__ == '__main__':
    conn = http.client.HTTPConnection('127.0.0.1', 8000)
    for url in sys.stdin.readlines():
        url = url.strip()
        print(url, get_digest(parse_content(get_url(conn, url))))
    conn.close()
    sys.exit(0)
