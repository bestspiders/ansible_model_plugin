# assemble_lineinfile
在ansible服务器修改好配置文件传送到目标机器上<br>
这是一个ansible的action插件<br>
因为经常需要更新配置文件。如果只用ansible自带的包，就要copy+lineinfile。显然这很麻烦并且速度很慢。<br>
所以我参考了assemble与template。直接在ansible服务器上修改完，再传递，测试下来一个task能少10秒。当然如果是局域网，这个差距会小很多。主要是为了书写方便。<br>
用法：<br>
```
  - name: update file
    assemble_lineinfile:
      src: "/root/base.yaml"
      dest: "/root/base.yaml"
      sub_str: >
               {"#adserverredismaster start":"test\nthis is entry"
               ,"#zkhosts start":"txttest"}
      remote_src: no
      mode: 0777
```
插件使用的是copy模块<br>
sub_str填写的值为字典<br>
key为regexp值，键值是你你替换成的值<br>
# 注意:<br>
此替换操作仅限remote_src是False(默认也是False)<br>
# rec_raw_script
作为一个action插件仿照script插件编写，接受binascii.b2a_hex()编码后字符<br>
作用：为提供python api执行python脚本回显<br>
用法:<br>
```
编码前原内容:
#!/usr/bin/python
#-*- coding:utf-8 -*-
import os,sys
if __name__ == '__main__':
	os.mkdir('/root/www')
	print "hello world
```
```
  - name: exec script
    rec_raw_script:             
    content:      23212f7573722f62696e2f707974686f6e0a232d2a2d20636f64696e673a7574662d38202d2a2d0a696d706f7274206f732c7379730a6966205f5f6e616d655f5f203d3d20275f5f6d61696e5f5f273a0a096f732e6d6b64697228272f726f6f742f77777727290a097072696e74202268656c6c6f20776f726c6422
```
