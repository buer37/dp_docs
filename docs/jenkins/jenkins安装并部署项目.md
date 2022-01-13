1. 安装jenkins https://get.jenkins.io/redhat-stable/

   ```
   yum -y install https://get.jenkins.io/redhat-stable/jenkins-2.319.1-1.1.noarch.rpm
   ```

2. Jenkins 默认使用`8080`端口，如果你的`8080`端口被占用了，请修改配置文件`/etc/sysconfig/jenkins`，将`JENKINS_PORT`字段配置成你想要的端口

   ```
   JENKINS_PORT="18080"
   JENKINS_HOME="/home/webapps/jenkins"
   JENKINS_USER="root"
   ```

3. 配置java路径,打开文件`/etc/rc.d/init.d/jenkins`，确认`candidates`中是否包括了你的Java路径

   ```
   candidates="
   /etc/alternatives/java
   /usr/lib/jvm/java-1.8.0/bin/java
   /usr/lib/jvm/jre-1.8.0/bin/java
   /usr/lib/jvm/java-1.7.0/bin/java
   /usr/lib/jvm/jre-1.7.0/bin/java
   /usr/lib/jvm/java-11.0/bin/java
   /usr/lib/jvm/jre-11.0/bin/java
   /usr/lib/jvm/java-11-openjdk-amd64
   /usr/bin/java
   "
   ```

4. 启动

   ```
    systemctl start jenkins
    #开机启动
    systemctl enable jenkins
   ```

   

5. 添加jenkins全局环境变量

   ![img](https://imgconvert.csdnimg.cn/aHR0cHM6Ly9pbWcyMDIwLmNuYmxvZ3MuY29tL2Jsb2cvMTU4MDk5OC8yMDIwMDUvMTU4MDk5OC0yMDIwMDUxMDExNDMxMDg0MS0yMDc5NjQ0NzIyLnBuZw?x-oss-process=image/format,png)

6. 构建sheel命令

   ```shell
   JARFILE=universe-project.jar
   DIR=/home/webapps/universe_carpool
   #打包,跳过测试
   mvn clean package -Dmaven.test.skip=true
   #进入打包后的文件夹,查看jar包是否存在
   cd ${WORKSPACE}/universe-project/target/
   if [ ! -e $JARFILE ]; then
       exit $JARFILE文件不存在
   fi
   #查看备份文件夹是否存在,并把旧的jar文件移动进来
   if [ ! -d $DIR/backup ];then
      mkdir -p $DIR/backup
   fi
   mv -f $DIR/$JARFILE $DIR/backup/$JARFILE
   #把新打包的jar文件移动到项目文件夹下
   mv -f $JARFILE $DIR/$JARFILE
   #查询当前运行的项目,并杀掉
   PID=`ps -ef |grep java|grep $JARFILE|grep -v grep|awk '{print $2}'`
   if [ "$PID" != "" ]; then
   	echo "App is running and pid = $PID, will kill it"
   	kill -9 $PID
   fi
   #运行新的jar包
   sudo -u root nohup /usr/java/jdk1.8.0_121/bin/java -jar $DIR/$JARFILE --spring.profiles.active=master > /home/webapps/universe_carpool/TGLI3KM72O.log 2>&1 &
   ```


7. gitee推送触发构建

   1. Jenkins → Manage Jenkins →Manage Plugins, 搜索gitee安装

   2. Manage Jenkins → Configure System → Gitee [Configuration](https://so.csdn.net/so/search?q=Configuration),获取Gitee API V5 的私人令牌配置上

   3. 项目配置-构建触发器,选择Gitee webhook触发构建,在下面生成Gitee WebHook 密码,要在 Gitee webhook 中填写 URL,并填写密码

8. vue项目构建

   ```sh
   DIR=/www/webfront/product
   FRONTDIR=gaoyuantong
   PROJECTDIR=dist-production
   npm install 
   #删除之前的打包文件夹
   rm -rf $PROJECTDIR
   #打包
   npm run buildProd
   #新建备份文件夹
   if [ ! -d $DIR/backup ];then
      mkdir -p $DIR/backup
   fi
   #删除备份文件夹之前的备份
   rm -rf $DIR/backup/$FRONTDIR
   #移动当前项目文件夹到备份文件夹里
   if [ -d $DIR/$FRONTDIR ];then
   	mv -f $DIR/$FRONTDIR $DIR/backup
   fi
   #把新打包的文件移入项目文件夹
   mv -f $PROJECTDIR $DIR/$FRONTDIR
   
   ```

   