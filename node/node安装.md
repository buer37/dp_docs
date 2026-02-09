#### node

#### macOS (M 系列芯片 / Homebrew)

1. 确保已安装 [Homebrew](https://brew.sh)。若未安装，在终端执行：

   ```bash
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   ```

   安装完成后按提示将 brew 加入 PATH（通常需执行提示中的 `echo` 和 `eval` 命令）。

2. 使用 Homebrew 安装 Node.js：

   ```bash
   brew install node
   ```

   Homebrew 会安装当前推荐的 LTS 版本，同时包含 `node`、`npm` 和 `npx`。

3. 验证安装是否成功：

   ```bash
   node -v
   npm -v
   ```

4. （可选）配置 npm 全局模块路径与缓存路径，避免占用系统目录：

   ```bash
   mkdir -p ~/node_global ~/node_cache
   npm config set prefix "$HOME/node_global"
   npm config set cache "$HOME/node_cache"
   ```

   将全局可执行目录加入 PATH，在 `~/.zshrc` 或 `~/.bash_profile` 中追加：

   ```bash
   export PATH="$HOME/node_global/bin:$PATH"
   ```

   然后执行 `source ~/.zshrc`（或 `source ~/.bash_profile`）使配置生效。

5. （可选）使用国内镜像加速：

   ```bash
   npm config set registry https://registry.npmmirror.com
   ```

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

5. 配置环境变量，在path中追加：

   ```
   D:\node\node_global
   ```

```PowerShell 
# 定义基础路径和子路径变量
$nodeBaseDir = "E:\MyWork\nodejs"
$nodeGlobalDir = Join-Path -Path $nodeBaseDir -ChildPath "node_global"
$nodeCacheDir = Join-Path -Path $nodeBaseDir -ChildPath "node_cache"

# 创建文件夹
if (-not (Test-Path -Path $nodeGlobalDir)) {
    New-Item -ItemType Directory -Path $nodeGlobalDir | Out-Null
    Write-Host "成功创建 $nodeGlobalDir 文件夹"
} else {
    Write-Host "$nodeGlobalDir 文件夹已存在"
}

if (-not (Test-Path -Path $nodeCacheDir)) {
    New-Item -ItemType Directory -Path $nodeCacheDir | Out-Null
    Write-Host "成功创建 $nodeCacheDir 文件夹"
} else {
    Write-Host "$nodeCacheDir 文件夹已存在"
}

# 设置 npm 配置
npm config set prefix $nodeGlobalDir
npm config set cache $nodeCacheDir

# 获取当前系统的 PATH 环境变量值
$currentPath = [Environment]::GetEnvironmentVariable("PATH", [EnvironmentVariableTarget]::Machine)

# 检查全局安装路径是否已经存在于 PATH 中
if (-not $currentPath.Contains($nodeGlobalDir)) {
    # 如果不存在，则将全局安装路径添加到 PATH 中
    $newPath = "$currentPath;$nodeGlobalDir"
    [Environment]::SetEnvironmentVariable("PATH", $newPath, [EnvironmentVariableTarget]::Machine)
    Write-Host "已将 $nodeGlobalDir 永久添加到系统 PATH 环境变量中"
} else {
    Write-Host "$nodeGlobalDir 已经存在于系统 PATH 环境变量中"
}

Write-Host "操作完成"
npm config ls
```

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

   

