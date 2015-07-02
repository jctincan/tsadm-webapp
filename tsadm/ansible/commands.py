# $Id$

import subprocess


ansible_command = "/usr/bin/ansible {hostname} -i /home/jrms/git/tsadm/ansible/hosts.dev -o -u asb {extra_args} -a '{command_args}'"

commands_map = {
    'host_ssh_key': {
        'cmd': '/bin/cat ~/.ssh/id_rsa.pub',
        'extra_args': '-s'
    },
}


class AnsibleCommandError(Exception):
    pass


class AnsibleCommand:
    status = None
    output = None
    _log = None
    _valid_commands = None


    def __init__(self, log):
        self._log = log
        self._valid_commands = commands_map.keys()


    def run(self, host, command):
        if command not in self._valid_commands:
            raise AnsibleCommandError('invalid command')
        #~ self.status = -128
        self.status = 0
        self.output = None
        cmd_info = commands_map.get(command)
        cmd = ansible_command.format(hostname=host,
            command_args=cmd_info['cmd'],
            extra_args=cmd_info['extra_args']
        )
        self._log.dbg('ansible cmd: ', cmd)

        # FIXME: esto genera un loop porque estoy queriendo ejecutar un
        #        comando via ansible para generar el inventario mismo de
        #        ansible... Sí, muy inteligente...
        #~ self.status, self.output = subprocess.getstatusoutput(cmd, shell=True)

        self._log.dbg('ansible cmd status: ', self.status)
        if int(self.status) != 0:
            self._log.dbg('ansible cmd output: ', self.output)
            raise AnsibleCommandError('command failed: '+str(self.status))
        return self.output
