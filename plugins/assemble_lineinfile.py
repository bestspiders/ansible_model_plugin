#-*- coding:utf-8 -*-
from ansible.plugins.action import ActionBase
from ansible.errors import AnsibleError, AnsibleFileNotFound
from ansible.module_utils._text import to_bytes, to_text
from ansible.module_utils.parsing.convert_bool import boolean
import shutil
import tempfile
import os,re
class ActionModule(ActionBase):
    
    def run(self, tmp=None, task_vars=None):
        
        # 调用 ActionBase的run
        if task_vars is None:
            task_vars = dict()
        result = super(ActionModule, self).run(tmp, task_vars)

        # 获取入参
        source = self._task.args.get('src', None)
        dest   = self._task.args.get('dest', None)
        sub_str=self._task.args.get('sub_str',None)
        remote_src= boolean(self._task.args.get('remote_src',False),strict=False)
        mode=self._task.args.get('mode',0755)
        if os.path.isfile(source)==False and remote_src== False:
            result['failed'] = True
            result['msg']=u'源文件不存在'
            return result
        try:
            tmp_source = self._loader.get_real_file(source)
        except AnsibleFileNotFound as e:
            result['failed'] = True
            result['msg'] = "could not find src=%s, %s" % (source, e)
            self._remove_tmp_path(tmp)
            return result
        try:
            if sub_str:
                str_dic = eval(sub_str)
                with open(tmp_source, 'r') as f:
                    will_sub=f.read()
                    for every_value in str_dic:
                        will_sub=re.sub(every_value,str_dic[every_value],will_sub)
                    template_data = to_text(will_sub)

            else:
                with open(tmp_source, 'r') as f:
                    template_data = to_text(f.read())

            resultant = self._templar.do_template(template_data, preserve_trailing_newlines=True, escape_backslashes=False)
        except Exception as e:
            result['failed'] = True
            result['msg'] = "%s: %s" % (type(e).__name__, to_text(e))
            return result
        finally:
            self._loader.cleanup_tmp_file(tmp_source)
        new_task=self._task.copy()
        new_task.args.pop('sub_str',None)
        if remote_src ==False:
            try:
                tempdir = tempfile.mkdtemp()
                result_file = os.path.join(tempdir, os.path.basename(source))
                with open(result_file, 'wb') as f:
                    f.write(to_bytes(resultant, errors='surrogate_or_strict'))
                new_task.args.update(
                    dict(
                        src=result_file,
                        dest=dest,
                        follow=False,
                        mode=mode,
                    ),
                )
                copy_action = self._shared_loader_obj.action_loader.get('copy',
                                                                    task=new_task,
                                                                    connection=self._connection,
                                                                    play_context=self._play_context,
                                                                    loader=self._loader,
                                                                    templar=self._templar,
                                                                    shared_loader_obj=self._shared_loader_obj)
                result.update(copy_action.run(task_vars=task_vars))
            finally:
                shutil.rmtree(tempdir)
                return result
        else:
            result.update(
                self._execute_module(
                    module_name='copy',
                    module_args=dict(
                    src=source,
                    dest=dest,
                    original_basename=os.path.basename(source),
                    follow=True,
                    remote_src=True,
                    mode=mode,
                    ),
                task_vars=task_vars,
                tmp=tmp,
                delete_remote_tmp=False,
                )
            )
            return result
 
