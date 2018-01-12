#-*- coding:utf-8 -*-
#!/usr/bin/python
#author: wang
#2017.1.7
"""
#模块针对yaml里正则替换
 - str_sub:
     original_str: 192.168.1.0 #将192.168.1.0替换成192_168_1_0
     re_content: \.
     sub_str:_
返回替换的内容和字符分割的列表
 - str_sub:
     original_str: ['192.168.1.12','10.150.21.34']
     re_content: 10\.150\.
返回匹配的内容
"""
from ansible.module_utils.basic import *
import re
def sub_content(data):
    try:
        will_content=re.sub(data['re_content'], data['sub_str'],data['original_str'])
        will_list=will_content.split(data['sub_str'])
    except:
        will_content,will_list=0,0
    try:
        get_compile=eval(data['original_str'])
        compile_list=[]
        for every_search in get_compile:
            if re.search(data['re_content'], every_search):
                compile_list.append(every_search)
    except:
        compile_list=[]
    return will_content,will_list,compile_list
def main():
    fields={
    "original_str":{"required":False,"type":"str"}, #原内容
    "re_content": {"required":False,"type":"str"}, #替换的正则
    "sub_str":{"required":False,"type":"str"}, #结果
    }
    module = AnsibleModule(argument_spec=fields)
    data=module.params
    success_list,content_list,may_compile=sub_content(data)
    response = {u"替换之后的结果": success_list}
    module.exit_json(changed=True, meta=response,result=success_list,result_list=content_list,compile_content=may_compile)

if __name__ == '__main__':
    main();
