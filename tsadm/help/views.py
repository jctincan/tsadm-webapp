# $Id: views.py 12116 2014-11-19 15:51:01Z jrms $

from django.shortcuts import render

from tsadm.wapp import TSAdmWApp
wapp = TSAdmWApp()


def site(req, sname, senv):
    if not wapp.start(req, sname, senv):
        return wapp.error_page()
    tmpl_data = wapp.tmpl_data()
    return render(req, 'help/site.html', wapp.end(tmpl_data))
