
from django.shortcuts import render

from tsadm.wapp import TSAdmWApp
wapp = TSAdmWApp()


def home(req, sname, senv):
    if not wapp.start(req, sname, senv):
        return wapp.error_page()
    tmpl_data = wapp.tmpl_data()
    return render(req, 'mysql/home.html', wapp.end(tmpl_data))
