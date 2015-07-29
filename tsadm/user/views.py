
import time
from django.shortcuts import render

from tsadm.wapp import TSAdmWApp
wapp = TSAdmWApp()


def home(req):
    if not wapp.start(req, '__user/home'):
        return wapp.error_page()
    tmpl_data = wapp.tmpl_data()
    return render(req, 'user/home.html', wapp.end(tmpl_data))


def admin(req):
    if not wapp.start(req, '__user/admin', acclvl='ADMIN'):
        return wapp.error_page()
    tmpl_data = wapp.tmpl_data()
    users_all = list()
    for u in wapp.db.user_all():
        u['last_seen'] = time.strftime(wapp.conf.get('CUR_TIME_FMT'), time.localtime(u['last_seen']))
        users_all.append(u)
    tmpl_data['users_all'] = users_all
    return render(req, 'user/admin.html', wapp.end(tmpl_data))
