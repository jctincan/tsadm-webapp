
from tsadm.jobq.req import TSAdmJobQReqInvoke


class TSAdmSlave:
    _wapp = None
    id = None
    _info = None
    fqdn = None
    slug = None


    def __init__(self, wapp, slave_id):
        self._wapp = wapp
        self.id = slave_id
        self._info = self._wapp.db.slave_info(slave_id)
        self.fqdn = self._info.get('fqdn')
        self.slug = self._info.get('slug')

    def hostinfo(self):
        cmd_hostinfo = TSAdmJobQReqInvoke('slave.hostinfo', self._wapp)
        return cmd_hostinfo.request_lines()

    def softinfo(self):
        cmd_softinfo = TSAdmJobQReqInvoke('slave.softinfo', self._wapp)
        return cmd_softinfo.request_lines()

    def tmpl_data(self, hostinfo=True, softinfo=False):
        self._wapp.jobq.server_addr(self.fqdn)
        self._info['ipaddr'] = self._wapp.nsresolve(self.fqdn)
        if hostinfo:
            self._info['hostinfo'] = '\n'.join(self.hostinfo())
        if softinfo:
            self._info['softinfo'] = '\n'.join(self.softinfo())
        self._info['graphs_base_url'] = self._wapp.conf.get('SLAVE_GRAPHS_BASE_URL', '/slave/graphs')
        return {
            'server': self._info
        }
