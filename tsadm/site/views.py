
import os
import time

from django.shortcuts import render, redirect

from tsadm.wapp import TSAdmWApp
wapp = TSAdmWApp()

from . import envs_all


def index(req):
    if not wapp.start(req, '__site/index', '__site/index'):
        return wapp.error_page()

    regrt_data = list()
    sites_no = 0
    envs_no = 0
    s_all = wapp.db.site_all()
    se_all = list()
    for s in s_all:
        sites_no += 1
        show_site = False
        sd = dict()
        sd['name'] = s[1]
        envs = wapp.db.siteenv_all(s[0])
        sd['envs'] = list()
        for e in envs:
            envs_no += 1
            if e['id'] in wapp.user.siteenv_acl or 0 in wapp.user.siteenv_acl:
                #~ ed = {
                    #~ 'name': e['name'],
                    #~ 'locked': e['locked'],
                    #~ 'claimed': e['claimed']
                #~ }
                if sd['name'] == 'regr':
                    if e['name'] == 'dev' or e['name'] == 'test':
                        regrt_data.append(sd['name'] + e['name'])
                ed = dict()
                ed.update(e)
                if ed['locked']:
                    if e['locked_by'] == wapp.user.name:
                        ed['locked_by'] = 'you'
                if ed['claimed']:
                    if e['claimed_by'] == wapp.user.name:
                        ed['claimed_by'] = 'you'
                sd['envs'].append(ed)
                show_site = True
        if show_site:
            se_all.append(sd)

    tmpl_data = wapp.tmpl_data()
    tmpl_data['se_all'] = se_all
    tmpl_data['sites_no'] = sites_no
    tmpl_data['envs_no'] = envs_no
    tmpl_data.update(wapp.tmpl_regr_tests_data(regrt_data))
    return render(req, 'site/index.html', wapp.end(tmpl_data))


def dashboard(req, sname, senv, wapp_start=True):
    if wapp_start:
        if not wapp.start(req, sname, senv):
            return wapp.error_page()
    tmpl_data = wapp.tmpl_data()
    # -- jobq log
    tmpl_data['jobq'] = dict()
    tmpl_data['jobq']['log'] = list()
    db_log = wapp.db.jobq_senv_all(wapp.site.env.id)
    for dbe in db_log:
        dbe['id_slug'] = '{}...{}'.format(dbe['id'][:7], dbe['id'][-7:])
        if dbe['cmd_exit'] == 0:
            dbe['css_class'] = 'ok'
        elif dbe['cmd_exit'] == 9999:
            dbe['css_class'] = 'start'
        elif dbe['cmd_exit'] == 9090:
            dbe['css_class'] = 'run'
        else:
            dbe['css_class'] = 'error'
        if dbe['status'] == 'END':
            dbe['cmd_took'] = '{}s'.format(dbe['tstamp_end'] - dbe['tstamp_start'])
        else:
            dbe['cmd_took'] = '.'
        dbe['date'] = time.strftime(wapp.conf.get('LOG_DATE_FMT'), time.localtime(dbe['tstamp_start']))
        tmpl_data['jobq']['log'].append(dbe)
    del db_log
    return render(req, 'site/dashboard.html', wapp.end(tmpl_data))


def lock_confirm(req, sname, senv):
    if not wapp.start(req, sname, senv):
        return wapp.error_page()
    tmpl_data = wapp.tmpl_data()
    jobr_id = wapp.jobq.idgen()
    tmpl_data['lock'] = dict()
    tmpl_data['lock']['jobr_id'] = jobr_id
    wapp.db.siteenv_lock_req(wapp.site.env.id, jobr_id, wapp.user.id)
    return render(req, 'site/lock_confirm.html', wapp.end(tmpl_data))


def lock(req, sname, senv, confirm):
    if not wapp.start(req, sname, senv):
        return wapp.error_page()
    tmpl_data = wapp.tmpl_data()
    jid = wapp.jobq.start('env.lock', '')
    wapp.db.siteenv_lock(wapp.site.env.id, confirm, wapp.user.id)
    wapp.jobq.end(jid, 0, 'env locked')
    tmpl_data['load_sites_navbar'] = False
    return render(req, 'site/locked.html', wapp.end(tmpl_data))


def unlock_confirm(req, sname, senv):
    if not wapp.start(req, sname, senv, unlock_req=True):
        return wapp.error_page()
    tmpl_data = wapp.tmpl_data()
    jobr_id = wapp.jobq.idgen()
    tmpl_data['unlock'] = dict()
    tmpl_data['unlock']['jobr_id'] = jobr_id
    wapp.db.siteenv_unlock_req(wapp.site.env.id, jobr_id)
    return render(req, 'site/unlock_confirm.html', wapp.end(tmpl_data))


def unlock(req, sname, senv, jobr_id):
    if not wapp.start(req, sname, senv, unlock_req=True):
        return wapp.error_page()
    jid = wapp.jobq.start('env.unlock', '')
    wapp.db.siteenv_unlock(wapp.site.env.id, jobr_id, wapp.user.id)
    wapp.jobq.end(jid, 0, 'env unlocked')
    wapp.end()
    return redirect('site:dashboard', sname, senv)


def claim_confirm(req, sname, senv):
    if not wapp.start(req, sname, senv):
        return wapp.error_page()
    tmpl_data = wapp.tmpl_data()
    jobr_id = wapp.jobq.idgen()
    tmpl_data['jobr_id'] = jobr_id
    wapp.db.siteenv_claim_req(jobr_id, wapp.user.id, wapp.site.env.id)
    return render(req, 'site/claim_confirm.html', wapp.end(tmpl_data))


def claim(req, sname, senv, confirm):
    if not wapp.start(req, sname, senv):
        return wapp.error_page()
    jid = wapp.jobq.start('env.claim', '')
    wapp.db.siteenv_claim(wapp.site.env.id, confirm, wapp.user.id)
    wapp.jobq.end(jid, 0, 'env claimed')
    wapp.end()
    return redirect('site:dashboard', sname, senv)


def release_confirm(req, sname, senv):
    if not wapp.start(req, sname, senv):
        return wapp.error_page()
    tmpl_data = wapp.tmpl_data()
    jobr_id = wapp.jobq.idgen()
    tmpl_data['jobr_id'] = jobr_id
    wapp.db.siteenv_release_req(jobr_id, wapp.user.id, wapp.site.env.id)
    return render(req, 'site/release_confirm.html', wapp.end(tmpl_data))


def release(req, sname, senv, confirm):
    if not wapp.start(req, sname, senv):
        return wapp.error_page()
    jid = wapp.jobq.start('env.release', '')
    wapp.db.siteenv_release(wapp.site.env.id, confirm, wapp.user.id)
    wapp.jobq.end(jid, 0, 'env released')
    wapp.end()
    return redirect('site:dashboard', sname, senv)


def log(req, sname, senv):
    if not wapp.start(req, sname, senv):
        return wapp.error_page()
    tmpl_data = wapp.tmpl_data()
    site_log = list()
    for le in wapp.db.site_log(wapp.site.id):
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
        site_log.append(le)
    tmpl_data['site']['log'] = site_log
    return render(req, 'site/log.html', wapp.end(tmpl_data))


def admin(req):
    if not wapp.start(req, '__site/admin', acclvl='SITE_ADMIN'):
        return wapp.error_page()
    tmpl_data = wapp.tmpl_data()
    tmpl_data['envs_all'] = envs_all(wapp)
    tmpl_data['admin'] = {
        'cmds': ['site.checks', 'lalala'],
    }
    return render(req, 'site/admin.html', wapp.end(tmpl_data))


def env_redir(req):
    if not wapp.start(req, '__site/envRedir'):
        return wapp.error_page()
    envRedir = req.POST.get('tsadmEnvRedir', None)
    if envRedir is None or envRedir == '':
        return wapp.error_page(400, 'invalid request -1')
    try:
        sName = envRedir.split('.')[0]
        eName = envRedir.split('.')[1]
    except IndexError:
        return wapp.error_page(400, 'invalid request -2')
    return redirect('site:dashboard', sName, eName)
