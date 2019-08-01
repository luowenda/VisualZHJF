from flask import Flask, render_template, request
import pymssql
import json
import numpy as np
import pandas as pd
global userID
userID=0
conn=pymssql.connect(
        server='172.16.108.153',
        #host='.',
		user=r'sa',password='123456',database='zhjfdemo1')
cursor=conn.cursor()
app = Flask(__name__)

@app.route('/',methods=['get'])
def welcome():
	return render_template('welcome.html')

@app.route('/', methods = ['POST'])
def login():
	global userID 
	userID = request.form['username']
	pwd = request.form['passwd']
	'''
	conn=pymssql.connect(
        server='172.16.108.153',
        #host='.',
		user=r'sa',password='123456',database='zhjfdemo1')
	cursor=conn.cursor()
	'''
	sql1 = "select userID from dbo.[user] where userID='"+userID+"' and password='"+pwd+"'"
	sql2 = "select roleid from dbo.userrolemapping where userID ='"+userID+"'"
	cursor.execute(sql1)
	#用一个rs_***变量获取数据
	rs_userid = cursor.fetchall()
	num=0
	for data in rs_userid:
		num=num+1
	if(num!=0):
		cursor.execute(sql2)
		rs_roleid= cursor.fetchone()
		roleID=rs_roleid[0]
		if(roleID==1):
			return stu_index()
		else:
			return '你是老师'
	else:
			return '登陆失败'

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
    return render_template('student/GPACalculator.html')

#查看GPA走向界面（折线）
@app.route('/student/GPATrend')
def GPATrend():
    A_data = [3.17, 3.75, 3.21, 3.46, 3.43, 3.31, 3.08, 3.61]
    B_data = [3.1, 3.00, 3.38, 3.01, 3.52, 3.87, 3.37, 3.85]
    return render_template('student/GPATrend.html', A_data=A_data, B_data=B_data)

#我的综合积分界面（雷达）
@app.route('/student/MyComprehensiveEval')
def MyComprehensiveEval():
    #userID = '1031101' #TODO需要从登录信息获取
    sql = 'select moralScore,intellectualScore,socialScore,bonus from evaluationFinalScore where userId={}'.format(userID)
    cursor.execute(sql)
    scores = cursor.fetchall()
    return render_template('student/MyComprehensiveEval.html', score=list(scores[0]),name=userID)

#我的附加分界面（表格）#TODO修正表格编号方式
@app.route('/student/MyExtra')
def MyExtra():
    #userID = '1031101' #TODO需要从登录信息获取
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

	#综合积分汇总界面（表格）#TODO增加排序功能 #TODO修正表格编号方式
@app.route('/student/TotalComprehensiveEval')
def TotalComprehensiveEval():
    #userID = '1031101' #TODO需要从登录信息获取
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
 
