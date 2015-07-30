
import time

from django.shortcuts import render
from django.http import HttpResponse

from tsadm.wapp import TSAdmWApp
wapp = TSAdmWApp()


def home(req):
    if not wapp.start(req, '__admin/home', acclvl='ADMIN_LOW'):
        return wapp.error_page()
    tmpl_data = wapp.tmpl_data()
    adm_log = list()
    for le in wapp.db.adm_log():
        d = {
            'date': time.strftime(wapp.conf.get('LOG_DATE_FMT'), time.localtime(le['tstamp_start'])),
            'cmd_took': '.',
            'id_slug': '{}...{}'.format(le['id'][:7], le['id'][-7:]),
        }
        if le['status'] == 'END':
            d['cmd_took'] = '{}s'.format(le['tstamp_end'] - le['tstamp_start'])
        if le['cmd_exit'] == 0:
            d['css_class'] = 'ok'
        elif le['cmd_exit'] == 9999:
            d['css_class'] = 'start'
        elif le['cmd_exit'] == 9090:
            d['css_class'] = 'run'
        else:
            d['css_class'] = 'error'
        le.update(d)
        adm_log.append(le)
    tmpl_data['adm'] = {
        'log': adm_log,
    }
    return render(req, 'admin/home.html', wapp.end(tmpl_data))


def activity(req, log_limit=50):
    if not wapp.start(req, '__admin/activity', acclvl='ADMIN_LOW'):
        return wapp.error_page()
    tmpl_data = wapp.tmpl_data()
    actlog = list()
    for le in wapp.db.activity_log_get(log_limit):
        le['date'] = time.strftime(wapp.conf.get('LOG_DATE_FMT'), time.localtime(le['tstamp']))
        actlog.append(le)
    tmpl_data['actlog'] = actlog
    return render(req, 'admin/activity.html', wapp.end(tmpl_data))


def dbmaint(req):
    if not wapp.start(req, '__admin/dbmaint', acclvl='ADMIN'):
        return wapp.error_page()
    resp = HttpResponse(content_type='text/plain; charset=utf-8', status=200)
    resp.write('dbmaint\n')
    wapp.db.jobq_maint()
    resp.write('  jobq\n')
    wapp.db.activity_log_maint()
    resp.write('  activity log\n')
    resp.write('done\n')
    wapp.end(wapp.tmpl_data())
    return resp
