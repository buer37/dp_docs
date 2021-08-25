#### mysql

 1. 环境变量

    - 配置MYSQL_HOME(mysql目录)
    - 把%MYSQL_HOME%\bin引入到path

 2. my.ini配置

    ```
    [mysqld]
    #设置3306端口
    port=3306
    #设置mysql的安装目录
    basedir=D:\mysql-5.7
    #设置mysql数据库的数据的存放目录
    datadir=D:\mysql-5.7\data
    #允许最大连接数
    max_connections=200
    #服务端使用的字符集默认为8比特编码的latin1字符集
    character-set-server=utf8
    #创建新表时将使用的默认存储引擎
    default-storage-engine=INNODB
    sql_mode=NO_ENGINE_SUBSTITUTION,STRICT_TRANS_TABLES
    #忽略密码
    #skip-grant-tables
    [mysql]
    #设置mysql客户端默认字符集
    default-character-set=utf8
    ```

    

3. 执行以下代码

   ```
   mysqld--defaults-file=my.ini--initialize-insecure
   //initialize-insecure生成空密码
   netstartmysql
   #启动
   #无密码不加-p
   mysql-uroot-p
   #修改密码
   set password for root@localhost = password('Abc123!@#321');
   #5.7版本
   update user set authentication_string=PASSWORD("Abc123!@#321") where user="root";
   #开启远程连接
   GRANT ALL PRIVILEGES ON *.* TO 'root'@'%' IDENTIFIED BY 'Abc123!@#321';
   #更新权限
   flush privileges;
   ```

 4. 创建用户并授权

    ```
    #创建用户
    create user qyjb@'localhost' identified by 'Abc123!@#321';
    #授权全部权限
    grant all privileges on *.* to qyjb;
    
    ```