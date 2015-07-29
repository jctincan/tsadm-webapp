
from django.shortcuts import render

import os

from tsadm.jobq.req import TSAdmJobQReqInvoke
from tsadm.wapp import TSAdmWApp
wapp = TSAdmWApp()


def home(req, sname, senv):
    if not wapp.start(req, sname, senv):
        return wapp.error_page()
    tmpl_data = wapp.tmpl_data()

    sources_cmd = TSAdmJobQReqInvoke('rsync.sources', wapp)
    rsources = sorted(sources_cmd.request_lines())

    tmpl_data['rsync'] = {
        'sources': rsources,
    }

    if wapp.regr_tests:
        regr_data = list()
        if wapp.site.name == 'regr':
            for e in wapp.site.envs_other:
                if e.get('name') == 'dev':
                    regr_data.append(wapp.site.name)
                    regr_data.append(e.get('name'))
                    regr_data.extend(rsources)
        tmpl_data.update(wapp.tmpl_regr_tests_data(regr_data))

    return render(req, 'rsync/home.html', wapp.end(tmpl_data))
