### Linux学习

1. ps 英文全拼：process status）命令用于显示当前进程的状态，类似于 windows 的任务管理器

2. grep 用于查找文件里符合条件的字符串

   ```
   ps -ef|grep universe_test|grep -v grep
   查询universe_test关键字的进程,但不显示grep本身
   常用参数：
   -A    显示所有进程（等价于-e）(utility)
   -a    显示一个终端的所有进程，除了会话引线
   -N    忽略选择。
   -d    显示所有进程，但省略所有的会话引线(utility)
   -x    显示没有控制终端的进程，同时显示各个命令的具体路径。dx不可合用。（utility）
   -p    pid 进程使用cpu的时间
   -u    uid or username 选择有效的用户id或者是用户名
   -g    gid or groupname 显示组的所有进程。
   U     username 显示该用户下的所有进程，且显示各个命令的详细路径。如:ps U zhang;(utility)
   -f    全部列出，通常和其他选项联用。如：ps -fa or ps -fx and so on.
   -l    长格式（有F,wchan,C 等字段）
   -j    作业格式
   -o    用户自定义格式。
   v     以虚拟存储器格式显示
   s     以信号格式显示
   -m    显示所有的线程
   -H    显示进程的层次(和其它的命令合用，如：ps -Ha)（utility）
   e     命令之后显示环境（如：ps -d e; ps -a e）(utility)
   h     不显示第一行
   
   ps 的参数说明
   l     长格式输出；
   u     按用户名和启动时间的顺序来显示进程；
   j     用任务格式来显示进程；
   f     用树形格式来显示进程；
   a     显示所有用户的所有进程（包括其它用户）。显示所有进程
   -a    显示同一终端下的所有程序
   x     显示无控制终端的进程；
   r     显示运行中的进程；
   ww    避免详细参数被截断；
   -A    列出所有的进程
   -w    显示加宽可以显示较多的资讯
   -au   显示较详细的资讯
   -aux  显示所有包含其他使用者的进程
   -e    显示所有进程,环境变量
   -f    全格式
   -h    不显示标题
   -l    长格式
   -w    宽输出
   a     显示终端上地所有进程,包括其他用户地进程
   r     只显示正在运行地进程
   x     显示没有控制终端地进程
   grep参数说明
   -a 或 --text : 不要忽略二进制的数据。
   -A<显示行数> 或 --after-context=<显示行数> : 除了显示符合范本样式的那一列之外，并显示该行之后的内容。
   -b 或 --byte-offset : 在显示符合样式的那一行之前，标示出该行第一个字符的编号。
   -B<显示行数> 或 --before-context=<显示行数> : 除了显示符合样式的那一行之外，并显示该行之前的内容。
   -c 或 --count : 计算符合样式的列数。
   -C<显示行数> 或 --context=<显示行数>或-<显示行数> : 除了显示符合样式的那一行之外，并显示该行之前后的内容。
   -d <动作> 或 --directories=<动作> : 当指定要查找的是目录而非文件时，必须使用这项参数，否则grep指令将回报信息并停止动作。
   -e<范本样式> 或 --regexp=<范本样式> : 指定字符串做为查找文件内容的样式。
   -E 或 --extended-regexp : 将样式为延伸的正则表达式来使用。
   -f<规则文件> 或 --file=<规则文件> : 指定规则文件，其内容含有一个或多个规则样式，让grep查找符合规则条件的文件内容，格式为每行一个规则样式。
   -F 或 --fixed-regexp : 将样式视为固定字符串的列表。
   -G 或 --basic-regexp : 将样式视为普通的表示法来使用。
   -h 或 --no-filename : 在显示符合样式的那一行之前，不标示该行所属的文件名称。
   -H 或 --with-filename : 在显示符合样式的那一行之前，表示该行所属的文件名称。
   -i 或 --ignore-case : 忽略字符大小写的差别。
   -l 或 --file-with-matches : 列出文件内容符合指定的样式的文件名称。
   -L 或 --files-without-match : 列出文件内容不符合指定的样式的文件名称。
   -n 或 --line-number : 在显示符合样式的那一行之前，标示出该行的列数编号。
   -o 或 --only-matching : 只显示匹配PATTERN 部分。
   -q 或 --quiet或--silent : 不显示任何信息。
   -r 或 --recursive : 此参数的效果和指定"-d recurse"参数相同。
   -s 或 --no-messages : 不显示错误信息。
   -v 或 --invert-match : 显示不包含匹配文本的所有行。
   -V 或 --version : 显示版本信息。
   -w 或 --word-regexp : 只显示全字符合的列。
   -x --line-regexp : 只显示全列符合的列。
   -y : 此参数的效果和指定"-i"参数相同。
   ```

   输出格式:

   ```
   USER PID %CPU %MEM VSZ RSS TTY STAT START TIME COMMAND
   ```

3. kill 用于删除执行中的程序或工作 kill -9 23132

   ```
   最常用的信号：
   1 (HUP)：重新加载进程。
   9 (KILL)：杀死一个进程。
   15 (TERM)：正常停止一个进程。
   ```


4. sudo 以系统管理者的身份执行指令，也就是说，经由 sudo 所执行的指令就好像是 root 亲自执行

5. nohup 用于在系统后台不挂断地运行命令，退出终端不会影响程序的运行。

   ```
   sudo -u root nohup /usr/java/jdk1.8.0_121/bin/java -jar /root/webapps/Universe3_test.jar --server.port=8090 >> /tmp/UCLV68CPGA.log 2>&1 &
   ```

6. linux内存使用率查看

   ```
   ps -eo pmem,pcpu,rss,vsize,args | sort -k 1 -r | less
   ```

   