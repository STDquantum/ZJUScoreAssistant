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
