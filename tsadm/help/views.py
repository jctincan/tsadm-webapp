from django.shortcuts import render
from django.template import loader, TemplateDoesNotExist

from tsadm.wapp import TSAdmWApp
wapp = TSAdmWApp()

def __find_template(name):
    try:
        loader.get_template(name)
    except TemplateDoesNotExist:
        return False
    return True

def site(req, sname, senv):
    if not wapp.start(req, sname, senv):
        return wapp.error_page()
    if not __find_template('help/site.html'):
        return wapp.error_page(500, 'help templates not found')
    tmpl_data = wapp.tmpl_data()
    return render(req, 'help/site.html', wapp.end(tmpl_data))
