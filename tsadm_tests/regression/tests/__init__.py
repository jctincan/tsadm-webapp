
from . import config

def load(tname):
    rt_build = config.LOAD_TESTS.get(tname)
    return rt_build(tname)
