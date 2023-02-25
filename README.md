# AttendanceStaticsAssistant
得力e+APP打卡时间统计助手，用于统计截止使用时刻，当周还需多少打卡时间
记录写代码过程中遇到的一些问题

从有想法到最终打包exe完成花费约两天时间，成品效果勉强能用

## 问题一：APP内部网址的抓取
由于得力e+APP隐藏了内部链接，所以通过模拟器+Fiddler抓包的方式得到考勤时间记录，做之前没想到这一步这么简单

## 问题二：动态网址数据的抓取
上一步中得到的网站是动态网站，因此之前用过的requests库抓不到要用的数据，换用selenium库抓取  
并用selenium的模拟点击功能顺带爬了上个月的数据，便于跨月周的计算（xpath定位元素可以直接从检查中导出）

## 问题三：网站具体数据解析
上一步得到了网站的全部源码，用beautifulsoup4解析匹配具体位置数据并记录

## 问题四：UI模块
没学过pyqt5，懒得学，做得很简陋

## 问题五：pyinstaller打包
一开始是打包缺模块，用venv解决，以免打包目录和pycharm目录不一致  
然后是运行会闪现命令行，修改了selenium的源代码，但是仍未完全解决  
打包的exe过大问题，新开一个venv只加入必要的模块，再加上UPX，将原来40+MB的exe优化到了30+MB（虽然还是很大）

## 效果图
![3SKDV3AS}J{X~ES_KP @I4X](https://user-images.githubusercontent.com/56437903/218032927-8516c6ca-603b-49d5-97c8-8511724a4fac.png)
# example
