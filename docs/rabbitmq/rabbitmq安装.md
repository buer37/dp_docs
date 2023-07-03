### 离线非root安装rabbitmq

#### 需要的包：

​	rabbitmq需要erlang环境，erlang需要ncurses依赖库，需要openssl

- ncurses-6.0.tar.gz

  - 可以通过apt-get source libncurses5-dev获取源码，然后make && make install

- openssl-1.0.2k.tar.gz
  - [/source/old/1.0.2/index.html (openssl.org)](https://www.openssl.org/source/old/1.0.2/)
- rabbitmq-server-generic-unix-3.8.0.tar
  - github地址【rabbitmq-server-3.8.0.tar.xz】：[Release RabbitMQ 3.8.0 · rabbitmq/rabbitmq-server (github.com)](https://github.com/rabbitmq/rabbitmq-server/releases/tag/v3.8.0)
  - 官网所有版本：[RabbitMQ Project Announcements — RabbitMQ](https://www.rabbitmq.com/news.html)

- otp_src_21.3.8.2.tar.gz

  [Otp 21.3.8.2 - Erlang/OTP](https://www.erlang.org/patches/otp-21.3.8.2)

#### 安装openssl

在安装erlang的时候会有一个[报错](#erlang-error)，需要加上`-fPIC`编译安装

```bash
#!/bin/bash

rabbitmq_path=/home/dp/software/rabbitmq

echo install openssl......
cd $rabbitmq_path
tar -zxf openssl-1.0.2k.tar.gz
mkdir openssl
cd openssl-1.0.2k
#install config
./config -fPIC --prefix=$rabbitmq_path/openssl
echo make install openssl......
make && make install
openssl version
echo install openssl over......
```

#### 安装ncurses

> 一定要设置环境变量，不设置erlang安装的时候无法识别

```bash
#!/bin/bash

rabbitmq_path=/home/dp/software/rabbitmq

#ncurses-6.0.tar.gz
echo install ncurses......
cd $rabbitmq_path
tar -zxf ncurses-6.0.tar.gz
mkdir ncurses
cd ncurses-6.0

#install config
./configure --prefix=$rabbitmq_path/ncurses
echo make install ncurses......
make && make install

#设置环境变量，不设置erlang安装的时候无法识别
echo 'set env $LIBRARY_PATH $C_INCLUDE_PATH......'
echo 'export LIBRARY_PATH='$rabbitmq_path'/ncurses/lib:$LIBRARY_PATH' >> ~/.bashrc
echo 'export C_INCLUDE_PATH='$rabbitmq_path'/ncurses/include:$C_INCLUDE_PATH' >> ~/.bashrc
source ~/.bashrc

echo install ncurses over......
```

#### 安装erlang

```bash
#!/bin/bash

rabbitmq_path=/home/dp/software/rabbitmq

echo install erlang......
cd $rabbitmq_path
tar -zxf otp_src_21.3.8.2.tar.gz
mkdir erlang
cd otp_src_21.3.8.2

./configure --with-ssl=$rabbitmq_path/openssl --with-ncurses=$rabbitmq_path/ncurses --prefix=$rabbitmq_path/erlang
echo make install erlang......
make && make install
#profile
echo 'export ERLANG_HOME='$rabbitmq_path'/erlang' >> ~/.bashrc
echo 'export PATH=$PATH:$ERLANG_HOME/bin' >> ~/.bashrc
source ~/.bashrc
#打印erlang version
echo erlang version [`erl -eval 'erlang:display(erlang:system_info(otp_release)), halt().' -noshell`]
echo  install erlang over......
```



##### 报错找不到ncurses，需要安装ncurses，并配置环境变量

```
configure: error: No curses library functions found
configure: error: /bin/sh ‘/app/otp_src_20.2/erts/configure’ failed for erts
```

##### 安装erlang报错 {#erlang-error} 

```shell
/usr/bin/ld: /home/dp/software/rabbitmq/openssl/lib/libcrypto.a(cryptlib.o): relocation R_X86_64_PC32 against symbol `stderr@@GLIBC_2.2.5' can not be used when making a shared object; recompile with -fPIC /usr/bin/ld: 最后的链结失败: bad value collect2: error: ld returned 1 exit status make[4]: *** [x86_64-unknown-linux-gnu/Makefile:158：../priv/lib/x86_64-unknown-linux-gnu/crypto.so] 错误 1 make[4]: 离开目录“/home/dp/software/rabbitmq/otp_src_21.3.8.2/lib/crypto/c_src” make[3]: *** [/home/dp/software/rabbitmq/otp_src_21.3.8.2/make/run_make.mk:35：opt] 错误 2 make[3]: 离开目录“/home/dp/software/rabbitmq/otp_src_21.3.8.2/lib/crypto/c_src” make[2]: *** [/home/dp/software/rabbitmq/otp_src_21.3.8.2/make/otp_subdir.mk:29：opt] 错误 2 make[2]: 离开目录“/home/dp/software/rabbitmq/otp_src_21.3.8.2/lib/crypto” make[1]: *** [/home/dp/software/rabbitmq/otp_src_21.3.8.2/make/otp_subdir.mk:29：opt] 错误 2 make[1]: 离开目录“/home/dp/software/rabbitmq/otp_src_21.3.8.2/lib” make: *** [Makefile:490：libs] 错误 2
```

这个错误通常是由于缺少 `-fPIC` 标志导致的。`-fPIC` 表示编译时生成位置无关的代码，用于创建共享对象（shared object）文件。

要解决这个问题，你可以尝试以下方法：

1. 检查 OpenSSL 的安装：确保你已经正确安装了 OpenSSL 库，并且包含了正确的头文件和库文件。你可以尝试重新安装 OpenSSL 或更新到最新版本。

2. 确认 OpenSSL 库的编译选项：如果你是自行编译 OpenSSL 库的话，确保在编译时包含了 `-fPIC` 选项。你可以查阅 OpenSSL 的编译文档或配置文件来确认。

   ```
   ./config -fPIC
   ```

   清理并重新编译 Erlang：在重新编译 Erlang 之前，尝试清理旧的构建文件。运行以下命令：

   ```shell
   make clean
   ```

   然后重新运行 Erlang 的配置和编译过程。

3. 更新 Erlang 版本：如果以上方法都不起作用，你可以尝试更新到最新版本的 Erlang，可能会修复这个问题。





#### 安装rabbitmq

```bash
#!/bin/bash

rabbitmq_path=/home/dp/software/rabbitmq
echo $rabbitmq_path

cd $rabbitmq_path
tar -xvf rabbitmq-server-generic-unix-3.8.0.tar

echo 'export PATH=$PATH:'$rabbitmq_path'/rabbitmq_server-3.8.0/sbin' >> ~/.bashrc
source ~/.bashrc

cd rabbitmq_server-3.8.0
#enable web
rabbitmq-plugins enable rabbitmq_management
#start
rabbitmq-server -detached

#（1）添加用户 rabbitmq 密码：root
rabbitmqctl add_user rabbitmq root
# 配置权限
rabbitmqctl set_permissions -p "/" rabbitmq ".*" ".*" ".*"
rabbitmqctl list_user_permissions rabbitmq
rabbitmqctl set_user_tags rabbitmq administrator
rabbitmqctl delete_user guest
```

