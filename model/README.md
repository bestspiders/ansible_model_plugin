#jdk_install
```
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
```
#str_sub
```
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
```
