
from django.shortcuts import render

from tsadm.wapp import TSAdmWApp
wapp = TSAdmWApp()

from . import inventory
inventory.wapp = wapp


def invlist(req):
    if not wapp.start(req, '__inventory_list', acclvl='BOT'):
        return wapp.error_page()
    return wapp.json_response(inventory.getinv())
