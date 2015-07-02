# $Id: cmd.py 12391 2015-01-15 04:52:43Z jrms $

class _CmdMeta:
    desc = None
    show = True
    admin = False

    def tmpl_data(self):
        return {
            'desc': self.desc,
        }


class TSAdmJobQCmd:
    name = None
    log = None
    db = None
    jobq = None
    env_id = None
    runbg = True
    meta = None

    def __init__(self, name, wapp, meta_opts=None):
        self.name = name
        self.log = wapp.log
        self.db = wapp.db
        self.jobq = wapp.jobq
        self.env_id = wapp.jobq.env_id()
        self.meta = _CmdMeta()
        if meta_opts is not None:
            self.__load_meta(meta_opts)

    def __load_meta(self, opts):
        for mk, mv in opts.items():
            if hasattr(self.meta, mk):
                setattr(self.meta, mk, mv)
            else:
                self.log.err('TSAdmJobQCmd: invalid cmd meta key ', mk)

    def request(self):
        cmd_rtrn, cmd_out = self.jobq.cmd(self.name)
        return cmd_out[0]

    def request_lines(self):
        cmd_rtrn, cmd_out = self.jobq.cmd(self.name)
        return cmd_out

    def execute(self, args=''):
        jobq_id, cmd_rtrn, cmd_out = self.jobq.run(self.name, args, runbg=self.runbg)
        return jobq_id


class TSAdmJobQCmdNotFound(Exception):
    pass


class TSAdmJobQCmdInvoke:
    __cmd = None

    def __init__(self, class_map, cmd_name, wapp):
        cmd_data = class_map.get(cmd_name, None)
        if cmd_data is None:
            raise TSAdmJobQCmdNotFound('not implemented')
        cmd_class = None
        cmd_meta = None
        if type(cmd_data) is type(tuple()):
            cmd_class = cmd_data[0]
            cmd_meta = cmd_data[1]
        else:
            cmd_class = cmd_data
        self.__cmd = cmd_class(cmd_name, wapp, cmd_meta)

    def request(self):
        return self.__cmd.request()

    def request_lines(self):
        return self.__cmd.request_lines()

    def execute(self, args=''):
        return self.__cmd.execute(args)


class TSAdmJobQCmdBuild:
    __cmd = None
    meta = None

    def __init__(self, wapp, cmd_name, cmd_data):
        cmd_class = None
        cmd_meta = None
        if type(cmd_data) is type(tuple()):
            cmd_class = cmd_data[0]
            cmd_meta = cmd_data[1]
        else:
            cmd_class = cmd_data
        self.__cmd = cmd_class(cmd_name, wapp, cmd_meta)
        self.meta = self.__cmd.meta

    def request(self):
        return self.__cmd.request()

    def request_lines(self):
        return self.__cmd.request_lines()

    def execute(self, args=''):
        return self.__cmd.execute(args)

    def tmpl_data(self):
        return {
            'name': self.__cmd.name,
            'meta': self.__cmd.meta.tmpl_data(),
        }
