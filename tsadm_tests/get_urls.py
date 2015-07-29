
import http.client
import re
import sys


re_href = re.compile(r'.*href="([^"]+)"[^"].*$')
re_jobq_info = re.compile(r'^/jobq/([\w]+)/([\w]+)/info/([a-f0-9]+)/$')
#~ re_claim_confirm = re.compile(r'^/site/[\w]+/[\w]+/claim/[a-f0-9]+/$')
#~ re_lock_confirm = re.compile(r'^/site/[\w]+/[\w]+/lock/[a-f0-9]+/$')


class S:
    parsed_urls = 0
    found_urls = 0
    ignored_urls = 0

class G:
    conn = None
    full_list = None
    parsed_urls = None
    ignored_urls = None
    disable_ignore_urls = None


def __do_ignore(url):
    S.ignored_urls += 1
    G.ignored_urls.append(url)
    return True


def __ignore_url(url):
    if G.disable_ignore_urls:
        return False
    if url.startswith('/jobq/'):
        if url.startswith('/jobq/icc/'):
            return __do_ignore(url)
        elif re_jobq_info.match(url):
            return __do_ignore(url)
    elif url.startswith('/site/'):
        if url.endswith('/log/'):
            return __do_ignore(url)
        elif url.endswith('/claim/'):
            return __do_ignore(url)
        elif url.endswith('/lock/'):
            return __do_ignore(url)
    return False


def __get_content(url):
    G.conn.request('GET', url)
    resp = G.conn.getresponse()
    content = resp.read().decode()
    content_lines = content.split('\n')
    del content
    return content_lines


def __parse_content(content_lines):
    urls = list()
    for line in content_lines:
        line = line.strip()
        match = re_href.match(line)
        if match:
            href = match.group(1)
            if href.endswith('/') and href != '/' and not href.startswith('http'):
                if not __ignore_url(href):
                    __parse_url(href)
                    urls.append(href)
    return urls


def __parse_url(url):
    if not __ignore_url(url):
        if not url in G.parsed_urls:
            S.parsed_urls += 1
            G.parsed_urls.append(url)
            content_lines = __get_content(url)
            new_list = __parse_content(content_lines)
            for new_url in new_list:
                if not new_url in G.full_list:
                    G.full_list.append(new_url)
                    S.found_urls += 1


if __name__ == '__main__':
    G.disable_ignore_urls = False
    if '--disable-ignore' in sys.argv:
        G.disable_ignore_urls = True
    G.conn = http.client.HTTPConnection('127.0.0.1', 8000)
    G.full_list = ['/']
    G.parsed_urls = list()
    G.ignored_urls = list()
    __parse_url('/')
    G.conn.close()
    for url in sorted(G.full_list):
        print(url)
    if '--print-ignored' in sys.argv:
        for url in G.ignored_urls:
            print('IGNORED:', url, file=sys.stderr)
    print('Ignored URLs:', S.ignored_urls, file=sys.stderr)
    print('Parsed URLs:', S.parsed_urls, file=sys.stderr)
    print('Found URLs:', S.found_urls, file=sys.stderr)
    sys.exit(0)
