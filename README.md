# Edu_administration
这是一个简单的基于mysql和wxpython的教务管理系统
## 一、数据库表的设计
1.创建名为jwxt的数据库 create database jwxt charset='utf8';

2.创建用户管理表--userinfo

 CREATE TABLE `userinfo` (
  `userId` varchar(20) NOT NULL,
  `userName` varchar(20) NOT NULL,
  `gender` enum('男','女') DEFAULT NULL,
  `birthday` varchar(11) DEFAULT NULL,
  `department` varchar(20) DEFAULT NULL,
  `phone` varchar(11) DEFAULT NULL,
  `usertype` varchar(2) DEFAULT NULL,
  `password` varchar(20) NOT NULL,
  PRIMARY KEY (`userId`)
)

3.创建课程管理表--course

 CREATE TABLE `course` (
  `courseId` varchar(20) NOT NULL,
  `courseName` varchar(20) NOT NULL,
  `credit` int(11) DEFAULT NULL,
  `description` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`courseId`)
)

4. 创建教学班信息表--class

 CREATE TABLE `class` (
  `classId` varchar(20) NOT NULL,
  `courseId` varchar(20) NOT NULL,
  `userId` varchar(20) NOT NULL,
  `description` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`classId`)
)

5.创建学生成绩表--grades

此表可用来实现学生与课程之间多对多的关系

CREATE TABLE `grades` (
  `classId` varchar(20) NOT NULL DEFAULT '',
  `userid` varchar(20) NOT NULL DEFAULT '',
  `score` int(11) DEFAULT NULL,
  PRIMARY KEY (`classId`,`userid`)
)

## 二、用户管理界面

界面设计如下:
