#-*- coding:utf-8 -*-
#!/usr/bin/python
#author:王鑫
#2017.12.11
"""
#模块针对yaml里正则替换
 - str_sub:
     original_str: 192.168.1.0 #将192.168.1.0替换成192_168_1_0
     re_content: \.
     sub_str:_
"""
from ansible.module_utils.basic import *
import re
def sub_content(data):
    will_content=re.sub(data['re_content'], data['sub_str'],data['original_str'])
    will_list=will_content.split(data['sub_str'])
    return will_content,will_list
def main():
    fields={
    "original_str":{"required":False,"type":"str"}, #原内容
    "re_content": {"required":False,"type":"str"}, #替换的正则
    "sub_str":{"required":False,"type":"str"}, #结果
    }
    module = AnsibleModule(argument_spec=fields)
    data=module.params
    success_list,content_list=sub_content(data)
    response = {u"替换之后的结果": success_list}
    module.exit_json(changed=True, meta=response,result=success_list,result_list=content_list)

if __name__ == '__main__':
    main()