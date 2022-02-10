"""学生选课模块"""
import data;
import wx;
class StudentWindow(wx.Dialog):
    def __init__(self,parent,title,userid):
        wx.Frame.__init__(self,parent,title=title,size=(800,600));
        self.userid=userid;
        panel=wx.Panel(self,wx.ID_ANY);

        #创建控件
        lblListAction=['选课','退选'];
        self.rboxAction=wx.RadioBox(panel,label='操作',choices=lblListAction);

        self.listGrade=wx.ListCtrl(panel,wx.ID_ANY,size=(550,400),style=wx.LC_REPORT);
        self.listGrade.InsertColumn(0,'教学班号',width=80);
        self.listGrade.InsertColumn(1, '课程id', width=60);
        self.listGrade.InsertColumn(2, '课程名称', width=100);
        self.listGrade.InsertColumn(3, '教师id', width=50);
        self.listGrade.InsertColumn(4, '教师姓名', width=100);
        self.listGrade.InsertColumn(5, '时间地点', width=120);
        self.listGrade.InsertColumn(6, '成绩', width=60);

        labelJxbId=wx.StaticText(panel,wx.ID_ANY,'教学班号');
        #输入教学班信息就可以全部输入
        self.inputTextJxbId=wx.TextCtrl(panel,wx.ID_ANY,'',style=wx.TE_PROCESS_ENTER);
        labelCourseId=wx.StaticText(panel,wx.ID_ANY,'课程id');
        self.inputTextCourseId = wx.TextCtrl(panel, wx.ID_ANY, '');
        self.inputTextCourseId.Disable();
        self.inputTextCourseName = wx.TextCtrl(panel, wx.ID_ANY, '');
        self.inputTextCourseName.Disable();
        labelTeacherId = wx.StaticText(panel, wx.ID_ANY, '教师id');
        self.inputTextTeacherId = wx.TextCtrl(panel, wx.ID_ANY, '');
        self.inputTextTeacherId.Disable();
        self.inputTextTeacherName = wx.TextCtrl(panel, wx.ID_ANY, '');
        self.inputTextTeacherName.Disable();

        labelDescription = wx.StaticText(panel, wx.ID_ANY, '时间地点');
        self.inputTextDescription = wx.TextCtrl(panel, wx.ID_ANY, '');
        self.inputTextDescription.Disable();
        labelScore = wx.StaticText(panel, wx.ID_ANY, '学生成绩');
        self.inputTextScore = wx.TextCtrl(panel, wx.ID_ANY, '');
        self.inputTextScore.Disable();

        self.insertBtn=wx.Button(panel,wx.ID_ANY,'选课');
        self.deleteBtn = wx.Button(panel, wx.ID_ANY, '退选');
        self.deleteBtn.Disable();
        exitBtn=wx.Button(panel, wx.ID_ANY, '退出');

        # 添加布局
        topSizer = wx.BoxSizer(wx.VERTICAL);
        optionSizer = wx.BoxSizer(wx.HORIZONTAL);
        contentSizer = wx.BoxSizer(wx.HORIZONTAL);
        listSizer = wx.BoxSizer(wx.HORIZONTAL);
        editSizer = wx.BoxSizer(wx.VERTICAL);
        jxbSizer=wx.BoxSizer(wx.HORIZONTAL);
        courseSizer = wx.BoxSizer(wx.HORIZONTAL);
        userSizer = wx.BoxSizer(wx.HORIZONTAL);
        descriptionSizer = wx.BoxSizer(wx.HORIZONTAL);
        scoreSizer = wx.BoxSizer(wx.HORIZONTAL);
        btnSizer=wx.BoxSizer(wx.HORIZONTAL);

        optionSizer.Add(self.rboxAction,0,wx.ALL,5);
        listSizer.Add(self.listGrade, 0, wx.ALL, 5);

        jxbSizer.Add(labelJxbId,0,wx.ALL,5);
        jxbSizer.Add(self.inputTextJxbId, 0, wx.ALL, 5);
        courseSizer.Add(labelCourseId,0,wx.ALL,5);
        courseSizer.Add(self.inputTextCourseId,0,wx.ALL,5);
        courseSizer.Add(self.inputTextCourseName,0,wx.ALL,5);
        userSizer.Add(labelTeacherId,0,wx.ALL,5);
        userSizer.Add(self.inputTextTeacherId, 0, wx.ALL, 5);
        userSizer.Add(self.inputTextTeacherName,0,wx.ALL,5);
        descriptionSizer.Add(labelDescription,0,wx.ALL,5);
        descriptionSizer.Add(self.inputTextDescription, 0, wx.ALL, 5)
        scoreSizer.Add(labelScore,0,wx.ALL,5)
        scoreSizer.Add(self.inputTextScore,0, wx.ALL, 5);
        btnSizer.Add(self.insertBtn,0,wx.ALL,5);
        btnSizer.Add(self.deleteBtn, 0, wx.ALL, 5)
        btnSizer.Add(exitBtn, 0, wx.ALL, 5);

        editSizer.Add(jxbSizer,0,wx.ALL,5);
        editSizer.Add(courseSizer, 0, wx.ALL, 5);
        editSizer.Add(userSizer, 0, wx.ALL, 5);
        editSizer.Add(descriptionSizer, 0, wx.ALL, 5);
        editSizer.Add(scoreSizer, 0, wx.ALL, 5);
        editSizer.Add(btnSizer, 0, wx.ALL, 5);

        contentSizer.Add(listSizer,0, wx.ALL, 5);
        contentSizer.Add(editSizer, 0, wx.ALL, 5);

        topSizer.Add(optionSizer, 0, wx.ALL | wx.Centre, 5);
        topSizer.Add(contentSizer, 0, wx.ALL | wx.Centre, 5);

        panel.SetSizer(topSizer);
        topSizer.Fit(self)

        #绑定事件
        self.Bind(wx.EVT_RADIOBOX,self.onAction,self.rboxAction);
        self.Bind(wx.EVT_LIST_ITEM_ACTIVATED,self.onGradeList,self.listGrade);
        self.Bind(wx.EVT_TEXT_ENTER,self.onJxbId,self.inputTextJxbId);
        self.Bind(wx.EVT_BUTTON, self.onInsert,self.insertBtn);
        self.Bind(wx.EVT_BUTTON, self.onDelete,self.deleteBtn);
        self.Bind(wx.EVT_BUTTON, self.onExit,exitBtn);

        #查询课程信息并显示
        self.populate_courese_list();

    def populate_courese_list(self):
        """查询并显示所有课程信息"""
        grade_list=data.get_grade_list_by_student(self.userid);
        self.listGrade.DeleteAllItems();
        index=0;
        for grade in grade_list:
            self.listGrade.InsertItem(index,grade[0]);
            for i in range(1,7):
                if grade[i]==None:
                    self.listGrade.SetItem(index, i, '');
                else:
                    self.listGrade.SetItem(index,i,grade[i]);
            index+=1;
    def onAction(self,e):
        action=self.rboxAction.GetStringSelection();
        if action=='选课':
            self.inputTextJxbId.Enable();
            self.insertBtn.Enable();
            self.deleteBtn.Disable();
        elif action == '退选':
            self.inputTextJxbId.Disable();
            self.insertBtn.Disable();
            self.deleteBtn.Enable();
    def onGradeList(self,e):
        index=e.GetIndex();
        self.inputTextJxbId.SetValue(self.listGrade.GetItem(index,0).GetText());
        self.inputTextCourseId.SetValue(self.listGrade.GetItem(index, 1).GetText());
        self.inputTextCourseName.SetValue(self.listGrade.GetItem(index, 2).GetText());
        self.inputTextTeacherId.SetValue(self.listGrade.GetItem(index, 3).GetText());
        self.inputTextTeacherName.SetValue(self.listGrade.GetItem(index, 4).GetText());
        self.inputTextDescription.SetValue(self.listGrade.GetItem(index, 5).GetText());
        self.inputTextScore.SetValue(self.listGrade.GetItem(index, 6).GetText());

    def onJxbId(self,e):
        """输入完教学班号是自动检查其合法性并显示相关内容"""
        jxbid=self.inputTextJxbId.GetValue();
        if len(jxbid.strip())==0:
            return 0;
        if data.check_jwb_id(jxbid):
            row=data.check_jwb_id(jxbid);
            self.inputTextCourseId.SetValue(row[0]);
            self.inputTextCourseName.SetValue(row[1]);
            self.inputTextTeacherId.SetValue(row[2]);
            self.inputTextTeacherName.SetValue(row[3]);
            if row[4]==None:
                self.inputTextDescription.SetValue('');
            else:
                self.inputTextDescription.SetValue(row[4]);


    def onInsert(self,e):
        """选课：就是插入一条数据"""
        jxbid=self.inputTextJxbId.GetValue();
        if len(jxbid.strip())==0:
            wx.MessageBox("请输入教学班号！");
            self.inputTextJxbId.SetFocus();
            return 0;
        if data.check_grade_id(jxbid,userid=self.userid):
            wx.MessageBox("请不要重复选课！");
            self.inputTextJxbId.SetFocus();
            return 0;

        #插入记录
        data.insert_grade(jxbid,self.userid);
        #初始化界面
        self.refresh_screen();

    def refresh_screen(self):
        """重新刷新界面"""
        self.inputTextJxbId.SetValue('');
        self.inputTextCourseId.SetValue('');
        self.inputTextCourseName.SetValue('');
        self.inputTextTeacherId.SetValue('');
        self.inputTextTeacherName.SetValue('');
        self.inputTextDescription.SetValue('');

        #
        self.populate_courese_list();

    def onDelete(self,e):
        '''退课：删除一条数据'''
        jxbid=self.inputTextJxbId.GetValue();
        data.delete_grade(jxbid,self.userid);

        #
        self.refresh_screen();
    def onExit(self,e):
        self.Close();

if __name__=='__main__':
    app=wx.App();
    frame=StudentWindow(parent=None,title=2,userid='j001');
    frame.Show();
    app.MainLoop();

