
import time
from django.shortcuts import render, redirect

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


def addkey(req):
    if not wapp.start(req, '__user/addkey'):
        return wapp.error_page()

    wapp.log.dbg('req.POST:', req.POST)
    tsadm_cmd = req.POST.get('tsadm_cmd', None)

    if tsadm_cmd == 'userAddKey':
        input_ok = True
        key_name = req.POST.get('tsadm_user_key_name', None)
        key_text = req.POST.get('tsadm_user_key_text', None)

        if key_name is None or key_name == '':
            wapp.umesg.err('key name not provided')
            input_ok = False
        else:
            key_name = key_name.strip()
            wapp.log.dbg('user key name:', key_name)

        if key_text is None or key_text == '':
            wapp.umesg.err('key not provided')
            input_ok = False
        elif len(key_text.splitlines()) > 1:
            wapp.umesg.err('the key text contains more than one line')
            input_ok = False
        else:
            key_text = key_text.strip()
            wapp.log.dbg('user key text:', key_text)

        if input_ok:
            try:
                import_ok, err_msg = wapp.user.auth_key_import(key_name, key_text)
            except Exception as e:
                return wapp.error_page(500, str(e))
            else:
                if import_ok:
                    wapp.umesg.inf('key "'+key_name+'" added')
                else:
                    wapp.umesg.err('adding key "'+key_name+'" failed!')
                    wapp.umesg.err(err_msg)

    tmpl_data = wapp.tmpl_data()
    return render(req, 'user/addkey.html', wapp.end(tmpl_data))


def showkey(req, kfprint):
    if not wapp.start(req, '__user/showkey'):
        return wapp.error_page()
    tmpl_data = wapp.tmpl_data()
    tmpl_data['userAuthKey'] = wapp.db.user_auth_getkey(wapp.user.id, kfprint)
    if tmpl_data['userAuthKey'] is None:
        return wapp.error_page(400, 'invalid key')
    return render(req, 'user/showkey.html', wapp.end(tmpl_data))


def delkey(req, kfprint):
    if not wapp.start(req, '__user/delkey'):
        return wapp.error_page()
    tmpl_data = wapp.tmpl_data()
    tmpl_data['userAuthKey'] = wapp.db.user_auth_getkey(wapp.user.id, kfprint)
    if tmpl_data['userAuthKey'] is None:
        return wapp.error_page(400, 'invalid key')
    delConfirm = req.GET.get('tsadmConfirmRemove', None)
    if delConfirm is None:
        return render(req, 'user/delkey.html', wapp.end(tmpl_data))
    else:
        try:
            wapp.db.user_auth_delkey(wapp.user.id, kfprint)
        except Exception as e:
            return wapp.error_page(500, str(e))
        else:
            wapp.umesg.inf('auth key '+tmpl_data['userAuthKey']['key_name']+' removed!')
            tmpl_data['userAuthKey'] = '__removed__'
        return render(req, 'user/delkey.html', wapp.end(tmpl_data))
