# king of knowledge

This is a program to compete knowledge by two teams

Since the problem is all localized in Simplified Chinese, the following `README.md` is localized in the same language, too.

# 基于Tornado框架的头脑王者

你可以使用这个项目完成一个简单的头脑王者平台的搭建，可以在晚会的时候作为一个娱乐节目。

我已经提供了一个sqlite5的数据库，里面约有1000+的题目，可以Clone后直接使用。

# 安装

## Python 3.5

## 库

+ tornado
+ sqlalchemy
+ pandas (仅在自行导入数据时使用，如果你不需要导入自己的数据，可以不适应)
+ numpy (仅在自行导入数据时使用)

# 自行导入数据

你可以参考`import_from_csv`和`import_question`两个文件来导入你的数据

# 运行

```shell
cd <克隆/下载的文件夹目录>
python/python3 brain_pk.py
```

作为主持人，你可以使用浏览器打开`<运行此项目的电脑所在的ip地址>:8888/host`

你需要选择两个比赛选手，分别用浏览器打开'<运行此项目的电脑所在的ip地址>:8888/team/A'及'<运行此项目的电脑所在的ip地址>:8888/team/B'

然后等到登陆完成后，主持人界面点击新一题就可以开始比赛了，置零就会清空积分信息，点击新一题后，两只队伍的置零信息将会被发送

# 开源协议

MIT 协议



