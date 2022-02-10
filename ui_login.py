import wx;
import data;
import ui_main;
class LoginWindow(wx.Dialog):
    def __init__(self,parent,title):
        wx.Dialog.__init__(self,parent,title=title,size=(800,600));
        panel=wx.Panel(self,wx.ID_ANY);

        # 创建控件
        labelUserId=wx.StaticText(panel,wx.ID_ANY,'用户id');
        self.inputTextUserID=wx.TextCtrl(panel,wx.ID_ANY,'');
        labelPassword=wx.StaticText(panel,wx.ID_ANY,'密码')
        self.inputTextPassword=wx.TextCtrl(panel,wx.ID_ANY,'');

        lblList=['教务','教师','学生'];
        self.rboxUserType=wx.RadioBox(panel,label='角色',choices=lblList);
        self.rboxUserType.SetSelection(2);#默认选择学生

        okBtn=wx.Button(panel,wx.ID_ANY,'登录');
        cancelBtn=wx.Button(panel,wx.ID_ANY,'取消');

        topSizer=wx.BoxSizer(wx.VERTICAL);
        userSizer=wx.BoxSizer(wx.HORIZONTAL);
        passwordSizer=wx.BoxSizer(wx.HORIZONTAL);
        userTypeSizer=wx.BoxSizer(wx.HORIZONTAL);
        btnSizer=wx.BoxSizer(wx.HORIZONTAL);

        userSizer.Add(labelUserId,0,wx.ALL,5);
        userSizer.Add(self.inputTextUserID,0,wx.ALL,5);
        passwordSizer.Add(labelPassword,0,wx.ALL,5);
        passwordSizer.Add(self.inputTextPassword, 0, wx.ALL, 5);
        userTypeSizer.Add(self.rboxUserType);
        btnSizer.Add(okBtn,0, wx.ALL, 5);
        btnSizer.Add(cancelBtn, 0, wx.ALL, 5);

        topSizer.Add(userSizer,0,wx.ALL|wx.Centre,5);
        topSizer.Add(passwordSizer, 0, wx.ALL | wx.Centre, 5);
        topSizer.Add(userTypeSizer, 0, wx.ALL | wx.Centre, 5);
        topSizer.Add(btnSizer, 0, wx.ALL | wx.Centre, 5);

        panel.SetSizer(topSizer);
        topSizer.Fit(self);

        #绑定事件
        self.Bind(wx.EVT_BUTTON,self.onOk,okBtn);
        self.Bind(wx.EVT_BUTTON, self.onCancel,cancelBtn)


    def onOk(self,e):
        """登录确认"""
        userid=self.inputTextUserID.GetValue();
        password=self.inputTextPassword.GetValue();
        usertype=self.rboxUserType.GetStringSelection();

        if len(userid.strip())==0:
            wx.MessageBox("请输入用户id");
            self.inputTextUserID.SetFocus();
            return 0;

        if len(password.strip())==0:
            wx.MessageBox("请输入密码");
            self.inputTextPassword.SetFocus();
            return 0;

        username=data.check_login(userid,password,usertype);

        if not username:
            """用户不存在"""
            wx.MessageBox("用户不正确，请重新输入");
            self.inputTextUserID.SetFocus();
        else:
            """成功登录"""
            self.Close();#关闭该窗口进入 主界面
            title='教务管理系统'
            mainFrame=ui_main.MainWindow(None,title,userid,username,usertype);
            mainFrame.Show();
            mainFrame.Center();
    def onCancel(self,e):
        self.Close();
