# VisualZHJF

#### 运行环境
- python 3.6.3
- flask 0.12.2

#### 目录结构
│    
└─VisualZHJF    # 主目录  
    &emsp;│  config.py    # 默认配置文件  
    &emsp;│  run.py        # 启动文件 **<-运行这个预览**  
    &emsp;│  manage.py     #不知道干嘛的  
    &emsp;|  exts.py       #不知道干嘛的  
    &emsp;|  models.py     #不知道干嘛的     
    ├─data        # 造的数据（改为使用数据库）  
    │  info.json  
       &emsp;&emsp;16cs1.json  
       &emsp;&emsp;16cs2.json  
       &emsp;&emsp;17cs1.json  
       &emsp;&emsp;17cs2.json  
    ├─static        # 静态文件  
    │  │    
    │  ├─css  
          &emsp;&emsp;base.css  
          &emsp;&emsp;index.css  
    │  ├─fonts   
    │  ├─image  
    │  │      logo.jpg #之后还要换   
    │  └─js   
    └─templates  
       &emsp;&emsp;|  
       &emsp;&emsp;├─student #学生界面  
       &emsp;&emsp;|&emsp;&emsp;base.html #界面模板（需补充最上方用户信息栏）  
       &emsp;&emsp;|&emsp;&emsp;index.html #学生界面首页（界面内容待更改）  
       &emsp;&emsp;|&emsp;&emsp;GradeByAttri.html #个人成绩 按照课程属性分类  
       &emsp;&emsp;|&emsp;&emsp;GradeBySemester.html #个人成绩 按照学期分类  
       &emsp;&emsp;|&emsp;&emsp;GPACalculator.html #GPA查询  
       &emsp;&emsp;|&emsp;&emsp;GPATrend.html #GPA走向  
       &emsp;&emsp;|&emsp;&emsp;MyExtra.html #我的附加分  
       &emsp;&emsp;|&emsp;&emsp;MyComprehensiveEval.html #我的综合积分  
       &emsp;&emsp;|&emsp;&emsp;TotalComprehensiveEval.html #综合积分汇总  
       &emsp;&emsp;├─teacher #辅导员界面  
       &emsp;&emsp;|&emsp;&emsp;base.html #界面模板（需补充最上方用户信息栏）  
       &emsp;&emsp;|&emsp;&emsp;Bonus.html #个人查询-附加分统计    
       &emsp;&emsp;|&emsp;&emsp;ComByStu.html #多人（班级）比较-学生成绩  
       &emsp;&emsp;|&emsp;&emsp;ComByClass.html #多人（班级）比较-班级成绩对比  
       &emsp;&emsp;|&emsp;&emsp;ComByYear.html #多人（班级）比较-各届成绩对比   
       &emsp;&emsp;|&emsp;&emsp;CourseyOverview.html #课程总览  
       &emsp;&emsp;|&emsp;&emsp;FailedCourses.html #个人查询-挂科情况统计  
       &emsp;&emsp;|&emsp;&emsp;GradeTrend.html #个人查询-成绩走向  
       &emsp;&emsp;|&emsp;&emsp;index.html #首页  
       &emsp;&emsp;|&emsp;&emsp;MajorOverview.html #专业总览  
       
       

         404.html  
         500.html
         base.html  
         index.html   
         radar.html  
         table.html  
         zhexian.html  
         radar_search.html #查找学号匹配  
         search.html #对比学生GPA
         pie.html  
         column.html  

#### TODO 

**MajorOverview**  
- [ ] 下拉菜单CSS  
- [ ] 表格CSS  
- [ ] 设置选项session(选择后显示选项？)  

**CourseOverview**  
- [ ] 下拉菜单CSS  
- [ ] 整体CSS  
- [ ] 设置选项session  
- [ ] 显示请求查询内容  
- [ ] 专选课问题  

**GradeTrend**
- [ ] 连按两次查询按钮显示list index out of range  
- [ ] 整体CSS  
- [ ] 成绩走向？（目前之显示当前GPA）    