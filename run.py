
# encoding:utf-8


from flask import Flask, render_template, request, session, redirect, url_for
from flask_material import Material
import config
import os
import json
import re
# EG
# from flask_bootstrap import Bootstrap
# from flask_wtf import FlaskForm
# from wtforms import StringField, SubmitField
# from wtforms.validators import DataRequired
import pymssql


conn = pymssql.connect(host='.',
                       user='sa',
                       password='ZHJF2019eggs',
                       database='zhjfdemo1',
                       charset='utf8')
# conn = pymssql.connect(host='202.112.194.247',
#                        user='zonghejifenrd',
#                        password='zhjf2019rd',
#                        database='zonghejifen',
#                        charset='utf8')

#查看连接是否成功
cursor = conn.cursor()

app = Flask(__name__)
Material(app)
app.config.from_object(config)

#EG
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500
#lwd
app.secret_key='BLCU is our school'

# @app.before_request
# def is_login():
#     # if request.path == '/':
#     #     return None
#     if 'userID' not in session:
#         return None
#     elif session['role']=='student'and '/student'in request.path:
#         return None
#     elif session['role']=='teacher'and '/teacher'in request.path:
#         return None
#     else:
#         return redirect(url_for('login'))
#     #   return '无访问权限'

def getName(userID):
    getUserName = 'select userName from [user] where userID = \'{}\''.format(userID)
    cursor.execute(getUserName)
    name = (cursor.fetchall())[0][0]
    return name

def getGrade(userID):
    sql = '''select grade from [currGrade] where userID like {}'''.format(userID) #匹配字符串用like
    cursor.execute(sql)
    content1 = cursor.fetchall()
    return content1[0][0]

def getGPA(userID,grade,year,semester):
    #获取classID
    sql = '''select classID from [UserRoleMapping] where userID like {}'''.format(userID) #匹配字符串用like
    cursor.execute(sql)
    content1 = cursor.fetchall()
    classID = content1[0][0]
    #获取departID
    sql = '''select departID from [class] where classID={}'''.format(classID)
    cursor.execute(sql)
    content2 = cursor.fetchall()
    departID = content2[0][0]
    #获取大纲课程currID列表
    currList=[]
    for i in range(1,year+1):
        academicYear = str(grade-2000+i-1) + "-" + str(grade-2000+i)
        if (i == year and semester == 1):
            sql = '''select distinct t2.currID from [currGrade] as t1, [currArrange] as t2 
                where userID=(%s) and t2.departID=(%s) 
                and t1.currID = t2.currID 
                and t1.grade = t2.grade 
                and t1.academicYear like t2.academicYear 
                and t1.academicYear like (%s) 
                and t1.semester = t2.semester 
                and t1.semester = 1'''
            cursor.execute(sql,(userID,departID,academicYear))
            content3 = cursor.fetchall()
            for item in content3:
                currList.append(item[0])
        else:
            for j in range(1,3):
                sql = '''select distinct t2.currID from [currGrade] as t1, [currArrange] as t2 
                        where userID=(%s)  and t2.departID=(%s) 
                        and t1.currID = t2.currID 
                        and t1.grade = t2.grade 
                        and t1.academicYear like t2.academicYear 
                        and t1.academicYear like (%s) 
                        and t1.semester = t2.semester 
                        and t1.semester = (%s)'''
                cursor.execute(sql,(userID,departID,academicYear,j)) #替换academicYear必须使用%s并将变量放在execute语句
                content3 = cursor.fetchall()
                for item in content3:
                    currList.append(item[0])
        
    #获取该学生的成绩和学分
    gradeList=[] #该学生的所有成绩
    creditList=[] #每个成绩对应课程的学分
    for j in currList:
        sql = '''select examGrade, credit from [currGrade] as t1, [curriculum] as t2 
                where userID={} and t1.currID={} 
                and t1.currID = t2.currID 
                and isReexam=0'''.format(userID,j)
        cursor.execute(sql)
        content = cursor.fetchall()
        gradeList.append(content[0][0])
        creditList.append(content[0][1])
    #计算GPA(排除得分为0课程)
    pointList=[]
    creditListPoped=[]
    for m in range(len(gradeList)):
        if(gradeList[m]<=60): point=0
        elif(gradeList[m]>60 and gradeList[m]<=63): point=1.0
        elif(gradeList[m]>63 and gradeList[m]<=67): point=1.5
        elif(gradeList[m]>67 and gradeList[m]<=71): point=2.0
        elif(gradeList[m]>71 and gradeList[m]<=74): point=2.3
        elif(gradeList[m]>74 and gradeList[m]<=77): point=2.7
        elif(gradeList[m]>77 and gradeList[m]<=81): point=3.0
        elif(gradeList[m]>81 and gradeList[m]<=84): point=3.3
        elif(gradeList[m]>84 and gradeList[m]<=89): point=3.7
        else: point=4.0
        if(gradeList[m]>0): 
            pointList.append(point)
            creditListPoped.append(creditList[m])
    pointSum=0
    creditSum=0
    n=0
    for n in range(len(pointList)):
        pointSum+=(pointList[n]*creditList[n])
        creditSum+=creditList[n]
    if (creditSum==0): 
        gpa=0
    else:
        gpa = pointSum/creditSum
    return round(gpa,2) 
def fillinusername():
    sql="select userName from dbo.[user] where userID='"+userID+"'"
    cursor.execute(sql)
    userName=cursor.fetchall()
    userName=userName[0][0]
    return userName

userID=None

# #登陆界面
# @app.route('/',methods=['get'])
# def welcome():
#     error=None
#     session.clear()
#     return render_template('welcome.html', error=error) 

@app.route('/', methods = ['POST','GET'])
def login():
    error=None
    if request.method == 'GET':
        return render_template('welcome.html', error=error)
    else:
        global userID
        userID = request.form['username']
        pwd = request.form['passwd']
        if not all([userID,pwd]):
            if userID == "":
                error = "请输入用户名"
                return render_template('welcome.html',error=error)
            else:
                error = "请输入密码"
                return render_template('welcome.html',error=error)
        sql1 = "select userID from dbo.[user] where userID='"+userID+"' and password='"+pwd+"'"
        sql2 = "select roleid from dbo.userrolemapping where userID ='"+userID+"'"
        cursor.execute(sql1)
        #用一个rs_***变量获取数据
        rs_userid = cursor.fetchall()
        num=0
        for data in rs_userid:
            num=num+1
        if(num!=0):
            #用户登录设置session的userID和username
            session['userID']=userID
            session['username']=fillinusername()

            cursor.execute(sql2)
            rs_roleid= cursor.fetchone()
            roleID=rs_roleid[0]
            if(roleID==1):
                #将用户角色加入session
                session['role']='student'
                return redirect(url_for('stu_index'))
            else:
                session['role']='teacher'
                return redirect(url_for('tea_index'))
        else:
            error="账号或密码错误"
            return render_template('welcome.html',error = error)

def deny():
    return "Permission denied"

# def deny():
#     return "Permission denied"

#学生界面首页（综合积分界面）
@app.route('/student', methods=['GET','POST'])
def stu_index():
    global userID
    sql = '''select grade, departId 
            from EvaluationFinalScore 
            where userId={}'''.format(userID)
    cursor.execute(sql)
    content = cursor.fetchall()
    grade = content[0][0]
    depart = content[0][1]
    #使用user表必须使用[user]才不会报错
    sql = '''select userName,round(moralScore,2),round(intellectualScore,2),round(socialScore,2),round(bonus,2),round(finalScore,2)
            from [EvaluationFinalScore],[user] 
            where grade={} and departId={} and EvaluationFinalScore.userId=[user].userID'''.format(grade,depart)
    sortList=[0,0,0,0,0]
    scoreList=["moralScore","intellectualScore","socialScore","bonus","finalScore"]
    flag=0 #是否有排序条件
    if request.method == "POST":   
        Moral = request.values.get("moralGrade")
        sortList[0]=Moral
        Intel = request.values.get("intelGrade")
        sortList[1]=Intel
        Social = request.values.get("socialGrade")
        sortList[2]=Social
        Extra = request.values.get("extraGrade")
        sortList[3]=Extra
        Total = request.values.get("totalGrade")
        sortList[4]=Total
    #print(sortList)
    for i in range(5):
        if (sortList[i] != 0 and sortList[i] != ''): 
            flag = 1
            sql += " order by "
            break
    if (flag):
        flag=0
        for i in range(5):
            if (sortList[i] == "asc"): sql += (scoreList[i]+",")
            elif (sortList[i] == "desc"): sql += (scoreList[i]+" desc,")
        sql = sql[:-1] #去掉最后一个,
    
    cursor.execute(sql)
    all_data = cursor.fetchall()
    return render_template('student/index.html',result = all_data)


#个人成绩界面（根据课程属性筛选）（表格）
@app.route('/student/GradeByAttri', methods=['GET','POST'])
def GradeByAttri():
    
    global userID
    #获取classID
    sql = 'select classID from [UserRoleMapping] where userID like {}'.format(userID) #匹配字符串用like
    cursor.execute(sql)
    content1 = cursor.fetchall()
    classID = content1[0][0]
    #获取departID
    sql = 'select departID from [class] where classID={}'.format(classID)
    cursor.execute(sql)
    content2 = cursor.fetchall()
    departID = content2[0][0]

    result = []
    attri = ['专业课', '必修课', '公共课']
    if request.method == "POST":
        selectedAttri = request.values.get("attri")
        if selectedAttri == '专业课':
            selectedAttri = 'isSpec'
        elif selectedAttri == '必修课':
            selectedAttri = 'isCompulsory'
        elif selectedAttri == '公共课':
            selectedAttri = 'isIntern'

        #获取属性课程列表
        sql = '''select distinct currName, period, credit, examGrade, (select count(distinct userID) 
                                                                       from currGrade where currID = t1.currID) as num,  
                                                                      (select rank 
                                                                      from(select  rank() over (order by examGrade desc) rank,*
                                                                           from currGrade  
                                                                           where currID = t1.currID ) T
                                                                      where userID = {}) as ran 
                          from [currGrade] as t1, [currArrange] as t2, [curriculum] as t3 
                          where userID={} and t2.departID={}
                          and t1.currID = t2.currID 
                          and t1.currID = t3.currID 
                          and t1.grade = t2.grade 
                          and t1.academicYear like t2.academicYear
                          and t1.semester = t2.semester
                          and {} = 1'''.format(userID, userID, departID, selectedAttri)
        cursor.execute(sql)
        result = cursor.fetchall()
    return render_template('student/GradeByAttri.html',attri = attri, result = result)


#个人成绩界面（根据学期筛选）（表格）
@app.route('/student/GradeBySemester', methods=['GET','POST'])
def GradeBySemester():

    global userID
    # 获取classID
    sql = 'select classID from [UserRoleMapping] where userID like {}'.format(userID)  # 匹配字符串用like
    cursor.execute(sql)
    content1 = cursor.fetchall()
    classID = content1[0][0]
    # 获取departID
    sql = 'select departID from [class] where classID={}'.format(classID)
    cursor.execute(sql)
    content2 = cursor.fetchall()
    departID = content2[0][0]

    getYear = '''select distinct academicYear 
                    from currArrange'''
    year = getList(getYear)
    getSemester = '''select distinct semester 
                    from currArrange'''
    semester = getList(getSemester)

    result = []
    if request.method == "POST":
        selectedYear = request.values.get("year")
        selectedSemester = request.values.get("semester")

        # 获取属性课程列表
        sql = '''select distinct currName, period, credit, examGrade,(select count(distinct userID) 
                                                                       from currGrade where currID = t1.currID) as num,  
                                                                      (select rank 
                                                                      from(select  rank() over (order by examGrade desc) rank,*
                                                                           from currGrade  
                                                                           where currID = t1.currID ) T
                                                                      where userID = {}) as ran
                      from [currGrade] as t1, [currArrange] as t2, [curriculum] as t3 
                      where userID={} and t2.departID={}
                      and t1.currID = t2.currID 
                      and t1.currID = t3.currID 
                      and t1.grade = t2.grade 
                      and t1.academicYear like t2.academicYear 
                      and t1.semester = t2.semester 
                      and t1.semester = {} 
                      and t1.academicYear = \'{}\' '''.format(userID, userID, departID, selectedSemester, selectedYear)
        cursor.execute(sql)
        result = cursor.fetchall()
    return render_template('/student/GradeBySemester.html', year = year, semester=semester ,result = result)

def getList(search):
    cursor.execute(search)
    showList = cursor.fetchall()
    if(len(showList)):
        for i,item in enumerate(showList):
            showList[i] = str(item[0])
        return showList
    return None

#GPA界面(GPA显示及走向)
@app.route('/student/GPA')
def GPA():
    global userID
    grade = getGrade(userID)
    gpa = getGPA(userID,grade,4,2)
    GPAlist = []
    for i in range(1,5):
        for j in range(1,3):
            GPAlist.append(getGPA(userID,grade,i,j))
    return render_template('student/GPA.html',GPA=gpa, data=GPAlist,name=getName(userID))


#我的附加分界面（表格）
@app.route('/student/MyExtra')
def MyExtra():

    global userID
    items = getBonus(userID)
    return render_template('student/MyExtra.html',result = items)

def getBonus(userID):
    sql = '''select content, bonusValue, semester
            from bonusItem2user as t1,bonusItem as t2 
            where ownerId={} and t1.bonusItemID=t2.bonusItemID'''.format(userID)
    cursor.execute(sql)
    items = cursor.fetchall()
    return items

#我的综合积分界面（雷达）
@app.route('/student/MyComprehensiveEval')
def MyComprehensiveEval():
    global userID
    sql = '''select moralScore,intellectualScore,socialScore,bonus 
            from evaluationFinalScore 
            where userId={}'''.format(userID)
    cursor.execute(sql)
    scores = cursor.fetchall()
    return render_template('student/MyComprehensiveEval.html', score=list(scores[0]),name=getName(userID))

#综合积分汇总界面（表格）
@app.route('/student/TotalComprehensiveEval', methods=['GET','POST'])
def TotalComprehensiveEval():
    global userID
    sql = '''select grade, departId 
            from EvaluationFinalScore 
            where userId={}'''.format(userID)
    cursor.execute(sql)
    content = cursor.fetchall()
    grade = content[0][0]
    depart = content[0][1]
    #使用user表必须使用[user]才不会报错
    sql = '''select userName,round(moralScore,2),round(intellectualScore,2),round(socialScore,2),round(bonus,2),round(finalScore,2)
            from [EvaluationFinalScore],[user] 
            where grade={} and departId={} and EvaluationFinalScore.userId=[user].userID'''.format(grade,depart)
    sortList=[0,0,0,0,0]
    scoreList=["moralScore","intellectualScore","socialScore","bonus","finalScore"]
    flag=0 #是否有排序条件
    if request.method == "POST":   
        Moral = request.values.get("moralGrade")
        sortList[0]=Moral
        Intel = request.values.get("intelGrade")
        sortList[1]=Intel
        Social = request.values.get("socialGrade")
        sortList[2]=Social
        Extra = request.values.get("extraGrade")
        sortList[3]=Extra
        Total = request.values.get("totalGrade")
        sortList[4]=Total
    #print(sortList)
    for i in range(5):
        if (sortList[i] != 0 and sortList[i] != ''): 
            flag = 1
            sql += " order by "
            break
    if (flag):
        flag=0
        for i in range(5):
            if (sortList[i] == "asc"): sql += (scoreList[i]+",")
            elif (sortList[i] == "desc"): sql += (scoreList[i]+" desc,")
        sql = sql[:-1] #去掉最后一个,
    
    cursor.execute(sql)
    all_data = cursor.fetchall()
    return render_template('student/TotalComprehensiveEval.html',result = all_data)





#-----------------------------------------------------------------------------------------------
#教师界面

#教师首页
@app.route('/teacher')
def tea_index():
    return render_template('/teacher/index.html')



#专业总览
@app.route('/teacher/MajorOverview', methods=['GET','POST'])
def MajorOverview():
    getGrade = '''select distinct grade 
                from evaluationFinalScore
                order by grade'''
    grade = getList(getGrade)
    
    getYear = '''select distinct academicYear 
                from evaluationFinalScore
                order by academicYear '''
    year = getList(getYear)

    getDepart = '''select distinct departName 
                    from department 
                    where departID in 
                                        (select departID 
                                        from evaluationFinalScore)
                    order by departName'''
    depart = getList(getDepart)
    result = []
    if request.method == "POST":   
        selectedGrade = request.values.get("grade")
        selectedYear = request.values.get("year")
        selectedDepart = request.values.get("depart")
        
        if selectedDepart == None or selectedGrade == None or selectedYear == None:
            selectedNull = '请选择选项'
            result = [[]]
            return render_template('/teacher/MajorOverview.html',
                            grade = grade,
                            year = year,
                            depart = depart,
                            result = result,
                            selectedNull = selectedNull,
                            username=fillinusername())
        getDepartID = '''select departID 
                         from department 
                         where departName = \'{}\''''.format(selectedDepart)
        deprtID = 0
        res = getList(getDepartID)
        if(res):
            deprtID = int(res[0])

        getResult = '''select userName,round(intellectualScore,2),round(moralScore,2),round(socialScore,2),round(bonus,2),round(finalScore,2)
                       from evaluationFinalScore inner join [user] on evaluationFinalScore.userID = [user].userID
                       where departID = {} and academicYear = \'{}\' and grade = {}'''.format(deprtID,selectedYear,int(selectedGrade))
        cursor.execute(getResult)
        result = cursor.fetchall()
                                
    return render_template('/teacher/MajorOverview.html',
                            grade = grade,
                            year = year,
                            depart = depart,
                            result = result,
                            selectedNull = '',
                            username=fillinusername())

#课程总览
@app.route('/teacher/CourseOverview',methods=['GET','POST'])
def CourseOverview():
    result=[]
    getGrade = '''select distinct grade 
                from currGrade
                order by grade'''
    grade = getList(getGrade)
    
    getYear = '''select distinct academicYear 
                from currGrade
                order by academicYear'''
    year = getList(getYear)

    getSemester = '''select distinct semester
                    from currGrade
                    order by semester'''
    semester = getList(getSemester)

    if request.method == "POST":   
        selectedGrade = request.values.get("grade")
        selectedYear = request.values.get("year")
        selectedSeme = request.values.get("semester")
        courseName = request.values.get("courseName")
        
        getCurrID = '''select currID 
                       from curriculum
                       where currName = \'{}\''''.format(courseName)
        curID = int(getList(getCurrID)[0])

        under60 = countUser(curID,int(selectedGrade),selectedYear,int(selectedSeme),0,61)
        result.append(under60[0])
        btw67 = countUser(curID,int(selectedGrade),selectedYear,int(selectedSeme),60,71)
        result.append(btw67[0])
        btw78 = countUser(curID,int(selectedGrade),selectedYear,int(selectedSeme),70,81)
        result.append(btw78[0])
        btw89 = countUser(curID,int(selectedGrade),selectedYear,int(selectedSeme),80,91)
        result.append(btw89[0])
        above90 = countUser(curID,int(selectedGrade),selectedYear,int(selectedSeme),90,101)
        result.append(above90[0])

    return render_template('/teacher/CourseOverview.html',
                            grade = grade,
                            year = year,
                            semester = semester,
                            result = result,
                            )

def countUser(currID,grade,year,seme,lowgrade,highgrade):
    getUserNum = '''select count(examGrade)
                    from currGrade
                    where currID = {} and grade = {} and academicYear = \'{}\' 
                    and semester = {} and examGrade between {} and {}'''.format(currID,grade,year,seme,lowgrade,highgrade)
    cursor.execute(getUserNum)
    num = (cursor.fetchall())[0]
    return num

#个人查询-成绩走向
@app.route('/teacher/GradeTrend',methods=['GET','POST'])
def GradeTrend():
    if request.method == "POST":   
        userID = request.values.get("userID")
        name = getName(userID)
        grade = getGrade(userID)
        gpa = getGPA(userID,grade,4,2)
        return render_template('/teacher/GradeTrend.html',
                            name = name,
                            GPA = round(gpa,2))
    return render_template('/teacher/GradeTrend.html')

#个人查询-挂科情况统计
@app.route('/teacher/FailedCourses',methods=['GET','POST'])
def FailedCourses():
    name = ''
    courses = []
    if request.method == "POST":   
        userID = request.values.get("userID")
        name = getName(userID)
        courses = getCourses(userID)
    return render_template('/teacher/FailedCourses.html',
                            name = name,
                            courses = courses
                            )

def getCourses(userID):
    getFailedCur = '''select currGrade.currID,currName,credit,examGrade
                      from currGrade inner join curriculum on currGrade.currID = curriculum.currID
                      where userID = \'{}\' and examGrade < 60'''.format(userID)
    cursor.execute(getFailedCur)                          
    failedCur = cursor.fetchall()
    return failedCur

#个人查询-附加分统计
@app.route('/teacher/Bonus',methods=['GET','POST'])
def Bonus():

    items = []
    if request.method == "POST":   
        userID = request.values.get("userID")
        items = getBonus(userID)
    return render_template('/teacher/Bonus.html',result = items)


#多人（班级）比较-学生成绩
@app.route('/teacher/CompByStu', methods=['GET','POST'])
def CompByStu():

    names = []
    courses = []
    grades = []
    if request.method == "POST":
        stuID = request.values.get("MultiID")
        stuList = stuID.split(",")
        ID = stuList[0]
        getStuCour = '''select curriculum.currName
                        from currGrade inner join curriculum on currGrade.currID = curriculum.currID
                        where userID = \'{}\' and examGrade != 0'''.format(ID)
        courses = getList(getStuCour)
        for ID in stuList:
            name = getName(int(ID))
            names.append(name)
            currStuCour = getList(getStuCour)
            courses = list(set(currStuCour).intersection(set(courses)))
        for ID in stuList:
            gradeList = []
            for course in courses:
                getCourGrade = '''select examGrade
                                    from currGrade inner join curriculum on currGrade.currID = curriculum.currID
                                    where userID = \'{}\' and currName = \'{}\''''.format(ID,course)
                grade = getList(getCourGrade)[0]
                gradeList.append(grade)
            grades.append(gradeList)
    return render_template('/teacher/CompByStu.html', 
                                    names = names, 
                                    courses = courses, 
                                    grades = grades)

    


#多人（班级）比较-班级成绩对比
@app.route('/teacher/CompByClass', methods=['GET','POST'])
def CompByClass():

    two_class = []

    getYear = 'select distinct yearIn from class'
    year = getList(getYear)

    getMajor = '''select distinct departName 
                    from department 
                    where departID in 
                                        (select departID 
                                        from class)'''
    major = getList(getMajor)

    getClass = 'select distinct className from class'
    classes = getList(getClass)

    c1 = []
    c2 = []
    courses = []
    grades = []
    if request.method == "POST":   
        selectedYear = request.values.get("year")
        selectedMajor = request.values.get("major")
        selectedClass1 = request.values.get("class1")
        selectedClass2 = request.values.get("class2")
        
        two_class.append(selectedYear+selectedMajor+selectedClass1)
        two_class.append(selectedYear+selectedMajor+selectedClass2)

        getDepartID = '''select departID 
                         from department 
                         where departName = \'{}\''''.format(selectedMajor)
        deprtID = int(getList(getDepartID)[0])
        
        getClass1ID = '''select classID
                         from class
                         where className = \'{}\' and departID = {} and yearIn = {}'''.format(selectedClass1,deprtID,selectedYear)
        class1ID = int(getList(getClass1ID)[0])

        getClass2ID = '''select classID
                         from class
                         where className = \'{}\' and departID = {} and yearIn = {}'''.format(selectedClass2,deprtID,selectedYear)
        class2ID = int(getList(getClass2ID)[0])

        getResult = '''select currName,round(avg(examGrade),2) as avgGrade into c1
                        from UserRoleMapping inner join currGrade on UserRoleMapping.userID = currGrade.userID
                        inner join curriculum on currGrade.currID = curriculum.currID
                        where classID = {} and grade = {} and examGrade != 0
                        group by currName

                        select currName,round(avg(examGrade),2) as avgGrade into c2
                        from UserRoleMapping inner join currGrade on UserRoleMapping.userID = currGrade.userID
                        inner join curriculum on currGrade.currID = curriculum.currID
                        where classID = {} and grade = {} and examGrade != 0
                        group by currName

                        select c1.currName,c1.avgGrade as c1Grade,c2.avgGrade as c2Grade
                        from c1 inner join c2 on c1.currName  = c2.currName

                        drop table c1
                        drop table c2'''.format(int(class1ID),int(selectedYear),int(class2ID),int(selectedYear))
        cursor.execute(getResult)
        result = cursor.fetchall()
        
        for item in result:
            courses.append(item[0])
            c1.append(item[1])
            c2.append(item[2])
        grades.append(c1)
        grades.append(c2)


    return render_template('/teacher/CompByClass.html',
                                year = year,
                                major = major,
                                classes = classes, 
                                two_class = two_class,
                                courses = courses, 
                                grades = grades)

#多人（班级）比较-各届成绩对比
@app.route('/teacher/CompByYear')
def CompByYear():
    return render_template('/teacher/CompByYear.html')






#-----------------------------------------------------------------------------------------------
#班长界面
@app.route('/monitor')
def mostu_index():
    if userIDisNone():
        return redirect(url_for('index'))
    return render_template('/monitor/index.html', username=fillinusername())
    sql = "select userName from dbo.[user] where userID='" + userID + "'"
    cursor.execute(sql)
    userName = cursor.fetchall()
    userName = userName[0][0]
    return render_template('/monitor/index.html', username=userName)


# 个人成绩界面（根据课程属性筛选）（表格）
@app.route('/monitor/GradeByAttri', methods=['GET', 'POST'])
def moGradeByAttri():
    if userIDisNone():
        return redirect(url_for('index'))
    global userID
    # 获取classID
    sql = 'select classID from [UserRoleMapping] where userID like {}'.format(userID)  # 匹配字符串用like
    cursor.execute(sql)
    content1 = cursor.fetchall()
    classID = content1[0][0]
    # 获取departID
    sql = 'select departID from [class] where classID={}'.format(classID)
    cursor.execute(sql)
    content2 = cursor.fetchall()
    departID = content2[0][0]

    result = []
    attri = ['专业课', '必修课', '公共课']
    if request.method == "POST":
        selectedAttri = request.values.get("attri")
        if selectedAttri == '专业课':
            selectedAttri = 'isSpec'
        elif selectedAttri == '必修课':
            selectedAttri = 'isCompulsory'
        elif selectedAttri == '公共课':
            selectedAttri = 'isIntern'

        # 获取属性课程列表
        sql = '''select distinct currName, period, credit, examGrade, (select count(distinct userID) 
                                                                       from currGrade where currID = t1.currID) as num,  
                                                                      (select rank 
                                                                      from(select  rank() over (order by examGrade desc) rank,*
                                                                           from currGrade  
                                                                           where currID = t1.currID ) T
                                                                      where userID = {}) as ran 
                          from [currGrade] as t1, [currArrange] as t2, [curriculum] as t3 
                          where userID={} and t2.departID={}
                          and t1.currID = t2.currID 
                          and t1.currID = t3.currID 
                          and t1.grade = t2.grade 
                          and t1.academicYear like t2.academicYear
                          and t1.semester = t2.semester
                          and {} = 1'''.format(userID, userID, departID, selectedAttri)
        cursor.execute(sql)
        result = cursor.fetchall()

    return render_template('monitor/GradeByAttri.html', attri=attri, result=result, username=fillinusername())


# 个人成绩界面（根据学期筛选）（表格）
@app.route('/monitor/GradeBySemester', methods=['GET', 'POST'])
def moGradeBySemester():
    if userIDisNone():
        return redirect(url_for('index'))
    global userID
    # 获取classID
    sql = 'select classID from [UserRoleMapping] where userID like {}'.format(userID)  # 匹配字符串用like
    cursor.execute(sql)
    content1 = cursor.fetchall()
    classID = content1[0][0]
    # 获取departID
    sql = 'select departID from [class] where classID={}'.format(classID)
    cursor.execute(sql)
    content2 = cursor.fetchall()
    departID = content2[0][0]

    getYear = '''select distinct academicYear 
                    from currArrange'''
    year = getList(getYear)
    getSemester = '''select distinct semester 
                    from currArrange'''
    semester = getList(getSemester)

    result = []
    if request.method == "POST":
        selectedYear = request.values.get("year")
        selectedSemester = request.values.get("semester")

        # 获取属性课程列表
        sql = '''select distinct currName, period, credit, examGrade,(select count(distinct userID) 
                                                                       from currGrade where currID = t1.currID) as num,  
                                                                      (select rank 
                                                                      from(select  rank() over (order by examGrade desc) rank,*
                                                                           from currGrade  
                                                                           where currID = t1.currID ) T
                                                                      where userID = {}) as ran
                      from [currGrade] as t1, [currArrange] as t2, [curriculum] as t3 
                      where userID={} and t2.departID={}
                      and t1.currID = t2.currID 
                      and t1.currID = t3.currID 
                      and t1.grade = t2.grade 
                      and t1.academicYear like t2.academicYear 
                      and t1.semester = t2.semester 
                      and t1.semester = {} 
                      and t1.academicYear = \'{}\' '''.format(userID, userID, departID, selectedSemester, selectedYear)
        cursor.execute(sql)
        result = cursor.fetchall()
    return render_template('/monitor/GradeBySemester.html', year=year, semester=semester, result=result,
                           username=fillinusername())

    def getList(search):
        cursor.execute(search)
        showList = cursor.fetchall()
        for i, item in enumerate(showList):
            showList[i] = str(item[0])
        return showList


# GPA计算界面
@app.route('/monitor/GPACalculator')
def moGPACalculator():
    if userIDisNone():
        return redirect(url_for('index'))
    global userID
    grade = getGrade(userID)
    gpa = getGPA(userID, grade, 4, 2)
    return render_template('monitor/GPACalculator.html', GPA=gpa, username=fillinusername())


# 查看GPA走向界面（折线）
@app.route('/monitor/GPATrend')
def moGPATrend():
    if userIDisNone():
        return redirect(url_for('index'))
    global userID
    grade = getGrade(userID)
    GPA = []
    for i in range(1, 5):
        for j in range(1, 3):
            GPA.append(getGPA(userID, grade, i, j))
    return render_template('monitor/GPATrend.html', data=GPA, name=getName(userID), username=fillinusername())


# 我的附加分界面（表格）
@app.route('/monitor/MyExtra')
def moMyExtra():
    if userIDisNone():
        return redirect(url_for('index'))
    global userID
    items = getBonus(userID)
    return render_template('monitor/MyExtra.html', result=items, username=fillinusername())


def mogetBonus(userID):
    sql = '''select content, bonusValue, semester
            from bonusItem2user as t1,bonusItem as t2 
            where ownerId={} and t1.bonusItemID=t2.bonusItemID'''.format(userID)
    cursor.execute(sql)
    items = cursor.fetchall()
    return items


# 我的综合积分界面（雷达）
@app.route('/monitor/MyComprehensiveEval')
def moMyComprehensiveEval():
    if userIDisNone():
        return redirect(url_for('index'))
    global userID
    sql = '''select moralScore,intellectualScore,socialScore,bonus 
            from evaluationFinalScore 
            where userId={}'''.format(userID)
    cursor.execute(sql)
    scores = cursor.fetchall()
    return render_template('monitor/MyComprehensiveEval.html', score=list(scores[0]), name=userID,
                           username=fillinusername())


# 综合积分汇总界面（表格）
@app.route('/monitor/TotalComprehensiveEval', methods=['GET', 'POST'])
def moTotalComprehensiveEval():
    if userIDisNone():
        return redirect(url_for('index'))
    global userID
    sql = '''select grade, departId 
            from EvaluationFinalScore 
            where userId={}'''.format(userID)
    cursor.execute(sql)
    content = cursor.fetchall()
    grade = content[0][0]
    depart = content[0][1]
    # 使用user表必须使用[user]才不会报错
    sql = '''select userName,moralScore,intellectualScore,socialScore,bonus,finalScore 
            from [EvaluationFinalScore],[user] 
            where grade={} and departId={} and EvaluationFinalScore.userId=[user].userID'''.format(grade, depart)
    sortList = [0, 0, 0, 0, 0]
    scoreList = ["moralScore", "intellectualScore", "socialScore", "bonus", "finalScore"]
    flag = 0  # 是否有排序条件
    if request.method == "POST":
        Moral = request.values.get("moralGrade")
        sortList[0] = Moral
        Intel = request.values.get("intelGrade")
        sortList[1] = Intel
        Social = request.values.get("socialGrade")
        sortList[2] = Social
        Extra = request.values.get("extraGrade")
        sortList[3] = Extra
        Total = request.values.get("totalGrade")
        sortList[4] = Total
    for i in range(5):
        if (sortList[i] != 0):
            flag = 1
            sql += " order by "
            break
    if (flag):
        for i in range(5):
            if (sortList[i] == "asc"):
                sql += (scoreList[i] + ",")
            elif (sortList[i] == "desc"):
                sql += (scoreList[i] + " desc,")
        sql = sql[:-1]  # 去掉最后一个,

    cursor.execute(sql)
    all_data = cursor.fetchall()
    return render_template('monitor/TotalComprehensiveEval.html', result=all_data, username=fillinusername())


#班级成绩
@app.route('/monitor/Class', methods=['GET', 'POST'])
def Class():
    if userIDisNone():
        return redirect(url_for('index'))
    global userID
    # 获取classID
    sql = 'select classID from [UserRoleMapping] where userID like {}'.format(userID)  # 匹配字符串用like
    cursor.execute(sql)
    content1 = cursor.fetchall()
    classID = content1[0][0]
    # 获取departID
    sql = 'select departID from [class] where classID={}'.format(classID)
    cursor.execute(sql)
    content2 = cursor.fetchall()
    departID = content2[0][0]

    getLesson = '''select distinct currName
                   from curriculum as t1,currArrange as t2
                   where (isCompulsory=1 or isSpec=1) and isPE=0 and t1.currID=t2.currID and t2.departID={}'''.format(departID)
    lesson = getList(getLesson)

    result = []
    if request.method == "POST":
        selectedLesson = request.values.get("lesson")

        # 获取属性课程列表
        sql = '''select userName,examGrade
                 from [user] as t1,currGrade as t2,UserRoleMapping as t3, curriculum as t4
                 where t1.userID=t2.userID and t2.userID =t3.userID and t2.currID=t4.currID and currName=\'{}\' and classID={} and isReexam=0 and grade>0'''.format(selectedLesson, classID)
        cursor.execute(sql)
        result = cursor.fetchall()
    return render_template('/monitor/Class.html', lesson=lesson, result=result,
                           username=fillinusername())



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

