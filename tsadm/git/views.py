
from django.shortcuts import render
from django.http import HttpResponse

import os
import time
from base64 import b64decode

from tsadm.jobq.req import TSAdmJobQReqInvoke
from tsadm.jobq.cmd import TSAdmJobQCmdBuild
from .jobq import GIT_CMD_MAP

from tsadm.wapp import TSAdmWApp
wapp = TSAdmWApp()


def home(req, sname, senv):
    if not wapp.start(req, sname, senv):
        return wapp.error_page()
    tmpl_data = wapp.tmpl_data()

    git_commands = list()
    for cmd_name in sorted(GIT_CMD_MAP.keys()):
        cmd_data = GIT_CMD_MAP.get(cmd_name)
        cmd_obj = TSAdmJobQCmdBuild(wapp, cmd_name, cmd_data)
        if cmd_obj.meta.show:
            git_commands.append(cmd_obj.tmpl_data())
        del cmd_obj

    tmpl_data['git'] = {
        'commands': git_commands,
        'url': TSAdmJobQReqInvoke('git.url', wapp).request(),
        'branch': TSAdmJobQReqInvoke('git.branch', wapp).request(),
        'tags': TSAdmJobQReqInvoke('git.tags', wapp).request_lines(),
        'branches': TSAdmJobQReqInvoke('git.branches', wapp).request_lines(),
        }
    return render(req, 'git/home.html', wapp.end(tmpl_data))


def _pr_update_branch(git_hash, senv_id):
    job_id, cmd_rtrn, cmd_out = wapp.jobq.run('git.pull', ['--git_hash={}'.format(git_hash)], runbg=True, senv_id=senv_id)
    wapp.log.dbg('pr update branch: ', job_id, ' ', cmd_rtrn)
    if cmd_rtrn == 0:
        return True
    return False


def _pr_fetch_tags(senv_id):
    job_id, cmd_rtrn, cmd_out = wapp.jobq.run('git.fetch', [], runbg=True, senv_id=senv_id)
    wapp.log.dbg('pr fetch tags: ', job_id, ' ', cmd_rtrn)
    if cmd_rtrn == 0:
        return True
    return False


def _pr_fetch(senv_id):
    job_id, cmd_rtrn, cmd_out = wapp.jobq.run('git.fetch', [], runbg=True, senv_id=senv_id)
    wapp.log.dbg('pr fetch: ', job_id, ' ', cmd_rtrn)
    if cmd_rtrn == 0:
        return True
    return False


def _pr_check_update(git_hash, site_name, branch_name):
    resp_status = 400
    resp_body = ';-) ;-)'
    site_id = wapp.db.site_id(site_name)
    if site_id > wapp.db.SITE_ID_MIN:
        wapp.log.dbg('site_id: ', site_id)
        site_envs = wapp.db.siteenv_all(site_id)
        resp_status = 200
        resp_body = 'branch '
        if branch_name.startswith('refs/tags/'):
            resp_body = 'tag '
        for env in site_envs:
            # sleep a bit in devmode
            if wapp.devmode:
                time.sleep(1)
            env_locked = env.get('locked', 0)
            env_claimed = env.get('claimed', 0)
            env_id = env.get('id')
            env_live = env.get('live', 0)
            if not env_locked and not env_claimed and not env_live:
                if branch_name.startswith('refs/tags/'):
                    wapp.log.dbg('git.fetch ', site_name, ' ', env_id, ' ', env.get('name'))
                    # fetch tags if a tag was pushed
                    if _pr_fetch_tags(env_id):
                        resp_body += ':-) '
                    else:
                        resp_body += ":'( "
                else:
                    cmd_rtrn, cmd_out = wapp.jobq.cmd('git.branch', senv_id=env_id)
                    wapp.log.dbg('get branch cmd_rtrn: ', cmd_rtrn)
                    if cmd_rtrn == 0:
                        env_branch = cmd_out[0]
                        wapp.log.dbg('git update branch site env: {}.{}[{}] {}'.format(site_name, env.get('name'), env_id, env_branch))
                        if env_branch == branch_name:
                            # update branch
                            if _pr_update_branch(git_hash, env_id):
                                resp_body += ':-) '
                            else:
                                resp_body += ":'( "
                        else:
                            # fetch metadata
                            if _pr_fetch(env_id):
                                resp_body += '(-: '
                            else:
                                resp_body += ")': "
                    else:
                        wapp.log.err('getting env_branch: ', cmd_rtrn)
                        wapp.log.dbg('getting env_branch cmd_out: ', cmd_out)
            else:
                msg = "no updating environment because it's "
                if env_locked:
                    msg += "locked"
                elif env_claimed:
                    msg += "claimed"
                elif env_live:
                    msg += "set as live"
                msg += "\nrun git.pull manually please if you are sure what you are doing"
                # jobq log entry
                job_id = wapp.jobq.start('git.pull', '--git_hash={}'.format(git_hash), env_id)
                wapp.jobq.end(job_id, 1, msg)
    else:
        resp_status = 404
        resp_body = ':-('
        wapp.log.err('site not found: ', site_name)
    resp_body = resp_body.strip()
    if resp_body == '':
        resp_body = ':-|'
    return (resp_status, resp_body)


def post_receive(req):
    if not wapp.start(req, '__git/post_receive', '__git/post_receive', acclvl='BOT'):
        return wapp.error_page()
    resp_body = ';-)'
    resp_status = 400
    if req.method == 'POST':
        post_data = req.POST.get('tsadm_post_data', '')
        wapp.log.dbg('post_data: ', post_data)
        git_hash = None
        site_name = None
        branch_name = None
        try:
            post_lines = b64decode(post_data.encode('utf-8', 'replace')).decode('utf-8', 'replace').splitlines()
            wapp.log.dbg('post_lines: ', post_lines)
            git_hash = post_lines[0]
            site_name = post_lines[1]
            branch_name = post_lines[2]
            wapp.log.dbg('git_hash: ', git_hash)
            wapp.log.dbg('site_name: ', site_name)
            wapp.log.dbg('branch_name: ', branch_name)
        except Exception as e:
            wapp.log.err('post_lines: ', e)
            post_lines = ''
        # try to update site's branch
        resp_status, resp_body = _pr_check_update(git_hash, site_name, branch_name)
    else:
        wapp.log.err('only POSTs are useful')
    resp = HttpResponse(resp_body+'\n', content_type='text/plain; charset=utf-8', status=resp_status)
    wapp.end()
    return resp
