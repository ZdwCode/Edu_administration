import wx;
import ui_login;
import ui_user;
import ui_course;
import ui_jxb;
import ui_student;

class MainWindow(wx.Frame):
    def __init__(self,parent,title,userid,username,usertype):
        wx.Frame.__init__(self,parent,title=title,size=(640,480));
        self.CreateStatusBar();#创建状态栏
        self.userid=userid;
        self.username=username;
        self.usertype=usertype;

        #创建菜单并添加菜单项
        sysmenu=wx.Menu();
        j_menu=wx.Menu();
        s_menu=wx.Menu();
        t_menu=wx.Menu();
        helpmenu=wx.Menu();

        menuLogin=sysmenu.Append(wx.ID_ANY,'重新登录','重新登录');
        menuChangePassword=sysmenu.Append(wx.ID_ANY,'修改密码','修改密码');
        menuExit=sysmenu.Append(wx.ID_EXIT,'退出系统','退出系统');
        menuUser=j_menu.Append(wx.ID_ANY,'用户管理','用户管理');
        menuCourse = j_menu.Append(wx.ID_ANY, '课程管理', '课程管理');
        menuJXB = j_menu.Append(wx.ID_ANY, '开课计划', '开课计划');
        menuStudent = s_menu.Append(wx.ID_ANY, '学生选课', '学生选课');
        menuTeacher = t_menu.Append(wx.ID_ANY, '成绩登录', '成绩登录');
        menuAbout=helpmenu.Append(wx.ID_ABOUT,'关于我们','关于');

        menuBar=wx.MenuBar();
        menuBar.Append(sysmenu,'系统');
        if self.usertype=='教务':
            menuBar.Append(j_menu,'教务')
        elif  self.usertype=='学生':
            menuBar.Append(s_menu,'学生');
        elif  self.usertype=='教师':
            menuBar.Append(t_menu,'教师');

        menuBar.Append(helpmenu,'帮助');
        self.SetMenuBar(menuBar)#加到顶层框架

        #绑定事件
        self.Bind(wx.EVT_MENU,self.onLogin,menuLogin);
        self.Bind(wx.EVT_MENU, self.onChangePassword, menuChangePassword);
        self.Bind(wx.EVT_MENU, self.onExit, menuExit);
        self.Bind(wx.EVT_MENU, self.onUser, menuUser);
        self.Bind(wx.EVT_MENU, self.onCourse, menuCourse);
        self.Bind(wx.EVT_MENU, self.onJXB, menuJXB);
        self.Bind(wx.EVT_MENU, self.onStudent, menuStudent);
        self.Bind(wx.EVT_MENU, self.onTeacher, menuTeacher);

        self.Bind(wx.EVT_MENU, self.onAbout, menuAbout);

    def onLogin(self,e):
        """重定向到ui_login"""
        self.Close(True);
        loginFrame=ui_login.LoginWindow(parent=None,title="重新登录");
        loginFrame.Show();
        loginFrame.Centre();

    def onChangePassword(self,e):
        wx.MessageBox("修改密码暂未开通")

    def onExit(self,e):
        self.Close();

    def onUser(self,e):
        userFrame=ui_user.UserWindow(parent=None,title='用户管理');
        userFrame.Show();
        userFrame.Centre();

    def onCourse(self,e):
        courseFrame=ui_course.CourseWindow(parent=None,title='课程管理')
        courseFrame.Show();
        courseFrame.Centre();
    def onJXB(self,e):
        """开课计划：教学班管理"""
        jxbFrame=ui_jxb.JXBWindow(parent=None,title='开课计划');
        jxbFrame.Show();
        jxbFrame.Centre();

    def onStudent(self,e):
        """事件处理 学生选课"""
        studentFrame=ui_student.StudentWindow(parent=None,title='学生选课',userid=self.userid);
        studentFrame.Show();
        studentFrame.Centre();

    def onTeacher(self,e):
        wx.MessageBox("暂未开通");

    def onAbout(self,e):
        pass;