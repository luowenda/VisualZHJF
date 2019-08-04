# encoding:utf-8


from flask import Flask, render_template,request
import config
import os
import json
# EG
import numpy as np
import pandas as pd
from IPython.display import HTML
from flask import Flask, render_template, session, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import pymssql

conn = pymssql.connect(host='.',
                       user='sa',
                       password='ZHJF2019eggs',
                       database='zhjfdemo1',
                       charset='utf8')

#查看连接是否成功
cursor = conn.cursor()

app = Flask(__name__)
app.config.from_object(config)
#EG
bootstrap = Bootstrap(app)

#EG
class NameForm(FlaskForm):
    id = StringField('请输入学号：', validators=[DataRequired()])
    submit = SubmitField('提交')

#EG
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500



#EG
#登录界面&学生界面首页？
@app.route('/student')
def stu_index():
    return render_template('/student/index.html')

#个人成绩界面（根据课程属性筛选）（表格）
@app.route('/student/GradeByAttri')
def GradeByAttri():
    data = open('data/16cs1.json', encoding='utf8').read()
    columns = ["学号", "高数1","高数2","线性代数"]
    dat = json.loads(data)
    dic = { #dict中key应和columns一致
        "学号": [],
        "高数1": [],
        "高数2": [],
        "线性代数": []
    }
    for stu in dat['2016CS1']:
        dic['学号'].append(stu)
        dic['高数1'].append(dat['2016CS1'][stu]['3250300106'])
        dic['高数2'].append(dat['2016CS1'][stu]['3250300204'])
        dic['线性代数'].append(dat['2016CS1'][stu]['3250300303'])
    df = pd.DataFrame(data=dic, columns=columns)
    convert = df.to_html(classes='table table-striped table-hover table-sm table-borderless',
                            border=None, justify=None)
    return render_template('/student/GradeByAttri.html',table = convert)

#个人成绩界面（根据学期筛选）（表格）
@app.route('/student/GradeBySemester')
def GradeBySemester():
    data = open('data/16cs1.json', encoding='utf8').read()
    columns = ["学号", "高数1","高数2","线性代数"]
    dat = json.loads(data)
    dic = { #dict中key应和columns一致
        "学号": [],
        "高数1": [],
        "高数2": [],
        "线性代数": []
    }
    for stu in dat['2016CS1']:
        dic['学号'].append(stu)
        dic['高数1'].append(dat['2016CS1'][stu]['3250300106'])
        dic['高数2'].append(dat['2016CS1'][stu]['3250300204'])
        dic['线性代数'].append(dat['2016CS1'][stu]['3250300303'])
    df = pd.DataFrame(data=dic, columns=columns)
    convert = df.to_html(classes='table table-striped table-hover table-sm table-borderless',
                            border=None, justify=None)
    return render_template('/student/GradeBySemester.html',table = convert)

#GPA计算界面
@app.route('/student/GPACalculator')
def GPACalculator():
    userID = '1031101' #TODO需要从登录信息获取
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
    #获取大纲课程currID列表
    sql = 'select distinct t2.currID from [currGrade] as t1, [currArrange] as t2 \
        where userID={}  and t2.departID={}\
        and t1.currID = t2.currID \
        and t1.grade = t2.grade \
        and t1.academicYear like t2.academicYear \
        and t1.semester = t2.semester'.format(userID,departID)
    cursor.execute(sql)
    content3 = cursor.fetchall()
    currList = []
    for i in content3:
        currList.append(i[0])
    #获取该学生的成绩和学分
    gradeList=[] #该学生的所有成绩
    creditList=[] #每个成绩对应课程的学分
    for j in currList:
        sql = 'select examGrade, credit from [currGrade] as t1, [curriculum] as t2 \
        where userID={} and t1.currID={}\
        and t1.currID = t2.currID \
        and isReexam=0'.format(userID,j)
        cursor.execute(sql)
        content = cursor.fetchall()
        gradeList.append(content[0][0])
        creditList.append(content[0][1])
    #计算GPA(未排除得分为0课程)
    pointList=[]
    for m in gradeList:
        if(m<=60): point=0
        elif(m>60 and m<=63): point=1.0
        elif(m>63 and m<=67): point=1.5
        elif(m>67 and m<=71): point=2.0
        elif(m>71 and m<=74): point=2.3
        elif(m>74 and m<=77): point=2.7
        elif(m>77 and m<=81): point=3.0
        elif(m>81 and m<=84): point=3.3
        elif(m>84 and m<=89): point=3.7
        else: point=4.0
        pointList.append(point)
    pointSum=0
    creditSum=0
    n=0
    for n in range(len(pointList)):
        pointSum+=(pointList[n]*creditList[n])
        creditSum+=creditList[n]
    gpa = pointSum/creditSum

    return render_template('student/GPACalculator.html',GPA=round(gpa,2))


#查看GPA走向界面（折线）
@app.route('/student/GPATrend')
def GPATrend():
    A_data = [3.17, 3.75, 3.21, 3.46, 3.43, 3.31, 3.08, 3.61]
    B_data = [3.1, 3.00, 3.38, 3.01, 3.52, 3.87, 3.37, 3.85]
    return render_template('student/GPATrend.html', A_data=A_data, B_data=B_data)

#我的附加分界面（表格）#TODO修正表格编号方式
@app.route('/student/MyExtra')
def MyExtra():
    userID = '1031101' #TODO需要从登录信息获取
    sql = 'select content, semester, bonusValue from bonusItem2user as t1,bonusItem as t2 where ownerId={} and t1.bonusItemID=t2.bonusItemID'.format(userID)
    cursor.execute(sql)
    items = cursor.fetchall()
    columns = ["项目内容", "分数","第1/2学期"]
    dic = { #dict中key应和columns一致
        "项目内容": [],
        "分数": [],
        "第1/2学期": [],
    }
    for item in items:
        dic['项目内容'].append(item[0])
        dic['分数'].append(item[1])
        dic['第1/2学期'].append(item[2])
    df = pd.DataFrame(data=dic, columns=columns)
    convert = df.to_html(classes='table table-striped table-hover table-sm table-borderless',
                            border=None, justify=None)
    return render_template('student/MyExtra.html',table = convert)

#我的综合积分界面（雷达）
@app.route('/student/MyComprehensiveEval')
def MyComprehensiveEval():
    userID = '1031101' #TODO需要从登录信息获取
    sql = 'select moralScore,intellectualScore,socialScore,bonus from evaluationFinalScore where userId={}'.format(userID)
    cursor.execute(sql)
    scores = cursor.fetchall()
    return render_template('student/MyComprehensiveEval.html', score=list(scores[0]),name=userID)

#综合积分汇总界面（表格）#TODO增加排序功能 #TODO修正表格编号方式
@app.route('/student/TotalComprehensiveEval')
def TotalComprehensiveEval():
    userID = '1031101' #TODO需要从登录信息获取
    sql = 'select grade, departId from EvaluationFinalScore where userId={}'.format(userID)
    cursor.execute(sql)
    content = cursor.fetchall()
    grade = content[0][0]
    depart = content[0][1]
    #使用user表必须使用[user]才不会报错
    sql = 'select userName,moralScore,intellectualScore,socialScore,bonus,finalScore from [EvaluationFinalScore],[user] where grade={} and departId={} and EvaluationFinalScore.userId=[user].userID'.format(grade,depart)
    cursor.execute(sql)
    all_data = cursor.fetchall()
    columns = ["姓名", "德育", "智育", "体育", "附加分", "总分"]
    dic = { #dict中key应和columns一致
        "姓名": [],
        "德育": [],
        "智育": [],
        "体育": [],
        "附加分": [],
        "总分": []
    }
    for item in all_data:
        dic['姓名'].append(item[0])
        dic['德育'].append(item[1])
        dic['智育'].append(item[2])
        dic['体育'].append(item[3])
        dic['附加分'].append(item[4])
        dic['总分'].append(item[5])
    df = pd.DataFrame(data=dic, columns=columns)
    convert = df.to_html(classes='table table-striped table-hover table-sm table-borderless',
                            border=None, justify=None)
    return render_template('student/MyExtra.html',table = convert)


if __name__ == '__main__':
    app.run()

#以下为原代码，参考这些
# @app.route('/')
# def index():
#     return render_template('index.html')


# @app.route('/radar')
# def radar():
#     id = "201611580516"
#     with open('data/info.json', encoding='utf-8') as json_file:
#         data = json.load(json_file)
#     score = data[id]["score"]
#     name = data[id]["name"]
#     return render_template('radar.html', score=score, name=name)


# @app.route('/radar')
# def radar():
#     id = "201611580516"
#     with open('data/info.json', encoding='utf-8') as json_file:
#         data = json.load(json_file)
#     score = data[id]["score"]
#     name = data[id]["name"]
#     return render_template('radar.html', score=score, name=name)

# @app.route('/radar_search', methods=['GET', 'POST'])
# def radar_search():
#     form = NameForm()
#     score = None
#     name = None
    
#     if form.validate_on_submit():
#         session['id'] = form.id.data
#         return redirect(url_for('radar_search'))
#         #form.id.data = ''
    
#     id = session.get('id')
#     with open('data/info.json', encoding='utf-8') as json_file:
# 	    data = json.load(json_file)
#     #EG
    
#     if (data.get(id)):
#         score = data.get(id)["score"]
#         name  = data.get(id)["name"]
#     return render_template('radar_search.html',form = form,score = score,name = name)

# @app.route('/zhexian')
# def zhexian():
#     A_data = [3.17, 3.75, 3.21, 3.46, 3.43, 3.31, 3.08, 3.61]
#     B_data = [3.1, 3.00, 3.38, 3.01, 3.52, 3.87, 3.37, 3.85]
#     return render_template('student/zhexian.html', A_data=A_data, B_data=B_data)


# @app.route('/pie')
# def pie():
#     return render_template('pie.html')

# @app.route('/column')
# def column():
#     dataz=[2,4,6,10,8]
#     return render_template('column.html',data=dataz)

# @app.route('/table')
# def table():
#     data = open('data/16cs1.json', encoding='utf8').read()
#     columns = ["学号", "高数1","高数2","线性代数"]
#     dat = json.loads(data)
#     dic = { #dict中key应和columns一致
#         "学号": [],
#         "高数1": [],
#         "高数2": [],
#         "线性代数": []
#     }
#     for stu in dat['2016CS1']:
#         dic['学号'].append(stu)
#         dic['高数1'].append(dat['2016CS1'][stu]['3250300106'])
#         dic['高数2'].append(dat['2016CS1'][stu]['3250300204'])
#         dic['线性代数'].append(dat['2016CS1'][stu]['3250300303'])
#     df = pd.DataFrame(data=dic, columns=columns)
#     convert = df.to_html(classes='table table-striped table-hover table-sm table-borderless',
#                             border=None, justify=None)

#     # data = open('data/data.json', encoding='utf8').read()
#     # columns = ["stuid", "name", "classid", "grade"]
#     # dat = json.loads(data)
#     # dic = {
#     #     "stuid": [],
#     #     "name": [],
#     #     "classid": [],
#     #     "grade": []
#     # }
#     # for stu in dat:
#     #     dic['stuid'].append(stu['stuid'])
#     #     dic['name'].append(stu[u'name'])
#     #     dic['classid'].append(stu['classid'])
#     #     dic['grade'].append(stu['grade'])
   
#     return render_template('student/table.html',table = convert)


# @app.route("/search", methods=['GET', 'POST'])
# def search():
#     if request.method == 'GET':
#         return render_template('search.html',
#                                sid1_name = None,
#                                sid2_name = None,
#                                sid1_score = None,
#                                sid2_score = None)
#     else:
#         sid1 = request.form.get('sid1')
#         sid2 = request.form.get('sid2')
#         with open('data/info.json', encoding='utf-8') as json_file:
#             data = json.load(json_file)
#         sid1_name = data[sid1]["name"]
#         sid2_name = data[sid2]["name"]
#         sid1_score = data[sid1]["com_score"]
#         sid2_score = data[sid2]["com_score"]
#         return render_template('search.html',
#                                sid1_name = sid1_name,
#                                sid2_name = sid2_name,
#                                sid1_score = sid1_score,
#                                sid2_score = sid2_score)




