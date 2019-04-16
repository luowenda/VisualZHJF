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
    ├─data        # 造的数据  
    │  info.json  
       data.json  # table数据  
       16cs1.json  
       16cs2.json  
       17cs1.json  
       17cs2.json  
    ├─static        # 静态文件  
    │  │    
    │  ├─css  
    │  │      base.css  
    │  ├─fonts  
    │  │        
    │  ├─image  
    │  │      logo.jpg #之后还要换  
    │  │        
    │  └─js  
    │            
    └─templates 
            base.html  
            index.html   
            radar.html  
            table.html  
            zhexian.html  
            radar_search.html #查找学号匹配  
            404.html  
            500.html  

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

