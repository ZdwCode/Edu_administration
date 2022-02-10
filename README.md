# Edu_administration
这是一个简单的基于mysql和wxpython的教务管理系统

教务管理系统的主模块是main.py，用于创建和显示登录界面(ui_login.py)。登录后显示主菜单界面(ui_main.py），并根据登录用户的类型（权限），显示不同的操作菜单。

(1）所有用户都可以使用“系统”和“帮助”菜单。包括“重新登录”(ui_login. py，重新登录）、“修改密码”(ui_change_password.py，修改密码)、“退出系统”。

(2）教务员角色可以使用“教务”菜单，包括“用户管理”(ui_user.py，管理用户信息）、“课程管理”(ui_course.py，管理课程信息）、“开课计划”(ui_jxb.py，管理开课计划，即教学班)。

(3)学生角色可以使用“学生”菜单，包括“学生选课”(ui_student.py，查看、选课或退选课程）。

(4)教师角色可以使用“教师”菜单，包括“成绩登录”(ui_teacher.py，查看所教授的教学班信息和登录学生成绩)。

部分功能操作演示如下



https://user-images.githubusercontent.com/68136166/153416590-108d9610-5991-47e5-af44-690ba531e37e.mp4


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
## 二、数据模块API

连接数据库 并创建需要的表如下 详细操作间具体代码
```
def get_connect(*args,**kwargs):
    # 获得连接
    con = pymysql.connect(host=kwargs.get('host'),
                          port=kwargs.get('port'),
                          user=kwargs.get('user'),
                          password=kwargs.get('password'),
                          charset='utf8')
    #获取游标
    cursor = con.cursor();

    #判断数据库是否存在：
    sql_show_databases="show databases";
    cursor.execute(sql_show_databases);
    databases=cursor.fetchall();
    databases_name = kwargs.get('databases_name');
    for i in range(len(databases)):
        if databases_name == databases[i][0]:
            print("数据库已经创建了");
            sql_use_jwxt='use jwxt';
            cursor.execute(sql_use_jwxt);
            cursor.close()
            return con;

    print("数据库没有创建 可以开始创建了")
    #创建数据库
    sql_create_jwtx="create database jwxt charset='utf8';";
    cursor.execute(sql_create_jwtx);
    print("jwxt已经创建好了");
    #使用数据库
    sql_use_jwxt = 'use jwxt';
    cursor.execute(sql_use_jwxt);
    #创建数据表
    create_sqlTable(con,cursor);
    cursor.close();
    return con;

def create_sqlTable(con,cursor):
    sql_create_UserInfo="create table userinfo( userId varchar(20) primary key," \
                        "userName varchar(20) not null," \
                        "gender enum('男','女'),birthday varchar(11)," \
                        "department varchar(20)," \
                        "phone varchar(11)," \
                        "usertype varchar(2)," \
                        "password varchar(20) not null);"
    cursor.execute(sql_create_UserInfo);
    print("用户表创建完毕")

    #插入一条数据 作为管理员
    sql_insert_UserInfo="insert into userinfo values('j001','章登炜','男'," \
                        "'1999/10/28','计算机系','18179219692','教务','123456');"
    cursor.execute(sql_insert_UserInfo);
    con.commit();
    print("初始管理员数据已插入");

    #创建课程表信息
    sql_create_COURSE="create table course(" \
                      "courseId varchar(20) primary key," \
                      "courseName varchar(20) not null," \
                      "credit int ," \
                      "description varchar(100)" \
                      ");"
    cursor.execute(sql_create_COURSE);

    #创建教学班号表 暂时不设计外键
    sql_create_class = "create table class(" \
                        "classId varchar(20) primary key," \
                        "courseId varchar(20) not null," \
                        "userId varchar(20) not null," \
                        "description varchar(100)" \
                        ");"
    cursor.execute(sql_create_class);

    #创建学生成绩表
    sql_create_grade="create table grades(" \
                        "classId varchar(20)," \
                        "userid varchar(20) ," \
                        "score int," \
                     "primary key(classid,userid));"
    cursor.execute(sql_create_grade);
```

## 三、用户管理界面如下
![用户管理界面.png](https://upload-images.jianshu.io/upload_images/18963630-28f489b233b7ca52.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
用户管理界面布局采用BoxSizer布局，具体参见源代码

(1）初始化时，调用self.populate_user_list()函数，进而调用data.get_user_list(user_type)，显示指定“角色”的所有用户列表。
```
 def populate_user_list(self):
        user_type=self.rboxUsertype.GetStringSelection();#获取
        user_list=data.get_user_list(user_type);
        self.listUser.DeleteAllItems();
        index =0;
        for user in user_list:
            self.listUser.InsertItem(index,user[0]);
            for i in range(1,len(user+1)):
                self.listUser.SetItem(index,i,user[i]);
            index+1;
```
(2）切换选择“角色”类型时，在事件处理函数中调用self.populate_user_list()函数，重新查询显示用户列表。

(3）选择“操作”类型时，在事件处理函数中，根据操作类型(插入、更新、删除）设置不同控件的状态

    def onAction(self,e):
        action=self.rboxAction.GetStringSelection();
        print(action,e)
        if action =='插入':
            self.rboxUsertype.Enable();
            self.inputTextUserId.Enable();
            self.insertBtn.Enable();
            self.updateBtn.Enable();
            self.deleteBtn.Enable();
        if action =='修改':#由于数据库是按id修改的 故要先确定id
            self.inputTextPassword.Disable();
            self.rboxUsertype.Disable();
            self.inputTextUserId.Disable();
            self.insertBtn.Disable();
            self.updateBtn.Enable();
            self.deleteBtn.Disable();
        if action =='删除':
            self.rboxUsertype.Disable();
            self.inputTextUserId.Disable();
            self.insertBtn.Disable();
            self.updateBtn.Disable();
            self.deleteBtn.Enable();

(4）双击左侧列表选择用户信息时，在事件处理函数中，显示该行信息到右侧对应的编辑框中。

    def onUserList(self,e):
        """在userList中选择用户 内容显示在右侧"""
        index=e.GetIndex();
        self.inputTextUserId.SetValue(self.listUser.GetItem(index,0).GetText())
        self.inputTextUserName.SetValue(self.listUser.GetItem(index, 1).GetText());
        if self.listUser.GetItem(index,2).GetText() == '男':
            n=0;
        else:n=1
        self.rboxGender.SetSelection(n);
        self.inputBirthday.SetValue(self.listUser.GetItem(index, 5).GetText());
        self.inputTextDepartment.SetValue(self.listUser.GetItem(index, 3).GetText());
        self.inputTextPhone.SetValue(self.listUser.GetItem(index, 4).GetText());

(5）单 击“插入”按钮，在事件处理函数中调用data.check_user_id(userid)，判断用户是否存在，如果存在，则报错;否则调用data.insert_user(user_type，userid,username，gender， birthday,department，phone)，插入一条记录到UserInfo表中。

    def onInsert(self,e):
        """插入一条记录"""
        user_type=self.rboxUsertype.GetStringSelection();
        userid=self.inputTextUserId.GetValue()
        username=self.inputTextUserName.GetValue();
        birthday=self.inputBirthday.GetValue();
        department=self.inputTextDepartment.GetValue();
        phone=self.inputTextPhone.GetValue();
        gender=self.rboxGender.GetStringSelection();
        password=self.inputTextPassword.GetValue();
        if len(userid.strip())==0:#去除两边空格
            wx.MessageBox("请输入用户ID");
            self.inputTextUserId.SetFocus();
            return 0;
        if len(username.strip())==0:
            wx.MessageBox("请输入用户名");
            self.inputTextUserName.SetFocus();
            return 0;
        if data.check_user_id(userid):
            print(data.check_user_id(userid))
            wx.MessageBox("用户id已存在，请重新输入");
            self.inputTextUserId.SetFocus();
            return 0;

        #输入没有问题 则条用data的insert_user插入
        data.insert_user(usertype=user_type,userid=userid,username=username,
                         gender=gender,birthday=birthday,department=department,
                         phone=phone,password=password)
        #刷新界面
        self.refresh_screen();

(6)单击“更新”按钮，在事件处理函数中调用data.update_user(userid,username， gender, birthday，, department,phone)，更新UserInfo表中的一条记录。

    def onUpdate(self,e):
        """更新一条数据"""
        userid = self.inputTextUserId.GetValue()
        username = self.inputTextUserName.GetValue();
        birthday = self.inputBirthday.GetValue();
        department = self.inputTextDepartment.GetValue();
        phone = self.inputTextPhone.GetValue();
        gender = self.rboxGender.GetStringSelection();
        if len(username.strip())==0:
            wx.MessageBox("请输入用户名");
            self.inputTextUserName.SetFocus();
            return 0;

        #更新记录
        data.update_user(userid=userid,username=username,
                         gender=gender,department=department,
                         phone=phone,birthday=birthday)
        self.refresh_screen();

(7）单击“删除”按钮，在事件处理函数中调用data.delete_user (userid)，从UserInfo表中的删除一条记录。

    def onDelete(self,e):
        userid = self.inputTextUserId.GetValue();
        #删除记录————是否应该考虑逻辑删除
        data.delete_userbyid(userid);
        self.refresh_screen();

(8）单击“退出”按钮，返回主界面。

课程管理，开课计划等模块与用户管理模块的实现方法大同小异，这里就不做赘述








