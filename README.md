# ZJUScoreAssistant

https://github.com/PeiPei233/ZJUScoreAssistant 的个人修改版，结合了去年写的用 playwright 的脚本。

## 下载

```
git clone https://github.com/STDquantum/ZJUScoreAssistant
```

或者直接下载 zip。

## 使用

### 登录

```
python zjuscore.py -i
```

然后按照提示输学号密码就行，密码不显示是正常的。

### 更新

```
python zjuscore.py -u
```

就能更新绩点，更新后的在 `userscore.json`。

### 钉钉提醒和持续更新（不填 dingtalkwebhook 的话就是持续更新）

```
python zjuscore.py -d https://oapi.dingtalk.com/robot/send?access_token=...
```

后面网址换成你自己的钉钉机器人 WebHook。

使用方法如下：

钉钉搜索“新手体验群”，没有就自己建一个好了；依次打开“群设置”-“机器人”-“添加机器人”-“自定义”-（名字随便取）-“安全设置-自定义关键词-成绩”-“我已阅读并同意……”-“完成”-“复制”-“粘贴到dingTalkWebHook”

然后

```
python zjuscore.py -dn
```

就可以一直跑了，会有充足的提示。

注意：第一次运行的时候钉钉没有发全是正常现象。因为会限制一次发送的条数，只要脚本继续跑着后面都是正常的。

### 看看你在TOP3高校都什么水平（先起码跑过一遍 `-u` 或者 `-dn`）

```
python 算算你在TOP3的绩点会是多少.py
```

结果如下：

```
学年: 2022-2023
你在ZJU的绩点为  5.00, 你在FDU的绩点为  4.00, 你在SJTU的绩点为  4.30, 你在USTC的绩点为  4.30, 你在NJU的绩点为  5.00,

学年: 2023-2024
你在ZJU的绩点为  5.00, 你在FDU的绩点为  4.00, 你在SJTU的绩点为  4.30, 你在USTC的绩点为  4.30, 你在NJU的绩点为  5.00,

学年: 全部
你在ZJU的绩点为  5.00, 你在FDU的绩点为  4.00, 你在SJTU的绩点为  4.30, 你在USTC的绩点为  4.30, 你在NJU的绩点为  5.00,
```

### 查看成绩

```
python zjuscore.py -ls
```

可以显示所有的课程绩点。（前提是你运行过上面的 `-u` 过）

```
python zjuscore.py -ls 2023
```

可以显示 2023-2024 学年的绩点。（显示 2022-2023 学年的要用 `-ls 2022`）

```
python zjuscore.py -ls 2023 秋冬
```

可以显示 2023-2024 学年秋、冬、秋冬学期的课程绩点。（因为用的是模糊匹配，如果只有 `-ls 2023 春` 的话就是只有春学期的）

### 查看均绩 GPA

```
python zjuscore.py -g
```

可以显示所有课程均绩。

```
python zjuscore.py -g 2023
```

可以显示 2023-2024 学年的均绩。（显示 2022-2023 学年的要用 `-g 2022`）

```
python zjuscore.py -g 2023 秋冬
```

可以显示 2023-2024 学年秋、冬、秋冬学期的课程均绩。（因为用的是模糊匹配，如果只有 `-g 2023 春` 的话就是只有春学期的）

### 搜索课程

```
python zjuscore.py -n 微积分 工图
```

就能显示如下

```
Semeter         Name                    Mark    GP      Credit
2022-2023 春夏  微积分Ⅱ（H）            100      5.0     5.0
2022-2023 秋冬  微积分Ⅰ（H）            100      5.0     5.0
2022-2023 夏    常微分方程              100      5.0     1.0
2022-2023 秋冬  工程图学（H）           100      5.0     2.5
2022-2023 春夏  工程训练                100      5.0     1.5
```

由于是模糊匹配，所以会有常微分方程这种课。但无所谓，反正起到搜索的作用了。

### 

### 三十三

### Get Help

Use `-h` or `--help` to get help.

```powershell
PS > python zjuscore.py -h
usage: zjuscore.py [-h] [-i] [-u] [-ls [YEAR [SEMESTER ...]]] [-n NAME [NAME ...]]
                   [-g [YEAR [SEMESTER ...]]] [-d [DingWebhook]] [-dn]

ZJU Score Assistant

options:
  -h, --help            show this help message and exit
  -i, --initial         initialize your information
  -u, --update          update the course score
  -ls [YEAR [SEMESTER ...]], --list [YEAR [SEMESTER ...]]
                        list the course and score in a certain year/semester
  -n NAME [NAME ...], --name NAME [NAME ...]
                        search score by the name of the course
  -g [YEAR [SEMESTER ...]], --gpa [YEAR [SEMESTER ...]]
                        calculator the gpa
  -d [DingWebhook], --ding [DingWebhook]
                        set your DingTalk Robot Webhook. Empty means disabled
  -dn, --dnotification  enable dingtalk score notification
```

### Initialize the Score Assistant

You need to log in to get your score information, so it is necessary to let the assistant to know your username (usually your student ID) and password. You can use `-i` or `--initial` to initialize. Then the program will ask for your information and automatically verify your username and password. Your information will be saved on your computer.

```powershell
PS > python zjuscore.py -i
ZJUAM account's username: 3200106666
ZJUAM 3200106666's password: 
Error: Invalid username or password. Please check them again and use -i to reset them.

PS > python zjuscore.py -i
ZJUAM account's username: 3200106666
ZJUAM 3200106666's password: 
Done: Initial Success!
```

### Update the Score on your Computer

You can use the argument `-u` or `--update` to update the score information stord on your computer. This operation is used to avoid wasting time by having to get your information every time you use the program. 

```powershell
PS > python zjuscore.py -u
Updated Success!
```

### Score Query

Use `-ls` or `--list` to query your score. It supports the following three ways to use it:

- `python zjuscore.py -ls` can query all your score information during college.
- `python zjuscore.py -ls <ACADEMIC YEAR>` can query your information during a certain academic year. You can replace `<ACADEMIC YEAR>` with `2021` or `2021-2022` to query all your courses' score in the 2021-2022 academic year.
- `python zjuscore.py -ls <ACADEMIC YEAR> <SEMESTER>` can query your score information during a certain semester. You can replace `<ACADEMIC YEAR>` with `2021` or `2021-2022`, and replace `<SEMESTER>` with `春` `夏` `秋` `冬` or `春夏` `秋冬` and so on, to query all the grades of courses in a certain semester of 2021-2022 academic year.

For example:
```powershell
PS > python zjuscore.py -ls
Semeter         Name                    Mark    GP      Credit
2021-2022 春夏  离散数学及其应用           60      1.5     4.0
2021-2022 夏    社会主义发展史            79      3.3     1.5
......

PS > python zjuscore.py -ls 2021
Semeter         Name                    Mark    GP      Credit
2021-2022 春夏  离散数学及其应用           60      1.5     4.0
......

PS > python zjuscore.py -ls 2021 夏
Semeter         Name                    Mark    GP      Credit
2021-2022 夏    社会主义发展史             79      3.3     1.5
```

In addition, you can use `-n` or `--name` to search for score information, the name of which matching the course name in the following argument(s).

```powershell
PS > python zjuscore.py -n 离散
Semeter         Name                    Mark    GP      Credit
2021-2022 春夏  离散数学及其应用           60      1.5     4.0

PS > python zjuscore.py -n 微寄分 大物
Semeter         Name                    Mark    GP      Credit
2021-2022 春夏  微积分（甲）Ⅱ             80      3.3     5.0
2021-2022 秋冬  微积分（甲）Ⅰ             80      3.3     5.0
2021-2022 春夏  大学物理（乙）Ⅰ           80      3.3     3.0

PS > python zjuscore.py --name 汇编
Cannot find any course matching keyword(s) 汇编
```

### Calculate GPA

Use `-g` or `--gpa` to obtain your GPA of a certain period. The argument(s) and usage of this is consistent with those of `-ls`.

```powershell
PS > python zjuscore.py -g     
Your GPA during the whole college is 3.95

PS > python zjuscore.py -g 2021
Your GPA during the academic year of 2021-2022 is 3.95

PS > python zjuscore.py -g 2021 夏
Your GPA during the semester of 2021-2022 夏 is 3.90
```

### Score Update Notification

Before running the notification assistant, you should use `-d` or `--ding` to set the URL of DingTalk Robot.

- `python zjuscore.py -d https://oapi.dingtalk.com/robot/send?access_token=xxxxxxxxxx` Set the URL of dingtalk robot webhook.
- `python zjuscore.py -d` Reset the URL of dingtalk robot webhook. This means that you can unable the notification assistant in dingtalk.

You should configure your Dingtalk Robot first to get the URL. You can follow the following steps:

1. Add custom robot.
2. In the robot security setting, just add `成绩` to the custom keyword. You can customized your robot's photo and name like the following examples.
3. Copy the webhook URL provided by the robot and use `-d` to tell the notificaiton assistant mentioned above.

After that, use `python zjuscore.py -dn` or `python zjuscore.py -dnotification` to enable the score update notification. The application will run continuously and synchronize your score from ZJU every 1 to 5 minutes and inform you the updated information by DingTalk Robot.

Once there is an updated information, your dingtalk robot will push the following information automatically:

![](./screenshot/notification.jpg)

![](./screenshot/dingtalkrobot.jpg)

**NOTICE** For a better experience, it is recommended that you put this application on the server when you use notification assistant.

### Arguments Combination

Use the mutiple combination of arguments to simplied the use process. For example:

- Run `python zjuscore.py -i -u -g` to initialize and obtain your GPA.
- Run `python zjuscore.py -i -d https://oapi.dingtalk.com/robot/send?access_token=xxxxxxxxxx -dn` to initialize and enable the notification assistant.
- Run `python zjuscore.py -u -n xxx` `python zjuscore.py -u -ls` or `python zjuscore.py -u -ls` to make the assistant resynchronize your score information from ZJU every time you query the score information.
