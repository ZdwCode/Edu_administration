import data;
import wx;
class JXBWindow(wx.Dialog):
    def __init__(self,parent,title):
        wx.Frame.__init__(self, parent, title=title, size=(800, 600));
        panel = wx.Panel(self, wx.ID_ANY);
        #创建控件
        lblListAction = ['插入', '修改', '删除'];
        self.rboxAction = wx.RadioBox(panel, label='操作', choices=lblListAction)

        self.listJXB=wx.ListCtrl(panel,wx.ID_ANY,size=(450,400),style=wx.LC_REPORT);
        self.listJXB.InsertColumn(0,'教学班号',width=50);
        self.listJXB.InsertColumn(1,'课程ID',width=50);
        self.listJXB.InsertColumn(2,'课程名称',width=100)
        self.listJXB.InsertColumn(3,'教师ID',width=50);
        self.listJXB.InsertColumn(4,'教师姓名',width=100);
        self.listJXB.InsertColumn(5,'时间地点',width=100);

        labelJxbId=wx.StaticText(panel,wx.ID_ANY,'教学班号')
        self.inputTextJxbId=wx.TextCtrl(panel,wx.ID_ANY,'')
        labelCourseId = wx.StaticText(panel, wx.ID_ANY, '课程id')
        self.inputTextCourseId = wx.TextCtrl(panel, wx.ID_ANY, '',style=wx.TE_PROCESS_ENTER)
        self.inputTextCourseName=wx.TextCtrl(panel,wx.ID_ANY,'');
        self.inputTextCourseName.Disable();
        labelTeacherId = wx.StaticText(panel, wx.ID_ANY, '教师id')
        self.inputTextTeacherId = wx.TextCtrl(panel, wx.ID_ANY, '', style=wx.TE_PROCESS_ENTER)
        self.inputTextTeacherName = wx.TextCtrl(panel, wx.ID_ANY, '');
        self.inputTextTeacherName.Disable();
        labelDescription=wx.StaticText(panel,wx.ID_ANY,'时间地点');
        self.inputTextDescription=wx.TextCtrl(panel,wx.ID_ANY,'');

        # 按钮
        self.insertBtn = wx.Button(panel, wx.ID_ANY, '插入')
        self.updateBtn = wx.Button(panel, wx.ID_ANY, '更新');
        self.updateBtn.Disable();
        self.deleteBtn = wx.Button(panel, wx.ID_ANY, '删除')
        self.deleteBtn.Disable();
        exitBtn = wx.Button(panel, wx.ID_ANY, '退出');

        #创建布局容器
        topSizer = wx.BoxSizer(wx.VERTICAL);
        optionSizer = wx.BoxSizer(wx.HORIZONTAL);
        contentSizer = wx.BoxSizer(wx.HORIZONTAL);
        listSizer = wx.BoxSizer(wx.HORIZONTAL);
        editSizer = wx.BoxSizer(wx.VERTICAL)
        jxbSizer=wx.BoxSizer(wx.HORIZONTAL);
        courseSizer = wx.BoxSizer(wx.HORIZONTAL);
        userSizer = wx.BoxSizer(wx.HORIZONTAL);
        descriptionSizer=wx.BoxSizer(wx.HORIZONTAL);
        btnSizer=wx.BoxSizer(wx.HORIZONTAL);

        #添加
        optionSizer.Add(self.rboxAction,0,wx.ALL,5);

        listSizer.Add(self.listJXB,0,wx.ALL,5);

        jxbSizer.Add(labelJxbId,0,wx.ALL,5);
        jxbSizer.Add(self.inputTextJxbId,0,wx.ALL,5);
        courseSizer.Add(labelCourseId,0,wx.ALL,5);
        courseSizer.Add(self.inputTextCourseId,0,wx.ALL,5);
        courseSizer.Add(self.inputTextCourseName,0,wx.ALL,5);
        userSizer.Add(labelTeacherId, 0, wx.ALL, 5);
        userSizer.Add(self.inputTextTeacherId, 0, wx.ALL, 5);
        userSizer.Add(self.inputTextTeacherName, 0, wx.ALL, 5);
        descriptionSizer.Add(labelDescription,0,wx.ALL,5);
        descriptionSizer.Add(self.inputTextDescription,0,wx.ALL,5);
        btnSizer.Add(self.insertBtn,0,wx.ALL,5)
        btnSizer.Add(self.updateBtn, 0, wx.ALL, 5)
        btnSizer.Add(self.deleteBtn, 0, wx.ALL, 5)
        btnSizer.Add(exitBtn, 0, wx.ALL, 5);

        editSizer.Add(jxbSizer,0,wx.ALL,5);
        editSizer.Add(courseSizer, 0, wx.ALL, 5);
        editSizer.Add(userSizer, 0, wx.ALL, 5);
        editSizer.Add(descriptionSizer, 0, wx.ALL, 5);
        editSizer.Add(btnSizer,0,wx.ALL,5);

        contentSizer.Add(listSizer,0,wx.ALL,5);
        contentSizer.Add(editSizer,0,wx.ALL,5);

        topSizer.Add(optionSizer, 0, wx.ALL | wx.Centre, 5)
        topSizer.Add(contentSizer,0,wx.ALL|wx.Centre,5)

        panel.SetSizer(topSizer);
        topSizer.Fit(self)

        #绑定事件
        self.Bind(wx.EVT_RADIOBOX,self.onAction,self.rboxAction);
        self.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.onJXBList, self.listJXB);
        self.Bind(wx.EVT_TEXT_ENTER, self.onCourseId, self.inputTextCourseId);
        self.Bind(wx.EVT_TEXT_ENTER, self.onTeacherId, self.inputTextTeacherId);
        self.Bind(wx.EVT_BUTTON, self.onInsert, self.insertBtn);
        self.Bind(wx.EVT_BUTTON, self.onUpdate, self.updateBtn);
        self.Bind(wx.EVT_BUTTON, self.onDelete, self.deleteBtn);
        self.Bind(wx.EVT_BUTTON, self.onExit, exitBtn);

        self.populate_JXB_list();
    def populate_JXB_list(self):
        """查询开课信息jxb并显示"""
        jxb_list=data.get_jxb_list();
        self.listJXB.DeleteAllItems();
        index=0;
        for jxb in jxb_list:
            self.listJXB.InsertItem(index,jxb[0]);
            self.listJXB.SetItem(index,1,jxb[1]);
            self.listJXB.SetItem(index, 2, jxb[2]);
            self.listJXB.SetItem(index, 3, jxb[3]);
            self.listJXB.SetItem(index, 4, jxb[4]);
            if jxb[5]==None:
                self.listJXB.SetItem(index, 5, '');
            else:
                self.listJXB.SetItem(index, 5, jxb[5]);
            index+=1;
    def onAction(self,e):
        action = self.rboxAction.GetStringSelection();
        #print(action, e)
        if action == '插入':
            self.inputTextJxbId.Enable();
            self.insertBtn.Enable();
            self.updateBtn.Disable();
            self.deleteBtn.Disable();
        if action == '修改':  # 由于数据库是按id修改的 故要先确定id
            self.inputTextJxbId.Disable();
            self.insertBtn.Disable();
            self.updateBtn.Enable();
            self.deleteBtn.Disable();
        if action == '删除':
            self.inputTextJxbId.Disable();
            self.insertBtn.Disable();
            self.updateBtn.Disable();
            self.deleteBtn.Enable();
    def onJXBList(self,e):
        """选择一门课程信息并显示在右边"""
        index=e.GetIndex();
        self.inputTextJxbId.SetValue(self.listJXB.GetItem(index,0).GetText());
        self.inputTextCourseId.SetValue(self.listJXB.GetItem(index, 1).GetText());
        self.inputTextCourseName.SetValue(self.listJXB.GetItem(index, 2).GetText());
        self.inputTextTeacherId.SetValue(self.listJXB.GetItem(index, 3).GetText());
        self.inputTextTeacherName.SetValue(self.listJXB.GetItem(index, 4).GetText());
        self.inputTextDescription.SetValue(self.listJXB.GetItem(index, 5).GetText())
    def onCourseId(self,e):
        """输入课程id时检查其存在 并显示名称"""
        courseid=self.inputTextCourseId.GetValue();
        if len(courseid.strip())==0:
            wx.MessageBox("请输入课程id")
            return 0;
        coursename=data.check_course_id(courseid);
        if coursename:
            self.inputTextCourseName.SetValue(coursename);
        else:
            wx.MessageBox("该课程不存在！");
            self.inputTextCourseId.SetFocus();
            return 0;

    def onTeacherId(self,e):
        teacherid = self.inputTextTeacherId.GetValue();
        if len(teacherid.strip()) == 0:
            wx.MessageBox("请输入教师id")
            return 0;
        teachername = data.check_user_id(teacherid);
        if teachername:
            self.inputTextTeacherName.SetValue(teachername);
        else:
            wx.MessageBox("该教师不存在！");
            self.inputTextTeacherId.SetFocus();
            return 0;
    def onInsert(self,e):
        """插入一条数据"""
        jxbid=self.inputTextJxbId.GetValue();
        courseid=self.inputTextCourseId.GetValue();
        teacherid=self.inputTextTeacherId.GetValue();
        description=self.inputTextDescription.GetValue();

        #输入检查
        if len(jxbid.strip())==0:
            wx.MessageBox("请输入教学班号");
            self.inputTextJxbId.SetFocus();
            return 0;
        if len(courseid.strip())==0:
            wx.MessageBox("请输入课程号");
            self.inputTextCourseId.SetFocus();
            return 0;
        if len(teacherid.strip())==0:
            wx.MessageBox("请输入教师id");
            self.inputTextTeacherId.SetFocus();
            return 0;
        if data.check_jwb_id(jxbid):
            wx.MessageBox("教学班号已存在，请重新输入");
            self.inputTextJxbId.SetFocus();
            return 0;
        if not data.check_course_id(courseid):
            wx.MessageBox("课程号不存在，请重新输入");
            self.inputTextCourseId.SetFocus();
            return 0;
        if not data.check_user_id(teacherid):
            wx.MessageBox("该教师不存在，请重新输入");
            self.inputTextTeacherId.SetFocus();
            return 0;
        #满足数据约束 插入
        data.insert_jxb(classid=jxbid,courseid=courseid,userid=teacherid,description=description);

        #初始化界面
        self.refresh_screen();
    def refresh_screen(self):
        self.inputTextJxbId.SetValue('');
        self.inputTextCourseId.SetValue('');
        self.inputTextCourseName.SetValue('');
        self.inputTextTeacherId.SetValue('');
        self.inputTextTeacherName.SetValue('');
        self.inputTextDescription.SetValue('');

        self.populate_JXB_list();
    def onUpdate(self,e):
        """修改数据"""
        jxbid = self.inputTextJxbId.GetValue();
        courseid = self.inputTextCourseId.GetValue();
        teacherid = self.inputTextTeacherId.GetValue();
        description = self.inputTextDescription.GetValue();

        if len(courseid.strip())==0:
            wx.MessageBox("请输入课程号");
            self.inputTextCourseId.SetFocus();
            return 0;
        if len(teacherid.strip())==0:
            wx.MessageBox("请输入教师id");
            self.inputTextTeacherId.SetFocus();
            return 0;

        if not data.check_course_id(courseid):
            wx.MessageBox("课程号不存在，请重新输入");
            self.inputTextCourseId.SetFocus();
            return 0;
        if not data.check_user_id(teacherid):
            wx.MessageBox("该教师不存在，请重新输入");
            self.inputTextTeacherId.SetFocus();
            return 0;
        data.update_jxb(classid=jxbid,courseid=courseid,
                        userid=teacherid,description=description);

        self.refresh_screen();
    def onDelete(self,e):
        """删除一条数据"""
        jxbid = self.inputTextJxbId.GetValue();

        #删除记录
        data.delete_jxb(jxbid);
        #初始化界面
        self.refresh_screen();

    def onExit(self,e):
        self.Close();

if __name__=="__main__":
    app=wx.App()
    frame=JXBWindow(parent=None,title="开课计划");
    frame.Show();
    app.MainLoop();