## 配置git环境：git config --[global](https://so.csdn.net/so/search?q=global&spm=1001.2101.3001.7020)

参数讲解：

> config：参数是用来配置git环境的
>
> --global：长命令表示配置整个git环境

初次使用git需要设置你的用户名以及邮箱，这将作为当前机器git的标识，如果你用它来下载远程仓库一些需要登录权限的仓库会要求登录，git默认使用配置邮箱以及用户名登入，但会要求你手动输入密码

用户名配置

> user代表用户，.name代表配置用户的名称

```bash
git config --global user.name "你的用户名"
```

邮箱配置

> user代表用户，.email代表配置用户的邮箱

```bash
git config --global user.email "你的邮箱"
```

不配置也行，当遇到要求登录权限的远程仓库会让你在手动输入用户名、邮箱、以及密码

## 创建本地空仓库：git init

> init：初始化当前目录为仓库，初始化后会自动将当前仓库设置为master

创建本地仓库的条件是需要一个空目录，然后在空目录中初始化你的项目

如我想创建一个名为“test”的空项目

1.创建目录

```bash
mkdir test
```

2.进入目录

```bash
cd test
```

3.使用git init初始化当前仓库

```bash
git init
```

![img](git.assets/20201229120401474.png)

初始化后会生成git的配置文件目录，普通的"ls"命令是看不到的，我们需要使用ls -ah查看隐藏目录

![img](git.assets/20201229120449115.png)

进入目录后可以看到它的相关配置文件

![img](git.assets/20201229120528503.png)

## 新建文件添加到本地仓库：git add、git [commit](https://so.csdn.net/so/search?q=commit&spm=1001.2101.3001.7020) -m

> add：将文件添加到缓存区
>
> commit：提交到本地仓库

用我刚刚上一节所创建的空仓库test为例，我们用touch命令新建一个文件，名为test.c

```bash
touch test.c
```

![img](git.assets/20201229120818287.png)

使用git add命令将文件添加到本地仓库的提交缓存

```bash
git add test.c 
```

这个时候还不算添加到了本地仓库，我们还需要使用git commit命令为其添加修改的描述信息

```bash
git commit -m "add new file \"test.c\""
```

> -m命令来简写描述我们的信息，如果不使用-m，会调用终端的注释编辑器让你输入描述信息

git commit 会为我们生成40位的哈希值，用于作为id，并把刚刚用git add添加到提交缓存区里的文件提交到本地仓库中，便于我们回滚，至此，这个文件就已经添加到本地仓库中了，同时本地仓库也迭代了一个版本。

### 改写提交：git commit --amend

> --amend：重写上一次的提交信息

就像刚刚的列子里一样，我们提交了仓库，但是发现注释写错了，我们可以使用 --amend长命令选项来改写提交

```bash
git commit --amend
```

输入上面的命令后会进入如下编辑器界面：

![img](git.assets/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L2JqYnpfY3h5,size_16,color_FFFFFF,t_70.png)

我们输入Y选中是

可以看到刚刚的注释信息

![img](git.assets/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L2JqYnpfY3h5,size_16,color_FFFFFF,t_70-1684119810152-1.png)

在界面中按下“i”即可进入编辑界面

![img](git.assets/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L2JqYnpfY3h5,size_16,color_FFFFFF,t_70-1684119810152-2.png)

修改完成后按下ctrl+o键

![img](git.assets/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L2JqYnpfY3h5,size_16,color_FFFFFF,t_70-1684119810153-3.png)

在按下回车，就会提示已写入，用#是注释，不会被提交，git会自动过滤

![img](git.assets/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L2JqYnpfY3h5,size_16,color_FFFFFF,t_70-1684119810153-4.png)

下面的^G和^O这种符号^在ascii里对应ctrl键，所以就是ctrl+x

![img](git.assets/20201229123400641.png)

按下ctrl+x(不分大小写)即可退出编辑界面

## 查看历史提交日志：git log

> log：查看日志

正如刚刚改写提交的，想要确定是否改写成功，我们可以使用git log查看一下

```bash
git log
```

![img](git.assets/2020122912354456.png)

可以看到没有生成新的版本号，而是直接改写了刚刚提交的注释

这里来解释一下上面提交的信息是什么意思

第一行的commit是哈希算法算出的id，正如一开始所说，分布式是没有一个主版本号的，它们都是用id来做标志的，同时用master作为主仓库，其它的分支怎么迭代都不会影响到master，后面我会介绍如何使用分支

目前我们的仓库就是master，因为我们没有拉取分支是直接用git init创建的，就是master。

```bash
commit b9e3a0d708ee5a81ea5ff383c6dabe716eec8cf1 (HEAD -> master)
```

后面的head是指向的意思，表示这次提交到哪儿，head->master代表这次提交到master主仓库，如果是head->分支仓库则代表提交到分支仓库

Author是提交者是谁的意思，显示格式是：用户名 <邮箱>

```bash
Author: StephenZhou <stephenzhou@StephenZhou.www.malloc.pro>
```

Date的意思是提交时间，后面的+0800这个是格林尼治时间，代表当前是以哪儿的时间地作为基准，这是世界时间，用它来作为基数与当前所在地时差进行计算，包括地球自转等公式。

```bash
Date:   Tue Dec 29 12:15:13 2020 +0800
```

最下面的就是注释了

```bash
 test add new file "test.c"
```

回滚代码仓库：git [reset](https://so.csdn.net/so/search?q=reset&spm=1001.2101.3001.7020) --hard

reset参数是重置命令

--hard是重置代码仓库版本

有三种模式

`--soft` 、`--mixed`以及`--hard`是三个恢复等级。

- 使用`--soft`就仅仅将头指针恢复，已经add的暂存区以及工作空间的所有东西都不变。
- 如果使用`--mixed`，就将头恢复掉，已经add的暂存区也会丢失掉，工作空间的代码什么的是不变的。
- 如果使用`--hard`，那么一切就全都恢复了，头变，aad的暂存区消失，代码什么的也恢复到以前状态。

1.回滚到指定历史版本

先使用git log查看历史版本

```bash
git log
```

在使用git reset --hard命令回滚

```bash
git reset --hard 要回滚id
```

示列：使用git log回滚

第一行的commit后面的字符串就是我们的哈希id

![img](git.assets/20201229124822787.png)

2.回滚当前仓库指向的版本

上面我们说过，HEAD是指向当前仓库的，历史版本中可能有别的分支，我们只想迭代我们仓库的上一个版本，这个很简单，我们只需要用HEAD来指向就可以了

```bash
git reset --hard HEAD^
```

^代表上一个版本的意思，HEAD代表当前仓库的指向，当前HEAD指向master，就代表回滚到master上一次提交的版本

当然我们也可以使用另外一种方式来回滚到当前仓库的指定版本

```bash
git reset --hard HEAD~3
```

后面的~3，代表以当前版本为基数，回滚多少次。HEAD~3代表回滚master前三个版本

如果觉得log打印内容过多，可以加上--pretty=oneline选项简洁输出

![img](git.assets/20210101003411898.png)

## 查看提交之后文件是否做了改动：git [status](https://so.csdn.net/so/search?q=status&spm=1001.2101.3001.7020)

> status：查看当前仓库状态

我们在提交完成之后，有时候可能自己不小心改动了某个文件，或者别人，我们可以使用git status查看文件是否被改动

![img](git.assets/20201229125744948.png)

可以看到报出了修改，这里我的环境语言是中文，英文对应：

A：未修改

AM：修改

Untracked：未提交

modified：新文件，但未提交

如果提交了的文件，且没有改动的，不会显示到这个里面

## 工作区与缓存区

在git下有一个概念是缓存区，这是其它集中式版本控制系统没有的

工作区：工作区就是你当前的工作目录

缓存区：这里存放了你使用git add命令提交的文件描述信息，它位于.git目录下的index文件中

![img](git.assets/20201229130440998.png)

有的低版本中叫stage

这些文件中存储了我们一些提交的缓存数据，git会解析它们，HEAD文件就是指向当前的仓库

最后使用git commit提交时git会提交到当前仓库中，当前的工作区也就成为了最新一次提交的仓库版本。

## 修改缓存区内容：git add、git commit -m

比如我们使用git add添加了一个名为min.c的文件，但是还没有提交的时候我们修改了它的内容，修改完成之后在提交会发现内容并不是我们第二次修改的内容

这就要说一点，当我们使用git add添加到缓存区的内容后，我们在修改这个文件时，它跟缓冲区内容是没有任何关系的！我们使用git commit提交的时，它只会提交缓存区内容

如果想提交第二次修改，我们只需要在git add一次，然后在使用git commit提交就可以了，git会自动帮我们合并提交

示列：

1.将文件添加到缓存区中

```bash
git add min.c
```

2.修改文件内容

```bash
vim min.c



xxxx



:wq
```

3.在此添加到缓存区

```bash
git add min.c
```

4.提交

```bash
git commit -m "add min.c"
```

## 将改动文件添加到缓存区：git add

平时我们可能写代码的时候不可能保证只改动了一个文件，我们切来切去最后都不知道自己改了哪些文件，为了保证所有的文件都能被准确提交，我们可以使用git add我们确定修改的文件，当git add后在使用status查看一下状态，看看是否有遗漏没有提交的文件：

```bash
git add min.c 
```

在使用git status查看是否有没有添加的：

![img](git.assets/20201229131825962.png)

可以看到test.c没有提交，在使用git add将test.c添加进来就可以了

## 将所有改动文件添加到缓存区：git add --all、git add .

如果你实在不确信哪些文件是改动过的，你只需要使用git add --all

```bash
git add --all
```

这个命令会将当前目录下包括子目录下所有改动的文件提交到暂存区，注意只包括改动的文件，不改动的不会放到缓存区。

这个命令还会把删除的文件也提交进去

如你在本地删除了min.c 这个命令会把删除信息也记录进去，然后在提交的时候把仓库里对应的min.c也删除掉，也就是说你在本地做的删除操作会被记录，提交仓库时会删除同样的文件，如果不想删除文件，可以使用git add .，注意后面有一个“.”点的符号，这个命令跟git add --all一样，但是不会记录删除操作。

最后别忘记使用git commit提交到仓库中

## 将文件撤销回到最近一次修改的状态：git checkout -- file

> checkout：切换参数，通常用来切换分支仓库

当我们在工作中修改了一个文件，猛然间发现内容好像改的不对，想重新修改，这个时又不知道自己改了什么代码，想撤销修改，有一个最简单的方法，就是git checkout -- file，注意中间要有“--”，checkout这个命令是切换分支的功能，关于它我们后面在细说，你现在只需要知道这个命令加上“--”可以用来将文件切换到最近一次的状态

注意这个恢复只能恢复到上一次提交的状态，如你刚提交了这个文件到仓库，随后你修改了它，那么使用这个命令只会回到刚刚提交后的那个状态里，不能回到你还没有提交，但修改的状态中。

下面这个演示，我将min.c文件修改了，并使用git checkout -- file回到了之前修改的状态

![img](git.assets/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L2JqYnpfY3h5,size_16,color_FFFFFF,t_70-1684119810154-8.png)

注意这个功能不能一直迭代恢复，如你恢复到了修改前的版本，你想再次回滚回滚到修改前在之前的版本是不行的。

## 查看单个文件可回滚版本：git log filename

当我们想回滚指定文件到指定版本时，需要查看该文件有多少个版本可以回滚时，可以使用git log filename命令

```bash
git log test.c
```

![img](git.assets/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L2JqYnpfY3h5,size_16,color_FFFFFF,t_70-1684119810154-9.png)

```bash
git log min.c
```

![img](git.assets/20201229143532632.png)

可以看到min.c文件可回滚版本较少，因为它是后来添加进来的。

在使用git reset命令将其回滚就可用了，命令格式如下：

```bash
git reset 1a1e91bf37add6c3914ebf20428efc0a7cea33f3 min.c
```

回退完成之后想要再次提交可以使用git add和git commit提交到本地仓库中，即可更新当前工作环境，让当前文件保持最新。

```bash
git add min.c



git commit -m "new"
```

更新完成后可以在使用log查看一下，会发现多出一个历史版本

![img](git.assets/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L2JqYnpfY3h5,size_16,color_FFFFFF,t_70-1684119810154-10.png)

即便你更新了一个文件，也会生成一个新的历史版本，注意历史版本里只包含了你更新的文件，你刚刚只add了min.c文件，所以新的历史版本里只有更新min.c文件，你当前的工作其它文件没有在这个历史版本里。

## 删除文件：git rm

如果我们使用普通的命令，rm删除文件，git状态会提示你删除了文件，你只需要使用add重新提交一次就可以了。

![img](git.assets/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L2JqYnpfY3h5,size_16,color_FFFFFF,t_70-1684119810154-11.png)

当然你也可以使用git rm删除文件，但是也需要使用git commit提交一次

![img](git.assets/20210101011026931.png)

可以看下status的状态

![img](git.assets/20210101011057428.png)

## 查看提交历史：git reflog

git reflog可以查看当前版本库的提交历史，凡是对仓库版本进行迭代的都会出现在这个里面，包括你回滚版本都会出现在这个历史中

![img](git.assets/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L2JqYnpfY3h5,size_16,color_FFFFFF,t_70-1684119810155-12.png)

## git基本组成框架：Workspace、Index / Stage、Repository、Remote

> - Workspace：开发者工作区
> - Index / Stage：暂存区/缓存区
> - Repository：仓库区（或本地仓库）
> - Remote：远程仓库

Workspace：开发者工作区，也就是你当前写代码的目录，它一般保持的是最新仓库代码。

Index / Stage：缓存区，最早叫Stage，现在新版本已经改成index，位于.git目录中，它用来存放临时动作，比如我们做了git add或者git rm，都是把文件提交到缓存区，这是可以撤销的，然后在通过git commit将缓存区的内容提交到本地仓库

Repository：仓库区，是仓库代码，你所有的提交都在这里，git会保存好每一个历史版本，存放在仓库区，它可以是服务端的也可以是本地的，因为在分布式中，任何人都可以是主仓库。

Remote：远程仓库，只能是别的电脑上的仓库，即服务器仓库。

## git rm后恢复文件：git rm、git reset、git checkout

此方法仅限git rm，因为git rm会先将文件放入缓存区,且没有使用commit提交的情况下

首先使用git rm删除一个文件

```bash
git rm d.c
```

在使用git reset重置所有缓存区操作

```cobol
git reset
```

重置完成之后在使用git checkout命令将文件取消操作

```bash
git checkout d.c
```

![img](git.assets/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L2JqYnpfY3h5,size_16,color_FFFFFF,t_70-1684119810155-13.png)

可以看到文件又恢复了

如果已经提交了想恢复怎么办？

这里给一个方法，就是把当前目录全部提交一次，这样做是为了防止我们等下回滚的时候导致一些修改的文件被替换掉了，然后我们回滚到有那个文件的版本，将那个文件copy到别的文件目录，这个文件目录要是你记得的，然后在回滚到最新版本代码，在将那个文件copy回来，在提交进去。

## git创建分支：git branch、git checkout

使用git checkout -b参数来创建一个分支，创建完成分支后会自动切换过去

```bash
git checkout -b dev
```

然后我们在使用branch来查看当前属于哪个分支，也就是查看HEAD的指向

```bash
git branch
```

![img](git.assets/20210101123559753.png)

git checkout -b等价于

```cobol
git branch dev



git checkout dev
```

git branch 如果后面跟着名字则会创建分支，但不会切换

git checkout 后面如果是分支名称则切换过去

## git切换分支：git checkout

当我们想切换分支可以使用git checkout来切换，如刚刚我们创建了一个分支dev并切换了过去，现在切换回masterk

```bash
git checkout master
```

![img](git.assets/20210101124051184.png)

git checkout的作用是检出，如果是文件的话，会放弃对文件的缓存区操作，但是要使用reset重置一下变更才行。

如果是分支的话会切换过去。

## git合并分支：git merge

当我们新建分支并做完工作之后，想要把分支提交至master，只需要切换到master仓库，并执行git merge 分支名就可以了

如我们在分支中新建了一个f.c和test.c的文件

然后在使用git checkout master切换到master

在使用git merge dev将其合并

![img](git.assets/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L2JqYnpfY3h5,size_16,color_FFFFFF,t_70-1684119810155-14.png)

这里需要说一点，如果你在任何分支下创建文件，没有提交到仓库，那么它在所有仓库都是可见的，比如你在分支dev中创建了一个文件，没有使用git add和git commit提交，此时你切换到master，这个文件依旧存在的，因为你创建的文件在工作目录中，你切换仓库时git只会更新跟仓库有关的文件，无关的文件依然存放在工作区。

同时我们可以看到历史版本中有分支提交的历史

![img](git.assets/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L2JqYnpfY3h5,size_16,color_FFFFFF,t_70-1684119810155-15.png)

## git查看分支：git branch -a

如果要查看当前所有分支可以使用：git branch -a

HEAD指向当前分支

```bash
* master



  remotes/origin/HEAD -> origin/master



  remotes/origin/master
```

## git删除本地分支：git branch -D

git branch -D 分支名

## git删除远程分支：git push origin --delete

注意这里的远程分支名不需要加origin，输入分支名就可以了

git push origin --delete 远程分支名

## 在开发中git分支的重要性

当我们在开发中，无论做什么操作都建议使用分支，因为在团队开发中，master只有一个，合作开发里任何人都可以从master里拉取代码，拉取时master后创建分支，分支名改为你要做的操作，比如修改某某文件，修改什么什么bug，单词以下划线做分割，然后在提交一个版本

分支名必须简洁，和标题一样，提交的commit在简单描述一下就可以了。

如我们的master中有个bug，是内存泄漏

我们可以常见一个分支名为Memory_Leak,然后在commit里简单描述一下修复了哪个模块的内存泄漏，不要写修复了什么什么代码，什么什么问题导致的，只需要简单描述一下就可以了。

一般情况下，我们都是拉取master后，想要修改功能或者添加功能，都是创建分支，在分支里修改不影响master，如果修改错了代码或者误删之类的，在从master上拉取一份就可以了。

## github的使用

github是一款使用git命令作为基础框架的网站，它是一款开源分享网站，你开源把你的源代码放到github上，然后让人来start给你小星星，小星星越多代表你的项目越具有影响力，很多公司面试如果你有一个很多星星的项目，会大大提升你的录取率。

你也可以把你的一些项目分享到github上保存，github上是无限制代码的。

1.首先到github上注册一个你的账号

2.在本地创建一个ssh的key，因为github是使用ssh服务进行通讯的

> ```html
> ssh-keygen -t rsa -C "your_email@example.com"
> ```

-t 指定密钥类型，默认是 rsa ，可以省略。
-C 设置注释文字，比如邮箱。
-f 指定密钥文件存储文件名，一般我们默认，让存储到默认路径以及默认文件名

它会要求输入Enter file in which to save the key (/home/stephenzhou/.ssh/id_rsa)

这里是生成的sshkey文件名，我们可以回车使用默认文件名

除此之外还会让你输入

Created directory '/home/stephenzhou/.ssh'.
Enter passphrase (empty for no passphrase): 
这个密码会在让你push提交时候要输入的，除了git登录密码，还要输入这个密码，直接回车则空密码，这里我们直接回车

接着会让你在此输入密码，验证这里依旧回车

Enter same passphrase again：

生成之后你就会看到这样的界面:

![img](git.assets/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L2JqYnpfY3h5,size_16,color_FFFFFF,t_70-1684119810155-16.png)

生成的ssh文件如果不使用-f指定的话会生成在用户目录下的.ssh目录中，.ssh是隐藏文件，可以使用ls -ah看到，使用cd ~进入用户主目录，然后cd进入到.ssh目录中可以看到文件

![img](git.assets/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L2JqYnpfY3h5,size_16,color_FFFFFF,t_70-1684119810155-17.png)

id_rsa是私匙，id_rsa.pub是公匙，id_rsa不能告诉任何人，只有公钥可以，ssh采用的是非对称加密。

接着在github上添加你的公钥

![img](git.assets/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L2JqYnpfY3h5,size_16,color_FFFFFF,t_70-1684119810155-18.png)



![img](git.assets/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L2JqYnpfY3h5,size_16,color_FFFFFF,t_70-1684119810155-19.png)

最后在输入你的登录密码就可以了

![img](git.assets/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L2JqYnpfY3h5,size_16,color_FFFFFF,t_70-1684119810155-20.png)

这样ssh就添加成功了~

![img](git.assets/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L2JqYnpfY3h5,size_16,color_FFFFFF,t_70-1684119810155-21.png)

你可以添加如很多个ssh，比如你有多台电脑，在每个电脑上都配置ssh然后添加进来就可以了，git需要这个是要确定你是主人，确定是主人的机器推送的才可以推送到仓库中，但是你可以创建公开仓库，别人只能拉取不能推送到这个仓库中，你可以给其它人权限。

找到你要开放的仓库，选择Manage access然后使用invite a cikkaborator添加成员就可以了。

![在这里插入图片描述](git.assets/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzQwMzA2MjY2,size_16,color_FFFFFF,t_70.png)

## github上创建仓库

我们可以在github上创建一个仓库

![img](git.assets/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L2JqYnpfY3h5,size_16,color_FFFFFF,t_70-1684119810155-22.png)

创建时记得选上readme文件，因为这个文件是github上的md文件，用来显示项目简介的，建议选上，日后我会教大家如何去写md文件，或者可以去使用一些在线的md文件生成网站也可以。

![img](git.assets/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L2JqYnpfY3h5,size_16,color_FFFFFF,t_70-1684119810155-23.png)

创建完成之后就是这个样子的

![img](git.assets/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L2JqYnpfY3h5,size_16,color_FFFFFF,t_70-1684119810155-24.png)

什么也没有，只有一个readme文件

## github将本地仓库关联到远程仓库：git remote add origin

我们本地有一个仓库，我们想把它推送到远程上去，很简单，我们只需要使用git remote add origin命令就可以了，ongin是github上的仓库名称，意思是远程仓库的意思。

首先选择仓库的code找到github生成的远程仓库链接

![img](git.assets/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L2JqYnpfY3h5,size_16,color_FFFFFF,t_70-1684119810155-25.png)

然后关联

```bash
git remote add origin git@github.com:beiszhihao/test.git
```

然后使用git push推送到远程

```bash
git push -u origin master
```

![img](git.assets/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L2JqYnpfY3h5,size_16,color_FFFFFF,t_70-1684119810155-26.png)

这里我来解释一下

> push：将本地仓库与远程仓库合并
>
> -u：将本地仓库分支与远程仓库分支一起合并，就是说将master的分支也提交上去，这样你就可以在远程仓库上看到你在本地仓库的master中创建了多少分支，不加这个参数只将当前的master与远程的合并，没有分支的历史记录，也不能切换分支
>
> origin：远程仓库的意思，如果这个仓库是远程的那么必须使用这个选项
>
> master：提交本地matser分支仓库

注意第一次提交ssh会让你验证是否来自github

The authenticity of host 'github.com (13.229.188.59)' can't be established.
RSA key fingerprint is SHA256:nThbg6kXUpJWGl7E1IGOCspRomTxdCARLviKw6E5SY8.
Are you sure you want to continue connecting (yes/no/[fingerprint])? yes
Warning: Permanently added 'github.com,13.229.188.59' (RSA) to the list of known hosts.
这里输入yes就可以了

我们不需要登录，因为github上的ssh列表里有这台机器

注意第一次的时候加上-u就可以了，因为我们本地其它可能有很多分支也提交上去，以后只提交最新代码就可以了git push origin master，不需要在提交其它分支

![img](git.assets/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L2JqYnpfY3h5,size_16,color_FFFFFF,t_70-1684119810155-27.png)

这个时候你可以在github上看到有提交记录

![img](git.assets/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L2JqYnpfY3h5,size_16,color_FFFFFF,t_70-1684119810155-28.png)

但是什么都没有，因为这个分支是main，我们提交的是master

选中它然后切换到master

![img](git.assets/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L2JqYnpfY3h5,size_16,color_FFFFFF,t_70-1684119810155-29.png)

默认是没有master的，这是我们新添加的分支

![img](git.assets/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L2JqYnpfY3h5,size_16,color_FFFFFF,t_70-1684119810155-30.png)

看到有文件了。

github上已经默认是main作为主仓库了，这个原因是因为种族运动的原因，master也代表主人，类似奴隶制，所以github已经替换默认master为main

## git将远程仓库关联到本地和拉取指定分支、切换远程分支：git clone

当我们远程有仓库时，想要关联到本地只需要使用git clone就可以了

新建一个空目录，不要git init

使用git clone会自动帮我们初始化

![img](git.assets/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L2JqYnpfY3h5,size_16,color_FFFFFF,t_70-1684119810156-31.png)

鉴于刚刚的，我们上传的代码在远程仓库中有一个默认的main和master，由于我们最初上传的分支是master，所以github给我们创建了一个新的分支叫master，并没有关联到mian中，我们拉取时，默认拉取的是main分支

所以我们可以使用git clone -b分支名 仓库地址来指定分支

![img](git.assets/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L2JqYnpfY3h5,size_16,color_FFFFFF,t_70-1684119810156-32.png)

## github提交本地仓库到远程仓库：git add、git commit、git push

我们修改了master上的分支代码，然后使用git add提交到缓存区，在使用commit提交到本地仓库，在使用push推送到远程就可以了，非常简单，命令都是我们学过的

![img](git.assets/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L2JqYnpfY3h5,size_16,color_FFFFFF,t_70-1684119810156-33.png)

## git修改分支名称：git branch

使用-m选项

git branch -m 分支名 新的分支名

## git保存当前工作切换分支：git stash

在你当前工作区修改了文件或者其它功能时，你想要切换或者创建到其它分区是不可能的，如：

![img](git.assets/20210101170120107.png)

我们分支修改了内容，想要切换到其它分区git会终止你这样操作，为的是防止丢失当前工作区内容。

我们可以使用git stash命令来保存当前工作状态

```bash
git stash
```

保存工作状态之后可以使用git stash list查看当前存储了多少工作状态

```bash
git stash list
```

那么此时我们就可以切换到其它分支了

![img](git.assets/20210101170528706.png)

当在别的分支做完事情之后，在切换回刚刚的分支，然后在刚刚的分支中将状态恢复

```bash
git stash pop
```

![img](git.assets/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L2JqYnpfY3h5,size_16,color_FFFFFF,t_70-1684119810156-34.png)

一般情况下，我们在修改代码时，突然来了一个新的需求，让我们先去做这个需求，但是此时我们正在写的代码还没有完成，是不可以提交的，所以我们先使用git stash保存当前工作状态，在拉取一个分支去这个分支里面干活，干完活之后回到之前的分支，在将工作内容恢复出来继续干活

git stash pop会将list保存的列表也给删除掉

git stash apply 不会删除列表里的内容会默认恢复第一个

如果想恢复指定内容可以使用git stash apply list名称

git stash drop list名称可以移除指定list

git stash clear 移除所有lsit

git stash show 查看栈中最新保存的stash和当前目录的差异。

注意stash是以栈的方式保存的，先进后出。

准确来说，这个命令的作用就是为了解决git不提交代码不能切换分支的问题。

## 将别的分支修改转移到自己的分支：git cherry-pick

有的时候我们从别的仓库拉取分支下来，是有bug的分支，但是master修复了，我们分支仓库没有修复，但是我们难不成重复master操作去修改这个bug？不不太繁琐了，我们直接使用cherry-pick命令将改动copy到我们分支上就可以了，这个命令只会将master改动代码合并到我们分支上，不会修改我们的代码。

git会检查master做了哪些修改，然后同步到我们的分支上，此时我们的分支依然是我们自己的代码，且会生成一个版本仓库。

做这个操作之前建议提交一次，便于恢复。

使用git cherry-pick 分支名即可合并分支修改，再次之前要保证你仓库代码是提交的，才可以进行这个步骤。

其次你可以使用git log查看commit 然后使用git cherry-pick也是可以的，合并分支的指定历史版本

## git远程删除分支后本地git branch -a依然看得到的问题：git remote 

这个问题是因为本地没有更新分支缓存

可以使用remote命令对远程仓库进行操作

使用 `git remote show origin命令查看远程仓库信息`

```bash
 git remote show origin
```

![img](git.assets/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L2JqYnpfY3h5,size_16,color_FFFFFF,t_70-1684119810156-35.png)

如果在里面没有看到删除后的分支就代表这个分支在远程已经被删除了。

使用prune参数刷新本地分支仓库

```bash
 git remote prune origin
```

## git强制合并分支：--allow-unrelated-histories

当我们在使用两个不同的分支时或此分支不是从原生仓库中分支出来的，想要合并不符合GIT规则，所以会弹出：fatal: refusing to merge unrelated histories 的错误，比如当我们在本地开发好了，但是并没有在一开始关联远程仓库，若想提交就会出现这样的错误，我们先拉取下来以后合并分支在后面加上这条语句就可以了

```cpp
git merge master --allow-unrelated-histories
```

![img](git.assets/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L2JqYnpfY3h5,size_16,color_FFFFFF,t_70-1684119810156-36.png)

## git拉取远程所有分支：git fetch

当我们在本地进行开发时，有时会发现有些分支看不见

![img](git.assets/20210625150943249.png)

可以使用git fetch把远程全部分支拉取下来，同时也包括这些分支的仓库版本，log日志等，这个操作不会进行合并。

```bash
git fetch
```

拉取后结果如下：

![img](git.assets/20210625151100522.png)

也可以拉取指定分支的最新内容：

```bash
git fetch xxxx
```

## git子模块管理：git submodule

在当我们项目较大的情况下，都会使用模块化编程，把不同的业务功能分割成数个子模块，git也拥有对子模块进行管理的方法，submodule，可以使用它来添加子模块与管理子模块。

如添加一个子模块：

```bash
git submodule add  http://192.168.1.88:7990/scm/wlibold/weye_lib.git
```

使用如上命令会添加一个子模块，名为weye_lib的子模块到自己的仓库中，这样我们就可以使用了

在添加时会添加仓库的最新版本，但是此模块不会自动更新，需要我们手动更新，当子模块的仓库进行了更新，我们需要进到此子模块的文件夹中执行如下命令：

```bash
git submodule update
```

这样就会自动化更新了模块到最新版本。

若我们想要使用指定版本的子模块也可以使用切换版本命令来完成子模块的版本切换，同时你也可以使用git log命令查看这个子模块的版本提交。

注意根据git版本不同的原因，你在添加时可能下来的子模块是空项目，这个时候可以使用如下命令：

首先进入到克隆下来的子模块目录，并执行如下命令：

```bash
git submodule init



git submodule update
```

最新的git在使用add添加子模块时会自动使用这两个命令。

这两个命令作用分别是初始化子模块仓库，更新远程子模块仓库到本地，最早的git添加子模块只是先在本地生成了映射关系，需要手动执行这两个命令。

最后别忘记使用git add与git commit提交一次。

在提醒一下，若你使用的子模块版本是0.17，最新版本是2.13，当别人拉取你仓库时子模块也会是0.17不会变动。

## git分支开发步骤

一般情况下我们开发都要在不扰乱master代码的情况下进行开发

1.拉取分支，分支名简明摘要说要干什么，然后干活，在合并到master，合并之后在删除分支，这是基本步骤，不需要留额外分支，分支只是为了将来看代码时方便而已，能看到这个分支是干什么的。

## git强制删除分支：git branch 

如果遇到无法删除的分支可以使用git branch -D 大写的D即可。

## git查看不同分支的文件差异：git diff

![img](git.assets/20210101213745449.png)

## git查看仓库信息：git remote

使用git remote可以查看当前仓库名称

```bash
git remote
```

使用remote -v可以查看更详细的权限信息

![img](git.assets/20210101214252440.png)

fetch代表可以拉取仓库，push代表可以推送。

如果没有权限只能拉取的情况下不会显示push。

git查看日志简洁方法：git log

```lua
git log --graph --pretty=oneline --abbrev-commit
```

![img](git.assets/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L2JqYnpfY3h5,size_16,color_FFFFFF,t_70-1684119810156-37.png)

注意前面的字符串是有效的，你可以用它来切换版本或者合并分支。

## Git新增分支操作：git switch、git restore

这两个命令是git 2.23以后引入的命令，目的是为了提供对新手更友好的分支操作，最早我们使用的是git checkout命令来对分支进行操作，这个命令相对于复杂了许多，使用很多子参数来进行操作，为此git新增了两个命令：switch、restore，switch是用来切换分支与新增分支的，而restore用来撤销文件的修改，使其变得更明确一点

切换分支：

```bash
git switch dev
```

注意如果分支不存在，是不会创建的

切换到commit ID：

切换到指定id并创建一个分支，我们称之为分离HEAD状态

```bash
git switch -d f8c540805b7e16753c65619ca3d7514178353f39
```

只需要加上-d参数就可以了，而checkout是不需要加-d的，在switch里一切变得明确了很多

如果要合并一个分支必须加上-b

```bash
git switch -b dev
```

创建分支则是-c

```bash
git switch -c dev
```

git restore命令是用来撤销提交与修改的，如：

```bash
git restore file
```

使用这条命令会将文件从暂存区删除

```bash
git restore file
```

这条命令会不会将文件从暂存区里删除，会将文件在暂存区里的状态覆盖到工作区，如我在工作区对这个文件又进行了修改，那么使用这个命令可以将这个文件在暂存区里的内容恢复到工作区

## 搭建本地git服务器

第一步在debian/linux下使用此命令安装完整git

```bash
sudo apt install git
```

安装完成之后我们可以新建一个用户用来做专门管理git服务的账户

```bash
git adduser git
```

这样，就创建了一个账户名为git组也为git的账户

我们切换到这个用户下

```bash
su git
```

然后使用

```bash
ssh-keygen -t rsa -C "你的邮箱"
```

配置好当前服务器的sshkey ，配置好之后会在用户目录下生成一个.ssh目录

然后在".ssh"目录里面查看有没有authorized_keys文件，没有则创建一个

```bash
touch authorized_keys
```

这个文件是用来存放别人的公钥的，就像上面配置github一样，你把别人机器上的ssh key的公钥输入到这个文件中，这样git才会开启权限免密登录，让其拥有推送以及拉取的权限。

好了你现在是这台git服务器的管理者了。

那么你现在想要创建一个仓库，并分享给团队。

假如你们要做一个文本编辑器，你可以使用git init --bare创建一个名为txt的文件目录。

注意要用git init，这里我们以.git为结尾，通常git仓库都是这样命名。

```csharp
sudo git init --bare txt.git
```

很遗憾它报了个错

![img](git.assets/20210101225626716.png)

这是因为我们新建的用户没有sudo权限，我们执行如下命令

```bash
vim /etc/sudoers
```

然后添加一行内容进去

```bash
git  ALL=(ALL:ALL) ALL
```

这样我们就可以执行sudo权限了，如果提示没有权限，则切回到可以执行sudo的用户中，执行上面的操作，在切回git。

![img](git.assets/20210101225811169.png)

我们在改变一下文件所属用户与组，让这个文件属于当前用户与组

```bash
 sudo chown -R git:git txt.git
```

为了安全考虑我们需要禁用ssh登录到我们的shell，防止别人登录到shell之后对我们的电脑做增删改

输入如下命令

```bash
vim /etc/passwd
```

找到这一行

```bash
git:x:1001:1001:,,,:/home/git:/bin/bash
```

改为：

```bash
git:x:1001:1001:,,,:/home/git:/usr/bin/git-shell
```



我们将默认ssh登录改为到git-shell程序中，这个git提供的shell程序，一旦登录会自动秒退。

好了现在可以让你的小伙伴们来克隆txt.git这个仓库了。

![img](git.assets/20210101232304323.png)

注意，你的服务器需要安装ssh服务

```bash
sudo apt install openssh-server
```

在git用户下执行上面这个命令，因为每个环境都不一样。

不然的话可能出现如下状况，ssh无法解析主机名：

![img](git.assets/20210101232734912.png)

## Git问题总汇

### [error: src refspec main does not match any](https://jrhar.blog.csdn.net/article/details/113931821)

### [Please make sure you have the correct access rights and the repository exists.](https://jrhar.blog.csdn.net/article/details/113934922)

## git命令总结

> ## 创造
>
> 克隆现有存储库
>
> $ git clone ssh://user@domain.com/repo.git
>
> 创建一个新的本地存储库
>
> $ git init
>
> ## 当地变化
>
> Changed files in your working directory
>
> $ git status
>
> Changes to tracked files
>
> $ git diff
>
> 将所有当前更改添加到下一个提交
>
> $ git add .
>
> 在中添加一些更改到下一次提交
>
> $ git add -p
>
> 提交跟踪文件中的所有本地更改
>
> $ git commit -a
>
> 提交先前进行的更改
>
> $ git commit
>
> 更改最后一次提交
>
> 不要修改已发布的提交！
>
> $ git commit --amend
>
> ## 提交历史
>
> 显示所有提交，从最新开始
>
> $ git log
>
> 显示特定文件随时间的变化e
>
> $ git log -p
>
> 谁更改了中的内容和时间
>
> $ git blame
>
> ## 分支机构和标签
>
> 列出所有现有分支
>
> $ git branch -av
>
> 切换HEAD分支
>
> $ git checkout
>
> 根据您当前的HEAD创建一个新分支
>
> $ git branch
>
> 基于远程分支创建一个新的跟踪分支
>
> $ git checkout --track
>
> 删除本地分支
>
> $ git branch -d
>
> 用标签标记当前提交
>
> $ git tag
>
> ## 更新和发布
>
> 列出所有当前配置的遥控器
>
> $ git remote -v
>
> 显示有关遥控器的信息
>
> $ git remote show
>
> 添加名为的新远程存储库
>
> $ git remote add
>
> 从下载所有更改，但不要集成到HEAD中
>
> $ git fetch
>
> 下载更改并直接合并/集成到HEAD中
>
> $ git pull
>
> 在远程上发布本地更改
>
> $ git push
>
> 删除遥控器上的分支
>
> $ git branch -dr
>
> 发布标签
>
> $ git push --tags
>
> ## 合并与基础
>
> 将合并到当前HEAD中
>
> $ git merge
>
> 将当前的HEAD重新设置到
>
> 不要重新发布已发布的提交！
>
> $ git rebase
>
> 中止基准
>
> $ git rebase --abort
>
> 解决冲突后继续进行基准
>
> $ git rebase --continue
>
> 使用您配置的合并工具解决冲突
>
> $ git mergetool
>
> 使用编辑器手动解决冲突，并（在解决之后）将文件标记为已解决
>
> $ git add
>
> $ git rm
>
> ## 撤消
>
> 丢弃工作目录中的所有本地更改
>
> $ git reset --hard HEAD
>
> 放弃特定文件中的本地更改
>
> $ git checkout HEAD
>
> 还原提交（通过产生具有相反更改的新提交）
>
> $ git revert
>
> 将HEAD指针重置为上一次提交
>
> …并丢弃此后的所有更改
>
> $ git reset --hard
>
> …并将所有更改保留为未分阶段的更改
>
> $ git reset
>
> …并保留未提交的本地更改
>
> $ git reset --keep