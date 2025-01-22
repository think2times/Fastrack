# 01_大数据导论与Linux基础
## 00-Hadoop导学
> 这个视频主要讲了 Hadoop 的核心组件，包括 HDFS, MapReduce, Hive。起步薪资很高，基本在12k以上，从业5年即可达到30k以上。

## 01-课程内容大纲与学习目标
> 为什么要学Linux：因为大数据的工具都在Linux系统运行

> Linux要学到什么程度：掌握基本的文件操作

> 学习目标：了解大数据基本概念，知道数据分析的步骤，掌握基本的Linux操作命令和简单的vi操作

## 02-数据分析与企业数据分析方向
> 数据是什么？数据如何产生？

> 企业进行数据分析的方向：现状分析，原因分析和未来预测，正好对应数据分析的三个方向：实时分析，离线分析/批处理，机器学习

## 03-数据分析的基本步骤
- 明确分析目的和思路
- 数据收集
- 数据处理
- 数据分析
- 数据展示
- 报告撰写

## 04-大数据时代
> 大数据是什么？5V特征是什么？大数据的应用？

> 大量数据如何存储？如何计算？

## 05-分布式与集群
> 分布式与集群是不同的概念：它们的共同点是都有多台机器实现，但是分布式的每台机器部署不同的组件，而集群中的每台机器都部署相同的组件

> 大数据可以通过分布式来解决存储和计算方面的难题

## 06-Linux操作系统概述
> Linux的起源和比较流行的发行版有哪些

## 11-Linux文件系统基础知识
> 在Linux中，万物皆文件，所以一切操作都可以认为是对文件的操作。

> 当前目录、相对路径和绝对路径的区别

## 12-Linux常用操作命令（1）-ls、cd、mkdir、rm
- ls: list files
    - ls -a
    - ll = ls -l
- cd: change directory
    - 不加参数时，会回到用户的家目录
- touch: 创建一个空文件
- mkdir: make directory
    - mkdir target_parents/target_dir -p: -p参数保证了父目录不存在时自动创建

## 13-Linux常用操作命令（2）-mv、cp、cat、tail、管道、重定向
- cp: copy file
    - cp source_dir/ target_dir/ -r: -r参数可以复制整个目录
- cat: concatenate
- more: 以页的形式显示文件内容，按enter可以看下面一行，空格看下一页，b可以回到上一页
- tail: 查看文件末尾部分的内容，默认显示10行
    - tail -n target_file: 显示最后n行的内容，注意-n参数必须在tail和文件名之间，不能放在最后
    - tail -f target_file: 实时显示动态追加到文件中的内容。只要文件有更新，该命令会不断输出最新的更新内容。-f的位置也可以放到最后
- echo: 将内容输出到console控制台上
- |: 管道操作，把前一个命令的结果作为输入传给后一个命令
- 输出重定向命令
    - command > target_file: 执行command，然后将执行结果存入target_file中，target_file中的内容会被新内容覆盖
    - command >> target_file: 执行command，然后将执行结果存入target_file中，新内容会追加到target_file文件末尾

## 14-Linux常用操作命令（3）-tar命令解压缩包
- 打包、解包
    - -c或--create: 建立新的备份文件
    - -x或--extract或--get: 从备份文件中还原文件
    - -v或--verbose: 显示指令执行过程
    - -f <备份文件> 或 --file=<备份文件> 指定备份文件
- 压缩
    - -z或--gzip或--ungzip 通过gzip压缩或解压备份文件

## 15-Linux常用系统命令--时间日期、内存磁盘使用率、进程查看
- 日期、日历
    - date: 查看当天的日期
    - cal(calendar): 查看当前的公历
- 内存、磁盘使用率
    - free: 显示内存状态，可以加上-h使显示的内容可读性更高
    - df(disk free): 显示磁盘使用情况，重点关注根目录/对应的磁盘信息，也可以用-h来提高可读性
- 进程查看
    - ps(process status): 显示当前的进程状态，ps -ef可以查看本机运行的所有进程
    - kill -进程号: 可以根据进程号结束对应的进程

## 16-vim编辑器介绍、3种工作模式
- vi作为Linux内置的文本编辑器，有三种工作模式：
    - 命令模式：使用vi命令默认进入命令模式，不能编辑文本，但是可以进行复制、粘贴、删除等操作
    - 编辑模式：可以按 i, a, o 今日编辑模式，对文件内容进行插入、修改、删除等操作，可以通过按esc进入命令模式
    - 底部命令模式：以 : 开始，主要用于文件的保存退出等

## 17-vim基本操作命令
- 移动光标
    - h: 光标向左移动一格
    - l: 光标向右移动一格
    - j: 光标向下移动一格
    - k: 光标向上移动一格
    - 0: 光标移动到行首
    - $: 光标移动到行尾
    - gg: 光标移动到文件开头
    - G: 光标移动到文件末尾
- 复制粘贴
    - yy: 复制光标所在行
    - nyy: 复制当前行往下n行
    - p: 把复制的内容粘贴到当前行的下一行
    - P: 把复制的内容粘贴到当前行的上一行
- 删除、撤销
    - dd: 删除光标所在行
    - ndd: 删除当前行往下n行
    - u: 撤销上一步的操作
    - ctrl+r: 反撤销

# 02_Apache Hadoop、HDFS
## 01-课程内容大纲-学习目标

## 02-Apache Hadoop介绍、发展简史、现状
> hadoop之父：Doug Cutting，起源于Nutch项目，受到谷歌3篇论文的启发，主要由HDFS分布式文件管理系统、YARN资源和任务管理调度平台和MapReduce计算框架组成，目前HDFS和YARN仍然使用广泛，而MapReduce由于设计上的缺陷，逐渐退居二线

## 03-Apache Hadoop特性优点、国内外应用
> 优点：扩展性强、成本低、效率高、可靠性强

## 04-Apache Hadoop发行版本、架构变迁
> 开源社区版：优点是官方出品，更新快，缺点是不稳定，兼容性不足; 商业版：优点是稳定，缺点是收费，更新不及时

## 05-Apache Hadoop安装部署--集群组成介绍
> Hadoop集群 = HDFS集群 + YARN集群; 这两个集群在逻辑上隔离，在物理上却可能部署在一起。另外没有MapReduce集群，它是一个计算框架

## 06-Apache Hadoop安装部署--服务器基础环境设置
> 配置Linux服务器环境，安装jdk并添加到环境变量

## 07-Apache Hadoop安装部署--安装包结构
> 上传hadoop安装包，了解安装包结构

## 08-Apache Hadoop安装部署--修改配置文件、同步安装包与环境变量
> 配置文件路径: hadoop安装目录/etc/hadoop

- hadoop-env.sh: 配置java环境变量，配置hdfs和yarn节点的默认用户为root
- xxxx-site.xml: 表示用户自定义的配置，会覆盖default中的默认配置
    - core-site.xml: 核心模块
    - hdfs-site.xml: hdfs文件系统模块
    - mapred-site.xml: MapReduce模块配置
    - yarn-site.xml: YARN模块配置
- workers

## 09-Apache Hadoop安装部署--format初始化操作
> 注意初始化命令多次执行会删除之前的数据

## 10-Apache Hadoop安装部署--集群启停命令、Web UI页面
> 启动的时候可能会遇到namenode或datanode无法启动的情况，解决方法是停止所有服务，把logs，tmp/dfs/data，tmp/dfs/name目录下所有文件都删除，然后重新启动hadoop服务

> hdfs网页端：http://namenode服务器所在ip:9870/

> YARN网页端：http://resourcemanager服务器所在ip:8088/

## 11-Apache Hadoop安装部署--初体验
> 用hadoop自带的jar包执行计算pi和单词统计，发现完成这样简单的任务的速度并不快，而且每次都要先连接YARN集群中的ResourceManager，再计算的时候是先进行Map运算，然后再进行Reduce运算，面对小数据量的任务hadoop不仅没有优势，反而会有劣势

## 12-传统文件系统在大数据时代面临的挑战
> 成本高，无法支撑高效率的计算分析，性能低，可扩展性差

## 13-场景互动：分布式存储系统的核心属性及功能作用
- 分布式存储：无限扩展，支持海量数据存储
- 元数据记录：快速定位文件位置，便于查找
- 分块存储：可针对块进行并行操作，提高效率
- 副本备份：冗余存储，保证数据安全
