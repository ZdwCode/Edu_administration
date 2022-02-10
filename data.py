'''数据管理模块'''
import pymysql
info={
        'host':'localhost',
        'port':3306,
        'user':'root',
        'password':'758258',
        'databases_name':'jwxt'
    }
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

def check_login(userid,password,usertype):
    """检查用户登录信息是否正确"""
    con=get_connect(**info);
    cursor = con.cursor()
    try:
        sql_pattern="select username from userinfo where userid=%s and password=%s and userType=%s";
        cursor.execute(sql_pattern,[userid,password,usertype])
        row = cursor.fetchone();
        if row:#确实查询到了用户
            r=tuple(row);
            print("登录成功");
            return r[0];
        else:
            print("登录失败");
            return False;
    except Exception as e:
        print(e)
        con.rollback();
    finally:
        cursor.close();
        con.close();

def change_password(uesrid,password):
    """修改用户密码"""
    con=get_connect(**info);
    cursor=con.cursor()
    try:
        sql="update userinfo set password=%s where userid =%s";
        cursor.execute(sql,[password,uesrid])
        con.commit();
        print('密码修改成功')
    except Exception as e :
        print(e)
        con.rollback();
    finally:
        cursor.close();
        con.close();

def check_user_id(userid):
    """检查userinfo中是否存在userid"""
    con=get_connect(**info);
    cursor=con.cursor();
    try:
        sql="select userid,username from userinfo where userid=%s;";
        cursor.execute(sql,[userid]);
        row=cursor.fetchone();
        if row:
            return row[1];#返回用户名
        else:
            return False;
    except Exception as  e:
        print(e)
        con.rollback();
    finally:
        cursor.close();
        con.close();

def get_user_list(usertype):
    """查找数据库userinfo表，获取类型为user_type的用户信息列表"""
    con=get_connect(**info);
    cursor=con.cursor();
    try:
        sql="select userid,username,gender,department,phone,birthday from userinfo where usertype=%s";
        cursor.execute(sql,[usertype]);
        results=cursor.fetchall();
        user_list=[];
        for user in results:
            user_list.append(user);
        return user_list;
    finally:
        cursor.close();
        con.close();

def insert_user(usertype,userid,username,gender,birthday,department,phone,password):
    """插入一条记录"""
    con=get_connect(**info);
    cursor=con.cursor()
    try:
        sql="insert into userinfo(usertype,userid,username,gender,birthday,department,phone,password) values(%s,%s,%s," \
            "%s,%s,%s,%s,%s); "
        cursor.execute(sql,[usertype,userid,username,gender,birthday,department,phone,password])
        con.commit();
    except Exception as e:
        print(e);
        con.rollback();
    finally:
        cursor.close();
        con.close();

def update_user(userid,username,gender,birthday,department,phone):
    """按userid更新一条数据"""
    con=get_connect(**info);
    cursor=con.cursor();
    try:
        sql='''update userinfo set username=%s,gender=%s,birthday=%s,department=%s,phone=%s where userid=%s;'''
        cursor.execute(sql,[username,gender,birthday,department,phone,userid])
        con.commit();
    except Exception as e:
        print(e);
        con.rollback();
    finally:
        cursor.close();
        con.close();

def delete_userbyid(userid):
    """删除一个用户"""
    con=get_connect(**info);
    cursor=con.cursor();
    try:
        sql='''delete from userinfo where userid=%s;'''
        cursor.execute(sql,[userid]);
        con.commit();
    except Exception as e:
        print(e);
        con.rollback();
    finally:
        cursor.close();
        con.close();

########课程管理
def check_course_id(courseid):
    """检查course表中是否存在courseid"""
    con=get_connect(**info);
    cursor=con.cursor()
    try:
        sql='''select courseid,coursename from course where courseid=%s;'''
        cursor.execute(sql,[courseid])
        row=cursor.fetchone();
        if row:
            return row[1];#返回课程名称
        else:
            return False;
    except Exception as e:
        print(e);
    finally:
        cursor.close();
        con.close();
def get_course_list():
    """查找数据库course表 获取课程信息列表"""
    con = get_connect(**info);
    cursor = con.cursor();
    try:
        sql='''select courseid,coursename,credit,description from course;''';
        cursor.execute(sql);
        courses=cursor.fetchall();
        course_list=[];
        for course in courses:
            course_list.append(course);
        return course_list;
    finally:
        cursor.close();
        con.close();

def insert_course(courseid,coursename,credit,description):
    con = get_connect(**info);
    cursor = con.cursor();
    try:
        sql='''insert into course(courseid,coursename,credit,description) values(%s,%s,%s,%s);'''
        cursor.execute(sql,[courseid,coursename,credit,description])
        con.commit();
    except Exception as e :
        print(e);
        con.rollback();
    finally:
        cursor.close();
        con.close();

def update_course(courseid,coursename,credit,description):
    """更新一条数据到course表"""
    con=get_connect(**info);
    cursor=con.cursor();
    try:
        sql='''update course set coursename=%s,credit=%s,description=%s where courseid=%s;'''
        cursor.execute(sql,[coursename,credit,description,courseid])
        con.commit();
    except Exception as e:
        print(e);
        con.rollback();
    finally:
        cursor.close();
        con.close();

def delete_course(courseid):
    """course中删除一条记录"""
    con=get_connect(**info);
    cursor=con.cursor();
    try:
        sql='''delete from course where courseid=%s;'''
        cursor.execute(sql,[courseid]);
    finally:
        cursor.close();
        con.close();

#### jxb==class
def check_jwb_id(classid):
    """检查class中是否存在classid"""
    con=get_connect(**info);
    cursor=con.cursor()
    try:
        sql='''select cr.courseId,c.coursename,cr.userId,u.username,cr.description from
        class cr,course c,userinfo u where cr.courseId=c.courseid and cr.userId=u.userid
        and cr.classId=%s;'''
        cursor.execute(sql,classid);
        row = cursor.fetchone();
        if row:
            return row;
        else:
            return False;
    finally:
        cursor.close();
        con.close();

def get_jxb_list():
    """查找数据库class 获取课程安排教学班信息列表"""
    con=get_connect(**info);
    cursor=con.cursor()
    try:
        sql='''select cr.classid,cr.courseid,c.coursename,cr.userid,u.username,cr.description
        from class cr,course c,userinfo u
        where cr.courseid=c.courseid
        and cr.userid=u.userid;'''
        cursor.execute(sql);
        results=cursor.fetchall();
        jxb_list=[];
        for jxb in results:
            jxb_list.append(jxb);
        return jxb_list;
    finally:
        cursor.close();
        con.close();

def insert_jxb(classid,courseid,userid,description):
    """插入一条数据到class表中"""
    con=get_connect(**info);
    cursor=con.cursor();
    try:
        sql='''insert into class(classid,courseid,userid,description) 
        values(%s,%s,%s,%s);'''
        cursor.execute(sql,[classid,courseid,userid,description]);
        con.commit();
    except Exception as e:
        print(e);
        con.rollback();
    finally:
        cursor.close();
        con.close();

def update_jxb(classid,courseid,userid,description):
    """更新一条信息.到TB表"""
    con = get_connect(**info);
    cursor = con.cursor();
    try:
        sql='''update class set courseid=%s,userid=%s,description=%s where classid=%s;'''
        cursor.execute(sql,(courseid,userid,description,classid));
        con.commit();
    finally:
        cursor.close();
        con.close();

def delete_jxb(classid):
    """删除一条记录"""
    con=get_connect(**info);
    cursor=con.cursor()
    try:
        sql='''delete from class where classid=%s''';
        cursor.execute(sql,[classid]);
        con.commit();
    finally:
        cursor.close();
        con.close();


###########学生选课
def check_grade_id(classid,userid):
    """检查grade表中是否存在classid userid 即userid是否已经选classid"""
    con = get_connect(**info);
    cursor = con.cursor()
    try:
        sql='''select classid from grades where classid=%s and userid=%s;'''
        cursor.execute(sql,[classid,userid]);
        row=cursor.fetchone();
        if row:
            return True;
        else:return False;
    finally:
        cursor.close();
        con.close();

def get_grade_list_by_student(userid):
    """查找数据库grade表 获取学生userid选课信息列表"""
    con = get_connect(**info);
    cursor = con.cursor();
    try:
        sql='''select g.classid,cr.courseid,c.coursename,cr.userid,u.username,cr.description,g.score
        from grades g,class cr,course c,userinfo u
        where g.classid=cr.classid
        and cr.courseid=c.courseid
        and cr.userid=u.userid
        and g.userid=%s;'''
        cursor.execute(sql,[userid]);
        grades=cursor.fetchall();
        grade_list=[];
        for grade in grades:
            grade_list.append(grade);
        return grade_list;
    finally:
        cursor.close();
        con.close();

def insert_grade(classid,userid):
    """插入一条数据到grade表中"""
    con=get_connect(**info);
    cursor=con.cursor();
    try:
        sql='''insert into grades(classid,userid) 
        values(%s,%s);'''
        cursor.execute(sql,[classid,userid]);
        con.commit();
    except Exception as e:
        print(e);
        con.rollback();
    finally:
        cursor.close();
        con.close();

def delete_grade(classid,userid):
    """删除一条记录"""
    con=get_connect(**info);
    cursor=con.cursor()
    try:
        sql='''delete from grades where classid=%s and userid=%s''';
        cursor.execute(sql,[classid,userid]);
        con.commit();
    finally:
        cursor.close();
        con.close();

#####教师成绩录入
def get_jwbid_list_by_userid(userid):
    """查找数据库jxb表，获取指定教师uerid授课课程信息"""
    con = get_connect(**info);
    cursor = con.cursor();
    try:
        sql='''select cr.classid from class cr where userid=%s;'''
        cursor.execute(sql,[userid]);
        jxbs=cursor.fetchall();
        jxbs_list=[];
        for jxb in jxbs:
            jxbs_list.append(jxb);
        return jxbs_list;
    finally:
        cursor.close();
        con.close();

def update_grade_score(grades_list):
    """更新学生成绩信息列表"""
    con = get_connect(**info);
    cursor = con.cursor();
    try:
        sql='''update grade set score=%s where classid=%s and userid=%s;'''
        for grade in grades_list:
            cursor.execute(sql,grade);
        con.commit();
    finally:
        cursor.close();
        con.close();
def get_grade_list_by_jxbid(classid):
    """查找grade表，获取指定课程的学生选课信息列表"""
    con = get_connect(**info);
    cursor = con.cursor();
    try:
        sql='''select g.userid,u.username,u.gender,u.department,g.score
        from grades g ,userinfo u where g.userid=u.userid
        and g.classid=%s;'''
        cursor.execute(sql,[classid]);
        grades=cursor.fetchall();
        grades_list=[];
        for grade in grades:
            grades_list.append(grade)
        return grades_list;
    finally:
        cursor.close();
        con.close();
if __name__=="__main__":
    '''#test fun check_login;
    check_login('j001','123456','教务')'''

    #test fun change_password
    #change_password('j001','758258');

    '''#test fun check_user_id
    username=check_user_id('j001')
    if username:
        print(username);
    else:
        print("userid 不存在")'''

    '''#test fun get_user_id
    user_list=get_user_list('教务');
    for user in user_list:
        print(user)#('j001', '章登炜', '男', '计算机系', '18179219692', '1999/10/28')
        print(len(user))#6
    '''
    
    '''#test fun insert_user
    # usertype, userid, username, gender, birthday, department, phone, password
    user_wzx={
        'usertype':'校长',
        'userid':'j003',
        'username':'王芷欣',
        'gender':'女',
        "birthday":'1999/2/20',
        'department':'公共事业管理',
        'phone':'17300223720',
        'password':'320975'
    }
    insert_user(**user_wzx)'''

    '''#test fun insert_user
    # usertype, userid, username, gender, birthday, department, phone, password
    user_wzx={
        'userid':'j003',
        'username':'王芷欣',
        'gender':'女',
        "birthday":'1999/2/20',
        'department':'公管',
        'phone':'17300223720'
    }
    update_user(**user_wzx)'''

    '''#test fun delete_user
    delete_userbyid('j003');'''

    '''#test fun check_class_id
    print(check_jwb_id('1'));#('2018', '算法设计与分析', 'j001', '章登炜', '')'''

    '''insert_course(courseid='2017',coursename='计算机网络',credit='3.5',description=None);
    insert_jxb(classid='2',courseid='2017',userid='j001',description=None);
    #test fun get_grade_by_userid
    print(get_grade_list_by_student('j001'));#[('1', '2018', '算法设计与分析', 'j001', '章登炜', '', None)]'''

    #test fun get_grade_list_by_jxbid(classid)
    print(get_grade_list_by_jxbid('1'));

    """测试一下github   """
