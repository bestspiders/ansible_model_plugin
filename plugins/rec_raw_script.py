#-*- coding:utf-8 -*-
import os
import re
import shlex
import binascii
from ansible.errors import AnsibleError
from ansible.module_utils._text import to_native, to_text
from ansible.plugins.action import ActionBase
class ActionModule(ActionBase):
    TRANSFERS_FILES = True

    # On Windows platform, absolute paths begin with a (back)slash
    # after chopping off a potential drive letter.
    windows_absolute_path_detection = re.compile(r'^(?:[a-zA-Z]\:)?(\\|\/)')
    def run(self, tmp=None, task_vars=None):
        ''' handler for file transfer operations '''
        if task_vars is None:
            task_vars = dict()
        result = super(ActionModule, self).run(tmp, task_vars)
        if not tmp:
            tmp = self._make_tmp_path()
        str_content=self._task.args.get('content',None)
        arg_py=self._task.args.get('py_arg',None)
        my_plugin_module='special_script.py'
        if arg_py:
            my_plugin_module=my_plugin_module+' '+arg_py
        will_content=binascii.a2b_hex(str_content)
        tmp_src = self._connection._shell.join_path(tmp, os.path.basename(my_plugin_module))
        self._transfer_data(tmp_src,will_content)
        self._fixup_perms2((tmp_src, tmp_src), execute=True)
        script_cmd = self._connection._shell.wrap_for_exec(tmp_src)
        exec_data = None
        result.update(self._low_level_execute_command(cmd=script_cmd, in_data=exec_data, sudoable=True))
        self._remove_tmp_path(tmp)
        return result