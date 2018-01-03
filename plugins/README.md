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
