import data;
import wx
class CourseWindow(wx.Dialog):
    def __init__(self,parent,title):
        wx.Frame.__init__(self,parent,title=title,size=(800,600));
        panel=wx.Panel(self,wx.ID_ANY);

        #创建控件
        lblListAction=['插入','修改','删除'];
        self.rboxAction=wx.RadioBox(panel,label='操作',choices=lblListAction);

        self.listCourse=wx.ListCtrl(panel,wx.ID_ANY,size=(400,400),style=wx.LC_REPORT);
        self.listCourse.InsertColumn(0,'课程ID',width=50);
        self.listCourse.InsertColumn(1, '课程名称', width=100);
        self.listCourse.InsertColumn(2, '学分', width=50);
        self.listCourse.InsertColumn(3, '说明', width=200);

        labelCourseId = wx.StaticText(panel, wx.ID_ANY, '课程id')
        self.inputTextCourseId = wx.TextCtrl(panel, wx.ID_ANY, '')
        labelCourseName = wx.StaticText(panel, wx.ID_ANY, '课程名称')
        self.inputTextCourseName = wx.TextCtrl(panel, wx.ID_ANY, '')
        labelCredit = wx.StaticText(panel, wx.ID_ANY, '学分')
        self.inputTextCredit = wx.TextCtrl(panel, wx.ID_ANY, '')
        labelDescription = wx.StaticText(panel, wx.ID_ANY, '课程说明')
        self.inputTextDescription = wx.TextCtrl(panel, wx.ID_ANY, '');

        # 按钮
        self.insertBtn = wx.Button(panel, wx.ID_ANY, '插入')
        self.updateBtn = wx.Button(panel, wx.ID_ANY, '更新');
        self.updateBtn.Disable();
        self.deleteBtn = wx.Button(panel, wx.ID_ANY, '删除')
        self.deleteBtn.Disable();
        exitBtn = wx.Button(panel, wx.ID_ANY, '退出');

        topSizer = wx.BoxSizer(wx.VERTICAL);
        optionSizer = wx.BoxSizer(wx.HORIZONTAL);
        contentSizer = wx.BoxSizer(wx.HORIZONTAL);
        listSizer = wx.BoxSizer(wx.HORIZONTAL);
        editSizer = wx.BoxSizer(wx.VERTICAL);
        courseidSizer = wx.BoxSizer(wx.HORIZONTAL);
        courseNameSizer = wx.BoxSizer(wx.HORIZONTAL);
        creditSizer = wx.BoxSizer(wx.HORIZONTAL);
        descriptionSizer = wx.BoxSizer(wx.HORIZONTAL);
        btnSizer = wx.BoxSizer(wx.HORIZONTAL);

        optionSizer.Add(self.rboxAction,0,wx.ALL,5);

        listSizer.Add(self.listCourse,0,wx.ALL,5);

        courseidSizer.Add(labelCourseId,0,wx.ALL,5);
        courseidSizer.Add(self.inputTextCourseId, 0, wx.ALL, 5);
        courseNameSizer.Add(labelCourseName,0,wx.ALL,5);
        courseNameSizer.Add(self.inputTextCourseName,0,wx.ALL,5);
        creditSizer.Add(labelCredit,0,wx.ALL,5);
        creditSizer.Add(self.inputTextCredit,0,wx.ALL,5);
        descriptionSizer.Add(labelDescription,0,wx.ALL,5);
        descriptionSizer.Add(self.inputTextDescription,0,wx.ALL,5);

        btnSizer.Add(self.insertBtn,0,wx.ALL,0);
        btnSizer.Add(self.updateBtn, 0, wx.ALL, 0);
        btnSizer.Add(self.deleteBtn, 0, wx.ALL, 0);
        btnSizer.Add(exitBtn, 0, wx.ALL, 0);

        editSizer.Add(courseidSizer,0,wx.ALL,0);
        editSizer.Add(courseNameSizer, 0, wx.ALL, 0);
        editSizer.Add(descriptionSizer, 0, wx.ALL, 0);
        editSizer.Add(creditSizer, 0, wx.ALL, 0);
        editSizer.Add(btnSizer,0,wx.ALL,0);

        contentSizer.Add(listSizer,0,wx.ALL,0);
        contentSizer.Add(editSizer,0,wx.ALL,0);

        topSizer.Add(optionSizer,0,wx.ALL,0);
        topSizer.Add(contentSizer, 0, wx.ALL, 0);

        panel.SetSizer(topSizer);
        topSizer.Fit(self);

        #绑定事件
        self.Bind(wx.EVT_RADIOBOX,self.onAction,self.rboxAction);
        self.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.onCourseList, self.listCourse);
        self.Bind(wx.EVT_BUTTON, self.onInsert, self.insertBtn);
        self.Bind(wx.EVT_BUTTON, self.onUpdate, self.updateBtn);
        self.Bind(wx.EVT_BUTTON, self.onDelete, self.deleteBtn);
        self.Bind(wx.EVT_BUTTON, self.onExit, exitBtn);

        self.populate_course_list();

    def populate_course_list(self):
        """获取所有课程列表"""
        course_list=data.get_course_list();
        self.listCourse.DeleteAllItems();
        index=0;
        for course in course_list:
            self.listCourse.InsertItem(index,course[0]);
            self.listCourse.SetItem(index,1,course[1]);
            self.listCourse.SetItem(index,2,str(course[2]));
            if(course[3]==None):
                self.listCourse.SetItem(index, 3, '');
            else:
                self.listCourse.SetItem(index,3,course[3]);
            index+=1;

    def onAction(self,e):
        action = self.rboxAction.GetStringSelection();
        print(action, e)
        if action == '插入':
            self.inputTextCourseId.Enable();
            self.insertBtn.Enable();
            self.updateBtn.Enable();
            self.deleteBtn.Enable();
        if action == '修改':  # 由于数据库是按id修改的 故要先确定id
            self.inputTextCourseId.Disable();
            self.insertBtn.Disable();
            self.updateBtn.Enable();
            self.deleteBtn.Disable();
        if action == '删除':
            self.inputTextCourseId.Disable();
            self.insertBtn.Disable();
            self.updateBtn.Disable();
            self.deleteBtn.Enable();
    def onCourseList(self,e):
        """选中课程 并将详细信息显示在右侧"""
        index=e.GetIndex();
        self.inputTextCourseId.SetValue(self.listCourse.GetItem(index,0).GetText());
        self.inputTextCourseName.SetValue(self.listCourse.GetItem(index, 1).GetText());
        self.inputTextCredit.SetValue(self.listCourse.GetItem(index,2).GetText());
        self.inputTextDescription.SetValue(self.listCourse.GetItem(index, 3).GetText());
    def onInsert(self,e):
        """插入一条数据"""
        courseid=self.inputTextCourseId.GetValue();
        coursename=self.inputTextCourseName.GetValue();
        credit=self.inputTextCredit.GetValue();
        description=self.inputTextDescription.GetValue();

        if len(courseid.strip())==0:
            wx.MessageBox("请输入课程id");
            self.inputTextCourseId.SetFocus();
            return 0;
        if len(coursename.strip()) == 0:
            wx.MessageBox("请输入课程名称");
            self.inputTextCourseName.SetFocus();
            return 0;
        if data.check_course_id(courseid):
            wx.MessageBox("请输入课程id已存在，请重新输入");
            self.inputTextCourseId.SetFocus();
            return 0;
        #插入记录
        data.insert_course(courseid=courseid,
                           coursename=coursename,
                           credit=credit,
                           description=description);

        self.refresh_screen();
    def refresh_screen(self):
        self.inputTextCourseId.SetValue('');
        self.inputTextCourseName.SetValue('');
        self.inputTextCredit.SetValue('');
        self.inputTextDescription.SetValue('');

        self.populate_course_list();
    def onUpdate(self,e):
        """更新一条记录"""
        courseid = self.inputTextCourseId.GetValue();
        coursename = self.inputTextCourseName.GetValue();
        credit = self.inputTextCredit.GetValue();
        description = self.inputTextDescription.GetValue();
        if len(coursename.strip())==0:
            wx.MessageBox("请输入课程名称");
            self.inputTextCourseName.SetFocus();
            return 0;
        #更新记录
        data.update_course(courseid=courseid,
                           coursename=coursename,
                           credit=credit,
                           description=description);

        self.populate_course_list();
    def onDelete(self,e):
        """删除一条记录"""
        courseid=self.inputTextCourseId.GetValue();
        data.delete_userbyid(courseid);
        self.refresh_screen();
    def onExit(self,e):
        self.Close();
if __name__=="__main__":
    app = wx.App()
    frame = CourseWindow(parent=None,title="课程管理");
    frame.Show();
    app.MainLoop();