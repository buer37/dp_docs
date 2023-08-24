### GIT配置

#### 查看当前用户（global）配置

```
git config --global  --list
```

#### 设置提交的用户名和邮箱：

```
git config --global user.name "用户名"
git config --global user.email "邮箱"
```

### 分支

#### 新建

```
git checkout -b 新分支名
```

#### 切换

```
git checkout 分支名
```

#### 推送新的分支到远程仓库

```
git push --set-upstream origin 分支名
```



### 提交分支代码思路

查看改动文件，将需要提交的文件提交到本地缓存区，将不需要提交的文件移除，最后将本地缓存区的文件提交到仓库更新到git上. ：

#### 查看本次修改的文件

```
 git status
```

#### 添加文件 

- 将所有的文件提交到本地缓存区

```
git add --all
```

- 将指定的文件提交到本地缓存区

```
 git add 文件夹名/文件名
```

#### 将某个文件从缓存区移除出来

- 撤销全部

```
git reset HEAD -- .
```

- 指定文件

```
git reset HEAD -- filename
```

#### 将本地缓存区的文件提交到本地仓库

```
git commit [-a] -m "msg"
```

| 参数 | 解释                                                         |
| ---- | ------------------------------------------------------------ |
| -a   | 参数表示，可以将所有已跟踪文件中的执行修改或删除操作的文件都提交到本地仓库，即使它们没有经过 git add 添加到暂存区。 |

追加提交，它可以在不增加一个新的 commitId 的情况下将新修改的追加到前一次的 commitId中。

```
git commit --amend
```

#### 撤销commit

```
git reset [--soft | --mixed | --hard] [HEAD]
```

| 参数  | 解释                                                         |
| ----- | ------------------------------------------------------------ |
| mixed | 不删除工作空间改动代码，撤销commit，并且撤销**git add**操作  |
| soft  | 不删除工作空间改动代码，撤销**commit**，不撤销**git add**    |
| hard  | <font color="red">**删除**</font>工作空间改动代码，撤销**commit**，撤销**git add **,注意完成这个操作后，就恢复到了上一次的commit状态。 |

HEAD^的意思是上一个版本，也可以写成HEAD~1

如果你进行了2次commit，想都撤回，可以使用HEAD^^/HEAD~2

#### 将本地仓库的文件更新到git

```
git push origin 已提交的分支名
```

### 合并分支思路

​	先去更新要被合并分支的代码，再合并到当前分支. ：

1. 先把当前分支提交：git commit -am "提交描述"
2. 切换到需要被合并的分支：git checkout 要被合并的分支名
3. 更新需要被合并的分支：git pull 要被合并的分支名
4. 切换到当前分支：git checkout 当前分支名
5. 在当前分支合并需要被合并的分支：git rebase 要被合并的分支名

1. 合并代码冲突，回到解决冲突前的状态：

   ```
   git rebase --abort
   ```

2. 强制提交建议用于代码没有被其他人修改的情况下使用，能正常提交就不用这个. ：

   ```
   git push --force origin 提交的分支名
   ```

### 使用git filter-branch 批量修改commit

> 另一种方法是使用 Git 的“filter-branch”命令。它允许您使用脚本**批处理**（可能很大）数量的提交。
>
> 您可以在存储库中运行以下示例脚本（为新旧电子邮件和名称填写实际值）：

#### 修改

   ```bash
   $ git filter-branch --env-filter '
   WRONG_NAME="wrong name"
   WRONG_EMAIL="wrong@example.com"
   NEW_NAME="New Name"
   NEW_EMAIL="correct@example.com"
   if [ "$GIT_COMMITTER_EMAIL" = "$WRONG_EMAIL" ]
   then
       export GIT_COMMITTER_NAME="$NEW_NAME"
       export GIT_COMMITTER_EMAIL="$NEW_EMAIL"
   fi
   if [ "$GIT_AUTHOR_EMAIL" = "$WRONG_EMAIL" ]
   then
       export GIT_AUTHOR_NAME="$NEW_NAME"
       export GIT_AUTHOR_EMAIL="$NEW_EMAIL"
   fi
   if [ "$GIT_COMMITTER_NAME" = "$WRONG_NAME" ]
   then
       export GIT_COMMITTER_NAME="$NEW_NAME"
       export GIT_COMMITTER_EMAIL="$NEW_EMAIL"
   fi
   if [ "$GIT_AUTHOR_NAME" = "$WRONG_NAME" ]
   then
       export GIT_AUTHOR_NAME="$NEW_NAME"
       export GIT_AUTHOR_EMAIL="$NEW_EMAIL"
   fi
   ' --tag-name-filter cat -- --branches --tags
   ```

#### push到仓库

- 与提到的其他方法一样，同样的警告适用于此方法：<font color=red>您正在使用此命令重写历史记录，并在此过程中创建新的提交对象！</font>

   ```bash
   git push --force
   ```

