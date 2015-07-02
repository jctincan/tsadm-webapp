# $Id: __init__.py 12188 2014-12-01 02:33:23Z jrms $

from . import config

def load(tname):
    rt_build = config.LOAD_TESTS.get(tname)
    return rt_build(tname)
