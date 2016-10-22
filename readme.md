环境要求：
=========
bs4,requests
</br>用法:
=========
[windows]
---------
python write.py
</br>根据提示输入,如输错直接回车
</br>设置定时任务 python main.py
[linux]
---------
python2 write.py
</br>根据提示输入，如输错直接回车
</br>crontab -e
</br>添加一行
</br>0 0 * * * /usr/bin/python2 /root/main.py> /root/log.log 2>&1 &
</br>其中 /root/ 为你上传的文件夹
</br>/usr/bin/python2 为python 解析器所在位置
