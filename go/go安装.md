
# Windows（Archive / zip）方式安装 Go 完整指南

> 适用系统：Windows 10 / Windows 11  
> 适用版本：Go 1.25.x（zip / Archive）  
> 适合人群：需要**手动控制安装路径 / 多版本共存**

---

## 一、下载安装包

1️⃣ 打开 Go 官方下载页  
Go 语言下载：[Downloads - The Go Programming Language](https://go.dev/dl/)
2️⃣ 下载：

```text
go1.25.5.windows-amd64.zip
```

📌 说明：
- `amd64` = 64 位 Windows（绝大多数）
- **不要选 msi**
- 不要选 `386`
---

## 三、配置环境变量
#### 解压到固定目录（推荐）
解压后目录结构应为：

```text
C:\Go
 ├─ bin\
 │   ├─ go.exe
 │   └─ gofmt.exe
 ├─ pkg\
 ├─ src\
 └─ VERSION
```

## 环境变量设置
### 配置 GOROOT

| 项目  | 值        |
| --- | -------- |
| 变量名 | `GOROOT` |
| 变量值 | `C:\Go`  |

---

### 配置 GOPATH

| 项目  | 值              |
| --- | -------------- |
| 变量名 | `GOPATH`       |
| 变量值 | `C:\go\gopath` |
|     |                |

---
### 配置 PATH

```text
%GOROOT%\bin
%GOPATH%\bin
```

### 最终目录 & 变量汇总（标准）

```text
GOROOT = E:\MyWork\go\go1.25.5\bin
GOPATH = E:\MyWork\go\gopath
PATH = %GOROOT%\bin;%GOPATH%\bin
```

---

### 检查环境变量

```bat
go env GOROOT
go env GOPATH

期望输出：
C:\Go
C:\go\gopath
```
### 检查 go.exe 路径

```bat
where go
应输出：
C:\Go\bin\go.exe
```

---
## 验证安装是否成功 

###  检查 Go 版本

```bat
go version
正确输出示例：
go version go1.25.5 windows/amd64
```

## 配置国内代理

```bat
go env -w GOPROXY=https://goproxy.cn,direct
go env -w GO111MODULE=on
验证：
```bat
go env GOPROXY
```

---

### 写一个测试程序

1.  新建目录

```bat
mkdir %GOPATH%\src\hello
cd %GOPATH%\src\hello
```

2. 创建 `main.go`

```go
package main

import "fmt"

func main() {
    fmt.Println("Hello, Go!")
}
```

3. 运行

```bat
go run main.go
输出：
Hello, Go!
```


---

## 常见问题排查

### ❌ 1️⃣ `'go' 不是内部或外部命令`

- `Path` 没配对
- 必须是：
    ```
    C:\Go\bin
    ```
### ❌ 2️⃣ `where go` 出现多个路径

- 说明装过多个 Go
- 调整 Path 顺序
- 或删除旧版本
### ❌ 3️⃣ 解压路径错误

❌ 错误示例：

```text
C:\Go\go\bin\go.exe
```

✅ 正确：

```text
C:\Go\bin\go.exe
```

---

## 卸载 / 升级（Archive 优势）

### 卸载

- 删除 `C:\Go`
- 删除环境变量
### 升级
- 解压新版本覆盖 `C:\Go`
- 或换目录指向新版本