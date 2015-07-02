# $Id: views.py 12295 2014-12-11 14:47:05Z jrms $

from django.shortcuts import render, redirect

from tsadm.slave import TSAdmSlave
from tsadm.wapp import TSAdmWApp
wapp = TSAdmWApp()


def dashboard(req, slave_slug):
    if not wapp.start(req, '__slave/dashboard', '__slave/dashboard'):
        return wapp.error_page()
    tmpl_data = wapp.tmpl_data()
    slave_id = wapp.db.slave_id(slave_slug)
    wapp.log.dbg('slave_slug=', slave_slug)
    wapp.log.dbg('slave_id=', slave_id)
    if slave_id is None:
        return wapp.error_page(404, 'slave server not found')
    slave = TSAdmSlave(wapp, slave_id)
    tmpl_data.update(slave.tmpl_data(softinfo=True))
    return render(req, 'slave/dashboard.html', wapp.end(tmpl_data))


def admin(req):
    if not wapp.start(req, '__slave/admin', acclvl='ADMIN'):
        return wapp.error_page()
    tmpl_data = wapp.tmpl_data()
    slaves_all = wapp.db.slave_all()
    for sinfo in slaves_all:
        slave = TSAdmSlave(wapp, sinfo.get('id', None))
        sinfo.update(slave.tmpl_data())
    tmpl_data['admin'] = {
        'slaves_all': slaves_all
    }
    wapp.log.dbg('slaves_all: ', tmpl_data['admin']['slaves_all'])
    return render(req, 'slave/admin.html', wapp.end(tmpl_data))
