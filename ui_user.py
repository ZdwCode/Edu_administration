"""用户管理模块"""
import data
import wx
class UserWindow(wx.Dialog):
    def __init__(self,parent,title):
        wx.Frame.__init__(self,parent,title,size=(800,600));

        panel=wx.Panel(self,wx.ID_ANY);

        #创建控件
        lblListAction=['插入','修改','删除'];
        self.rboxAction=wx.RadioBox(panel,label='操作',choices=lblListAction)
        lblListType=['学生','教师','教务'];
        self.rboxUsertype=wx.RadioBox(panel,label='角色',choices=lblListType)

        self.listUser=wx.ListCtrl(panel,wx.ID_ANY,size=(400,400),style=wx.LC_REPORT);
        self.listUser.InsertColumn(0,'用户id',width=50);
        self.listUser.InsertColumn(1, '姓名', width=50);
        self.listUser.InsertColumn(2, '性别', width=50);
        self.listUser.InsertColumn(3, '院系', width=50);
        self.listUser.InsertColumn(4, '电话号码', width=100);
        self.listUser.InsertColumn(5, '出生年月', width=100);

        labelUserId=wx.StaticText(panel,wx.ID_ANY,'用户id')
        self.inputTextUserId=wx.TextCtrl(panel,wx.ID_ANY,'')
        labelUserName = wx.StaticText(panel, wx.ID_ANY, '用户名')
        self.inputTextUserName = wx.TextCtrl(panel, wx.ID_ANY,'')
        labelBirthday = wx.StaticText(panel, wx.ID_ANY, '出生年月')
        self.inputBirthday = wx.TextCtrl(panel, wx.ID_ANY,'')
        labelDepartment = wx.StaticText(panel, wx.ID_ANY, '所属院系')
        self.inputTextDepartment = wx.TextCtrl(panel, wx.ID_ANY, '')
        labelPhone = wx.StaticText(panel, wx.ID_ANY, '电话号码')
        self.inputTextPhone = wx.TextCtrl(panel, wx.ID_ANY, '');
        labelPassword = wx.StaticText(panel, wx.ID_ANY, '密码')
        self.inputTextPassword = wx.TextCtrl(panel, wx.ID_ANY, '')
        lblListGender=['男','女'];
        self.rboxGender=wx.RadioBox(panel,label='性别',choices=lblListGender);

        #按钮
        self.insertBtn=wx.Button(panel,wx.ID_ANY,'插入')
        self.updateBtn = wx.Button(panel, wx.ID_ANY, '更新');
        self.updateBtn.Disable();
        self.deleteBtn = wx.Button(panel, wx.ID_ANY, '删除')
        self.deleteBtn.Disable();
        exitBtn=wx.Button(panel,wx.ID_ANY,'退出');

        #添加布局
        topSizer=wx.BoxSizer(wx.VERTICAL);
        optionSizer=wx.BoxSizer(wx.HORIZONTAL);
        contentSizer=wx.BoxSizer(wx.HORIZONTAL);
        listSizer=wx.BoxSizer(wx.HORIZONTAL);
        editSizer=wx.BoxSizer(wx.VERTICAL)
        useridSizer = wx.BoxSizer(wx.HORIZONTAL);
        usernameSizer = wx.BoxSizer(wx.HORIZONTAL);
        birthdaySizer = wx.BoxSizer(wx.HORIZONTAL);
        departmentSizer = wx.BoxSizer(wx.HORIZONTAL);
        phoneSizer = wx.BoxSizer(wx.HORIZONTAL);
        passwordSizer=wx.BoxSizer(wx.HORIZONTAL);
        genderSizer = wx.BoxSizer(wx.HORIZONTAL);
        btnSizer=wx.BoxSizer(wx.HORIZONTAL);

        optionSizer.Add(self.rboxAction,0,wx.ALL,5);
        optionSizer.Add(self.rboxUsertype,0,wx.ALL,5);

        listSizer.Add(self.listUser,0,wx.ALL,5);

        useridSizer.Add(labelUserId,0, wx.ALL,5)
        useridSizer.Add(self.inputTextUserId, 0,wx.ALL,5)
        usernameSizer.Add(labelUserName,0,wx.ALL,5);
        usernameSizer.Add(self.inputTextUserName,0,wx.ALL,5);
        birthdaySizer.Add(labelBirthday, 0, wx.ALL, 5);
        birthdaySizer.Add(self.inputBirthday, 0, wx.ALL, 5);
        departmentSizer.Add(labelDepartment, 0, wx.ALL, 5);
        departmentSizer.Add(self.inputTextDepartment, 0, wx.ALL, 5);
        phoneSizer.Add(labelPhone,0,wx.ALL,5);
        phoneSizer.Add(self.inputTextPhone,0,wx.ALL,5);
        passwordSizer.Add(labelPassword,0,wx.ALL,5);
        passwordSizer.Add(self.inputTextPassword,0,wx.ALL,5);
        genderSizer.Add(self.rboxGender,0,wx.ALL,5);
        btnSizer.Add(self.insertBtn,0,wx.ALL,5);
        btnSizer.Add(self.updateBtn, 0, wx.ALL, 5);
        btnSizer.Add(self.deleteBtn, 0, wx.ALL, 5);
        btnSizer.Add(exitBtn, 0, wx.ALL, 5);

        editSizer.Add(useridSizer,0,wx.ALL,5);#嵌套填入
        editSizer.Add(usernameSizer, 0, wx.ALL, 5);
        editSizer.Add(birthdaySizer, 0, wx.ALL, 5);
        editSizer.Add(departmentSizer, 0, wx.ALL, 5);
        editSizer.Add(phoneSizer, 0, wx.ALL, 5);
        editSizer.Add(passwordSizer, 0, wx.ALL, 5);
        editSizer.Add(genderSizer, 0, wx.ALL, 5);
        editSizer.Add(btnSizer, 0, wx.ALL, 5);


        contentSizer.Add(listSizer,0,wx.ALL,5);
        contentSizer.Add(editSizer, 0, wx.ALL, 5);

        topSizer.Add(optionSizer,0,wx.ALL|wx.Centre,5);
        topSizer.Add(contentSizer,0,wx.ALL|wx.Centre,5);

        panel.SetSizer(topSizer);
        topSizer.Fit(self)

        #绑定事件
        self.Bind(wx.EVT_RADIOBOX,self.onAction,self.rboxAction);
        self.Bind(wx.EVT_RADIOBOX, self.onUserType, self.rboxUsertype);
        self.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.onUserList, self.listUser);
        self.Bind(wx.EVT_BUTTON, self.onInsert, self.insertBtn);
        self.Bind(wx.EVT_BUTTON, self.onUpdate, self.updateBtn);
        self.Bind(wx.EVT_BUTTON, self.onDelete, self.deleteBtn);
        self.Bind(wx.EVT_BUTTON, self.onExit, exitBtn);

        #查询信息并显示在userlist中
        self.populate_user_list();
    def populate_user_list(self):
        user_type=self.rboxUsertype.GetStringSelection();#获取
        user_list=data.get_user_list(user_type);
        self.listUser.DeleteAllItems();
        index =0;
        for user in user_list:
            self.listUser.InsertItem(index,user[0]);
            self.listUser.SetItem(index,1,user[1]);
            self.listUser.SetItem(index, 2, user[2]);
            self.listUser.SetItem(index, 3, user[3]);
            self.listUser.SetItem(index, 4, user[4]);
            self.listUser.SetItem(index, 5, user[5]);
            index+1;
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
    def onUserType(self,e):
        self.populate_user_list();
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

    def refresh_screen(self):
        """刷新界面"""
        self.inputTextUserId.SetValue('');
        self.inputTextUserName.SetValue('');
        self.inputBirthday.SetValue('');
        self.inputTextDepartment.SetValue('');
        self.inputTextPhone.SetValue('');
        self.inputTextPassword.SetValue('');
        self.rboxGender.SetSelection(0);

        #初始化界面
        self.populate_user_list();

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
    def onDelete(self,e):
        userid = self.inputTextUserId.GetValue();
        #删除一条记录
        data.delete_userbyid(userid);
        self.refresh_screen();
    def onExit(self,e):
        self.Close();


if __name__=="__main__":
    app=wx.App()
    frame=UserWindow(parent=None,title=2);
    frame.Show();
    app.MainLoop();


