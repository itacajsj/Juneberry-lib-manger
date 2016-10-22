环境要求：
=========
bs4,requests
用法:
=========
[windows]
---------
python write.py
根据提示输入,如输错直接回车
设置定时任务 python main.py
[linux]
---------
python2 write.py
根据提示输入，如输错直接回车
crontab -e
添加一行
0 0 * * * /usr/bin/python2 /root/main.py> /root/log.log 2>&1 &
其中 /root/ 为你上传的文件夹
/usr/bin/python2 为python 解析器所在位置
