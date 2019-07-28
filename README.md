# VisualZHJF

#### 运行环境
- python 3.6.3
- flask 0.12.2

#### 目录结构
│    
└─VisualZHJF    # 主目录  
    │  config.py    # 默认配置文件  
    （里面有数据库的配置，和登录有关，但我不懂···而且mySQL-python 没装上）  
    │  run.py        # 启动文件 **<-运行这个预览**  
    │  manage.py     #不知道干嘛的  
    |  exts.py       #不知道干嘛的  
    |  models.py     #不知道干嘛的     
    ├─data        # 造的数据（改为使用数据库）  
    │  info.json  
       16cs1.json  
       16cs2.json  
       17cs1.json  
       17cs2.json  
    ├─static        # 静态文件  
    │  │    
    │  ├─css  
    │  │      base.css  
              index.css  
    │  ├─fonts  
    │  │        
    │  ├─image  
    │  │      logo.jpg #之后还要换  
    │  │        
    │  └─js  
    │            
    └─templates  
       |
       ├─student #学生界面
              base.html #界面模板（需补充最上方用户信息栏）  
              index.html #学生界面首页（界面内容待更改）  
              GradeByAttri.html #个人成绩 按照课程属性分类  
              GradeBySemester.html #个人成绩 按照学期分类  
              GPACalculator.html #GPA查询  
              GPATrend.html #GPA走向  
              MyExtra.html #我的附加分  
              MyComprehensiveEval.html #我的综合积分  
              TotalComprehensiveEval.html #综合积分汇总  
       ├─teacher #辅导员界面

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

- [ ] 页面布局  
  - 设计

  - 组件

  - 跳转
- [ ] 登录 
- [ ] 图表布局
  - 四项分数+总分
  - 姓名
  - 登录学号->获取个人信息 我不会rr 

