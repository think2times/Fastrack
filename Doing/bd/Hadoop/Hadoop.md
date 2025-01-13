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