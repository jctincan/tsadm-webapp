#!/usr/bin/python3
# $Id: merge.py 12399 2015-01-15 17:24:04Z jrms $

import sys
import os
import os.path
import subprocess


class G:
    src_dir = None
    dest_branch = None
    base_dir = None
    dst_dir = None
    last_merge_rev = None
    last_src_rev = None
    subpath = None
    src_branch = None


def print_info():
    print('src_dir:', G.src_dir)
    print('src_branch:', G.src_branch)
    #~ print('dest_branch:', G.dest_branch)
    print('base_dir:', G.base_dir)
    print('dst_dir:', G.dst_dir)
    #~ print('subpath:', G.subpath)
    print('last_merge_rev:', G.last_merge_rev)
    print('last_src_rev:', G.last_src_rev)


def get_subpath():
    G.subpath = input('subpath: ').strip()
    if G.subpath != '':
        G.src_dir = os.path.join(G.src_dir, G.subpath)
        G.dst_dir = os.path.join(G.dst_dir, G.subpath)


def get_info():
    G.src_dir = os.getcwd()
    G.src_branch = os.path.basename(os.path.dirname(os.path.dirname(G.src_dir)))
    G.dest_branch = input('dest branch: ')
    G.base_dir = os.path.dirname(os.path.dirname(os.path.dirname(G.src_dir)))
    G.dst_dir = os.path.join(G.base_dir, G.dest_branch, 'webapps', 'tsadm')
    get_subpath()


def pre_checks():
    if not os.path.exists(G.src_dir):
        print(G.src_dir, 'dir not found', file=sys.stderr)
        return False
    if not os.path.exists(G.dst_dir):
        print(G.dst_dir, 'dir not found', file=sys.stderr)
        return False
    return True


def shell_run(cmd):
    return subprocess.check_output(cmd, shell=True).decode().strip()


def get_last_merge_rev():
    cmd = "svn log --limit 20 {} 2>/dev/null | grep -E '^TSAdm: merge {}->{}' | head -n 1 | cut -d ':' -f 3 | cut -d ' ' -f 1".format(G.dst_dir, G.src_branch, G.dest_branch)
    return shell_run(cmd)


def get_last_src_rev():
    cmd = "svn info {} | fgrep 'Last Changed Rev:' | cut -d':' -f2".format(G.src_dir)
    return shell_run(cmd)


def get_svn_info():
    try:
        G.last_merge_rev = get_last_merge_rev()
        G.last_src_rev = get_last_src_rev()
        if int(G.last_src_rev) < int(G.last_merge_rev):
            print('src rev:', G.last_src_rev, 'is lower than merge rev:', G.last_merge_rev, file=sys.stderr)
            return False
    except Exception as e:
        print(e, file=sys.stderr)
        return False
    return True


def askyn(question):
    r = input('{} [y/N]: '.format(question))
    if r == 'y' or r == 'Y':
        return True
    else:
        print('aborting...', file=sys.stderr)
    return False


def merge():
    cmd = 'svn merge -r {}:{} {} {}'.format(G.last_merge_rev, G.last_src_rev, G.src_dir, G.dst_dir)
    print(cmd)
    if askyn('continue?'):
        #~ shell_run(cmd)
        os.system(cmd)
        return True
    return False


def edit_dst_version():
    vpath = os.path.join(G.dst_dir, 'VERSION.txt')
    if os.path.exists(vpath):
        print(vpath)
        if askyn('edit version file?'):
            os.system('vim {}'.format(vpath))


def merge_commit():
    edit_dst_version()
    cmd = "svn ci -m 'TSAdm: merge {}->{} {}:{}'".format(G.src_branch, G.dest_branch, G.last_merge_rev, G.last_src_rev)
    print()
    print(cmd)
    if askyn('commit merge?'):
        os.chdir(G.dst_dir)
        os.system(cmd)
        os.chdir(G.src_dir)
        return True
    return False


def main():
    get_info()
    if not pre_checks():
        return 1
    if not get_svn_info():
        return 2
    print_info()
    print()
    if not merge():
        return 3
    print()
    if not merge_commit():
        return 4
    return 0


if __name__ == '__main__':
    sys.exit(main())
