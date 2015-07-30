
import hashlib


def get_url(conn, url):
    conn.request('GET', url)
    resp = conn.getresponse()
    #~ print(resp.status, resp.reason)
    content = '{} {}\n{}'.format(resp.status, resp.reason, resp.read().decode())
    return content.split('\n')


def parse_content(content_lines):
    content = ''
    for line in content_lines:
        line = line.strip()
        #~ print('LINE:', line)
        if line.endswith('GMT<br />'):
            line = 'TSADM_TEST_REPLACE:date_time'
        elif line.startswith('vDEV : ') and line.endswith('s<br />'):
            line = 'TSADM_TEST_REPLACE:wapp_took'
        elif line.endswith('target="blank">view site</a> for this environment</pre>'):
            line = 'TSADM_TEST_REPLACE:site_view_link'
        content += line
    return content


def get_digest(content):
    sha1 = hashlib.sha1()
    sha1.update(content.encode())
    return sha1.hexdigest()
