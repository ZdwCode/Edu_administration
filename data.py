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
                        "classId varchar(20) primary key," \
                        "courseId varchar(20) not null," \
                        "userId varchar(20) not null," \
                        "description varchar(100)" \
                        ");"
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
if __name__=="__main__":
    '''#test fun check_login;
    check_login('j001','123456','教务')'''

    #test fun change_password
    change_password('j001','758258');
    
    