#### Windows搭建redis集群
#####
复制出六个配置文件,引用一个通用配置文件
```
include D:\\redis\cluster\conf\redis.windows.conf

port 7001(7002|7003|7004|7005|7006)
dir D:\\redis\cluster\data\7001(7002|7003|7004|7005|7006)\
# 是否开启集群
cluster-enabled yes
# 集群配置文件（启动后自动生成）
cluster-config-file nodes-7001(7002|7003|7004|7005|7006).conf
# 集群节点ping、pong超时时间
cluster-node-timeout 5000
```
#####启动命令
```
.\redis5.0\redis-cli.exe  --cluster create 127.0.0.1:7001 127.0.0.1:7002 127.0.0.1:7003 127.0.0.1:7004 127.0.0.1:7005 127.0.0.1:7006 --cluster-replicas 1

```
https://blog.csdn.net/u013515384/article/details/114434521