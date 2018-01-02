#-*- coding:utf-8 -*-
#!/usr/bin/python
#author:王鑫
#2017.12.08 修改
"""
本模块针对官方编译包安装
环境为centos6/7
eg:
  vars:
    client_path: /usr/local/src
  tasks:
  - name: install jdk
    jdk_install:   #模块名字
      jdk_gz_path: /usr/local/src/jdk-7u80-linux-x64.tar.gz #jdk压缩包路径
      jdk_install_path: "{{client_path}}" #jdk安装路径
      add_env: yes #是否添加进换进变量（可选）默认为no
    register: jdk_info
  - name: check jdk
    debug: var=jdk_info #打印输出结果
"""
from ansible.module_utils.basic import *
import tarfile
def unzip(data):
    untar = tarfile.open(data['jdk_gz_path']) #解压压缩包
    first_name=untar.getnames()[0] #获取压缩包里的文件名
    untar.extractall(data['jdk_install_path'])
    untar.close()
    info=u'失败'
    if data['add_env']==False:
        pass
    else:
        judge_file=open('/etc/profile','r')
        judge_content=judge_file.read()
        judge_file.close()
        profile_file=open('/etc/profile','r')
        jdk_root='%s/%s' %(data['jdk_install_path'],first_name)
        if 'export JAVA_HOME' in judge_content:
            rewrite_jdk=open('/etc/profile','r+')
            for line in profile_file:
                if 'export JAVA_HOME' in line:
                    rewrite_jdk.write('export JAVA_HOME='+jdk_root+'\n')
                elif 'export JAVA_BIN' in line:
                    rewrite_jdk.write('export JAVA_BIN='+jdk_root+'\n')
                else:
                    rewrite_jdk.write(line)
            rewrite_jdk.close()
            info=u'成功'
        else:
            file=open('/etc/profile','a+')
             #拼接安装全路径
            jdk_path="""
export JAVA_HOME=%s
export JAVA_BIN=%s/bin
export JRE_HOME=$JAVA_HOME/jre
export PATH=$JAVA_HOME/bin:$JRE_HOME/bin:$PATH
export CLASSPATH=.:$JAVA_HOME/lib/dt.jar:$JAVA_HOME/lib/tools.jar:$JRE_HOME/lib
""" % (jdk_root,jdk_root)
            file.write(jdk_path)
            file.close()
            info=u'成功'
        profile_file.close()
    return first_name,info
def main():
    fields={
    "jdk_gz_path":{"required":True,"type":"str"}, #"required":True 为必选 False为可选
    "jdk_install_path":{"required":True,"type":"str"},
    "add_env":{"required":False,"defalut":False,"type":"bool"}
    }
    module = AnsibleModule(argument_spec=fields)
    data=module.params
    first_info,second_info=unzip(data)
    response = {u"解压文件": first_info,u'添加环境变量':second_info}
    module.exit_json(changed=True, meta=response)

if __name__ == '__main__':
    main()
    