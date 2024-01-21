# 程序更新啦，不用手动复制了，会自动保存到一个文件里
# 嘿大家好，这是我自己写的一个可以提示新的【绩点】的 python 程序（目前已知适用于windows）
# 原理就是模仿登录查成绩的网站，然后用正则表达式搞到所有信息
# 目前是获取所有上过课的成绩
# 使用方法如下：
#   1. 下载 python
#   2. win+R，输入 cmd 回车，然后输入 pip install playwright
#   3. 然后输入 playwright install chrome
#   4. 把这条朵朵全文复制到一个 python 文件里，保存（似乎朵朵会吞掉空格，我在评论区放一个链接）
#   5. 修改 xuehao 和 mima 两个变量为自己登陆浙大通行证用的账号密码
#   6. 以文件的形式运行，如果出了新的绩点会弹窗提示，一直让它在那运行着就好，一分钟访问一次
#   7. 运行窗口会显示一个列表，里面有这节课的各种信息，文件会保存一个scores.txt的文件在同目录下，不用手动复制辽~再次打开时也是可以直接读取这个文件的~
#   8. 运行窗口什么都没有是正常情况，有新的会提示，没有就会静默，如果出现类似playwright._impl._api_types.TimeoutError: Timeout 30000ms exceeded.
# =========================== logs ===========================
# waiting for get_by_role("button", name="查询")
#       的报错，关掉重新运行就好了（可能是网不好或者服务器卡了）

xuehao = ""  # 这里改学号
mima = ""  # 这里改密码
dingTalkWebHook = ""  # 粘贴钉钉机器人的 webhook
xuenian = "2023-2024"
scores = []

import asyncio
from playwright.async_api import Playwright, async_playwright
import time
import re
import json
import requests


def sendToDingTalk(score, totalXueFen, totalJiDian, totalBaifen):
    try:
        requests.post(
            url=dingTalkWebHook,
            json={
                "msgtype": "markdown",
                "markdown": {
                    "title": "考试成绩通知",
                    "text": f"## 考试成绩通知\n\n- **选课课号**\t{score[0]}\n\n- **课程名称**\t{score[1]}\n\n- **成绩**\t{score[2]}\n\n- **学分**\t{score[3]}\n\n- **绩点**\t{score[4]}\n\n- **学年总学分**\t{totalXueFen}\n\n- **学年均绩**\t{totalJiDian / totalXueFen : .2f}\n\n- **学年百分制均分**\t{totalBaifen / totalXueFen : .2f}",
                },
            },
        )
    except:
        print("钉钉成绩发送失败")


async def run(playwright: Playwright) -> None:
    browser = await playwright.chromium.launch(headless=True)
    context = await browser.new_context()
    page = await context.new_page()
    await page.goto(
        "https://zjuam.zju.edu.cn/cas/login?service=http%3A%2F%2Fappservice.zju.edu.cn%2Fzdjw%2Fcjcx%2Fcjcxjg"
    )
    await page.get_by_placeholder("职工号/学号/手机号码/邮箱/别名").click()
    await page.get_by_placeholder("职工号/学号/手机号码/邮箱/别名").fill(xuehao)
    await page.get_by_placeholder("职工号/学号/手机号码/邮箱/别名").press("Tab")
    await page.get_by_role("textbox", name="输入密码").fill(mima)
    await page.get_by_role("textbox", name="输入密码").press("Enter")
    time.sleep(4)
    con = await page.content()
    r = re.findall(
        r'kcmc">(.+?)</d.+?学分：([0-9\.]+).+?学年：([0-9-\.]+).+?学期：(.+?)</p.+?绩点：([0-9\.]+).+?ccj">(\w+)',
        con,
    )

    # ---------------------
    await context.close()
    await browser.close()

    return r


def printf():  # 把新的列表打印到 scores.txt
    s = "["
    for score in scores:
        s += str(score) + ",\n"
    s = s[:-2] + "]"
    s = s.replace("'", '"')
    open("scores-浙大钉.txt", "w", encoding="utf-8").write(s)


async def main():
    global scores
    try:
        scores = json.load(open("scores-浙大钉.txt", "r", encoding="utf-8"))
    except:
        scores = []
    try:
        with open("counter.txt", "r", encoding="utf-8") as f:
            times = int(f.read())
    except:
        times = 0
    while True:
        times += 1
        print(
            time.strftime("%m-%d %H:%M:%S", time.localtime()), f"第 {times} 次运行", end="，"
        )
        try:
            async with async_playwright() as playwright:
                newScores = await run(playwright)
                tmp = ["秋", "冬", "秋冬", "春", "夏", "春夏", "短"]
                newScores.sort(key=lambda x: tmp.index(x[3]))
                newScores.sort(key=lambda x: int(x[2].split("-")[0]))
                newScores = [list(i) for i in newScores]
        except:
            print("不正常运行，出现错误，一分钟后重试")
            with open("counter.txt", "w", encoding="utf-8") as f:
                f.write(str(times))
            time.sleep(60)
            continue
        for score in newScores:
            if score in scores:
                continue
            if score[5] in ["弃修", "合格", "不合格"]:
                scores.append(score)
                printf()
                print(score)
                continue
            if xuenian != score[2]:
                scores.append(score)
                printf()
                print(score)
                continue
            if score not in scores:
                scores.append(score)
                printf()
                print(score)
                totalXueFen, totalJiDian, totalBaifen = 0, 0, 0
                for s in scores:
                    if xuenian != s[2]:
                        continue
                    totalXueFen += float(s[1])
                    totalJiDian += float(s[4]) * float(s[1])
                    totalBaifen += float(s[5]) * float(s[1])

                sendToDingTalk(score, totalXueFen, totalJiDian, totalBaifen)
                print(
                    f"总学分: {totalXueFen : .1f}, 均绩: {totalJiDian / totalXueFen : .3f}"
                )
                # os.system(f'mshta vbscript:msgbox("科目：{s[0]}, 绩点：{s[4]}, 百分制：{s[5]}")(window.close)')
        else:
            print("正常运行，没有新绩点")

        with open("counter.txt", "w", encoding="utf-8") as f:
            f.write(str(times))

        time.sleep(60)

def scorenotification():
    d = json.load(open("database.json", "r", encoding="utf-8"))
    global xuehao, mima, dingTalkWebHook
    xuehao, mima, dingTalkWebHook = d["username"], d["password"], d["url"]
    asyncio.run(main())

if __name__ == "__main__":
    scorenotification()