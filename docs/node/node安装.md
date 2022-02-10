#### node

#### Windows

1. 检测安装是否成功, 分别查看node和npm版本

    ```
    node -v
    npm -v
    ```

2. 环境配置,主要配置的是npm安装的全局模块所在的路径，以及缓存cache的路径，因为npm install -g模块自动安装到c盘下，为了不占c盘空间，所以我们可以自定义模块所放位置

   	npm config set prefix "D:\node\node_global"
   	npm config set cache "D:\node\node_cache"

3. 查看所有全局安装模块

   	npm list -g --depth 0

4. 查看全局安装路径,prefix就是模块全局安装路径

   	npm config ls



#### Linux

1. 下载

   ```
   wget https://oss.npmmirror.com/dist/node/v14.16.1/node-v14.16.1-linux-x64.tar.xz
   ```

   解压

   ```
   tar -xvf node-v14.16.1-linux-x64.tar.xz
   ```

2. 配置软连接，使全局都可以使用node命令

   ```
   #将node源文件映射到usr/bin下的node文件
   ln -s /home/webfront/node-v14.16.1-linux-x64/bin/node /usr/bin/node
   ln -s /home/webfront/node-v14.16.1-linux-x64/bin/npm /usr/bin/npm
   ```

3. 配置node文件安装路径

   ```
   mkdir node_global
   mkdir node_cache
   npm config set prefix "node_global"
   npm config set cache "node_cache"
   ```

4. 查看node配置

   ```
   npm config list -l
   ```

5. 替换阿里镜像

   ```
   npm config set registry https://registry.npm.taobao.org 
   ```

   

