import requests
import re
import json
import math
import time
import random

def get_sso_cookie(username: str, password: str):
    session = requests.Session()
    session.headers.update({
        "User-Agent": "Mozilla/5.0"
    })

    try:
        # Step 1: 获取登录页面，提取 execution 值
        resp = session.get('https://zjuam.zju.edu.cn/cas/login', timeout=8, allow_redirects=False)
        execution_match = re.search(r'name="execution" value="(.*?)"', resp.text)
        if not execution_match:
            raise "无法获取execution"
        execution = execution_match.group(1)

        # Step 2: 获取 RSA 公钥
        pubkey_resp = session.get('https://zjuam.zju.edu.cn/cas/v2/getPubKey', timeout=8)
        pubkey_json = pubkey_resp.json()
        modulus_str = pubkey_json.get("modulus")
        exponent_str = pubkey_json.get("exponent")
        if not modulus_str or not exponent_str:
            raise "无法获取RSA公钥"

        # Step 3: 执行 RSA 加密
        try:
            mod_int = int(modulus_str, 16)
            exp_int = int(exponent_str, 16)
            pwd_bytes = password.encode("utf-8")
            pwd_int = int(pwd_bytes.hex(), 16)
            pwd_enc_int = pow(pwd_int, exp_int, mod_int)
            pwd_enc = format(pwd_enc_int, 'x').zfill(128)
        except Exception:
            raise "密码不合法"

        # Step 4: 提交登录表单
        data = {
            "username": username,
            "password": pwd_enc,
            "execution": execution,
            "_eventId": "submit",
            "rememberMe": "true"
        }
        headers = {
            "Content-Type": "application/x-www-form-urlencoded; charset=utf-8"
        }
        login_resp = session.post(
            'https://zjuam.zju.edu.cn/cas/login',
            data=data,
            headers=headers,
            timeout=8,
            allow_redirects=False
        )

        # Step 5: 检查是否登录成功（是否有 iPlanetDirectoryPro Cookie）
        for cookie in session.cookies:
            if cookie.name == "iPlanetDirectoryPro":
                return cookie

        raise "学号或密码错误"

    except requests.exceptions.Timeout:
        raise "请求超时"
    except requests.exceptions.RequestException:
        raise "网络错误"

def login(iPlanetDirectoryPro) -> bool:
    if iPlanetDirectoryPro is None:
        raise "iPlanetDirectoryPro无效"

    session = requests.Session()
    session.headers.update({"User-Agent": "Mozilla/5.0"})

    # 设置 iPlanetDirectoryPro cookie
    session.cookies.set(
        name=iPlanetDirectoryPro.name,
        value=iPlanetDirectoryPro.value,
        domain="zjuam.zju.edu.cn"
    )

    try:
        # Step 1: 访问 login 接口获取 st ticket
        url = "https://zjuam.zju.edu.cn/cas/login?service=http%3A%2F%2Fzdbk.zju.edu.cn%2Fjwglxt%2Fxtgl%2Flogin_ssologin.html"
        resp = session.get(url, timeout=8, allow_redirects=False)

        # 获取跳转地址
        st_location = resp.headers.get("Location")
        if not st_location:
            raise "iPlanetDirectoryPro无效"

        if st_location.startswith("http://"):
            st_location = st_location.replace("http://", "https://")

        # Step 2: 跟随跳转
        resp2 = session.get(st_location, timeout=8, allow_redirects=False)

        # 检查 cookies
        global jsessionid, route
        jsessionid = None
        route = None
        for cookie in session.cookies:
            if cookie.name == "JSESSIONID" and cookie.path == "/jwglxt":
                jsessionid = cookie.value
            elif cookie.name == "route":
                route = cookie.value

        if not jsessionid:
            raise "无法获取JSESSIONID"
        if not route:
            raise "无法获取route"

        return True

    except requests.exceptions.Timeout:
        raise "请求超时"
    except requests.exceptions.RequestException:
        raise "网络错误"


def query_grades():
    if jsessionid is None or route is None:
        raise "未登录"

    session = requests.Session()
    session.headers.update({
        "User-Agent": "Mozilla/5.0"
    })

    # 设置 cookies
    session.cookies.set("JSESSIONID", jsessionid, domain="zdbk.zju.edu.cn", path="/jwglxt")
    session.cookies.set("route", route, domain="zdbk.zju.edu.cn")

    try:
        url = (
            "https://zdbk.zju.edu.cn/jwglxt/cxdy/xscjcx_cxXscjIndex.html"
            "?doType=query&queryModel.showCount=5000"
        )
        response = session.post(url, timeout=8, allow_redirects=False)

        return response

    except requests.exceptions.Timeout:
        raise "请求超时"
    except requests.exceptions.RequestException:
        raise "网络错误"
            
            
def update_score(new_score, url):
    try:
        with open("dingscore.json", 'r', encoding="utf-8") as load_f:
            userscore = json.load(load_f)
    except json.decoder.JSONDecodeError:
        userscore = {}
    except FileNotFoundError:
        userscore = {}

    totcredits = 0
    totgp = 0
    for lesson in userscore:
        if userscore[lesson]['score'] in ['合格', '不合格', '弃修']:
            continue
        totgp += float(userscore[lesson]['gp']) * float(userscore[lesson]['credit'])
        totcredits += float(userscore[lesson]['credit'])
    try:
        gpa = totgp / totcredits
    except:
        gpa = 0

    #对比以更新
    for lesson in new_score:
        id = lesson['xkkh']
        name = lesson['kcmc']
        score = lesson['cj']
        credit = lesson['xf']
        gp = lesson['jd']
        if id == '选课课号':
            continue
        if userscore.get(id) != None:
            continue
        
        #新的成绩更新
        userscore[id] = {
            'name': name,
            'score': score,
            'credit': credit,
            'gp': gp
        }
        newtotcredits = 0
        newtotgp = 0
        for lesson in userscore:
            if userscore[lesson]['score'] in ['合格', '不合格', '弃修']:
                continue
            newtotgp += float(userscore[lesson]['gp']) * float(userscore[lesson]['credit'])
            newtotcredits += float(userscore[lesson]['credit'])
        try:
            newgpa = newtotgp / newtotcredits
        except:
            newgpa = 0
        
        #钉钉推送消息
        try:
            requests.post(url=url, json={
                "msgtype": "markdown",
                "markdown" : {
                    "title": "考试成绩通知",
                    "text": """
### 考试成绩通知\n
- **选课课号**\t%s\n
- **课程名称**\t%s\n
- **成绩**\t%s\n
- **学分**\t%s\n
- **绩点**\t%s\n
- **成绩变化**\t%.2f(%+.2f) / %.1f(%+.1f)""" % (id, name, score, credit, gp, newgpa, newgpa - gpa, newtotcredits, newtotcredits - totcredits)
                }
            })
        except requests.exceptions.MissingSchema:
            print('The DingTalk Webhook URL is invalid. Please use -d [DingWebhook] to reset it first.')
        
        print('考试成绩通知\n选课课号\t%s\n课程名称\t%s\n成绩\t%s\n学分\t%s\n绩点\t%s\n成绩变化\t%.2f(%+.2f) / %.1f(%+.1f)' % (id, name, score, credit, gp, newgpa, newgpa - gpa, newtotcredits, newtotcredits - totcredits))
        totcredits = newtotcredits
        totgp = newtotgp
        gpa = newgpa

    #保存新的数据
    with open("dingscore.json", 'w', encoding="utf-8") as load_f:
        load_f.write(json.dumps(userscore, indent=4, ensure_ascii=False))
            
def scorenotification():
    with open('database.json', 'r') as f:
        userdata = json.load(f)
    username = userdata['username']
    password = userdata['password']
    url = userdata.get('url', 'https://oapi.dingtalk.com/robot/send?access_token=')

    iPlanetDirectoryPro = get_sso_cookie(username, password)
    
    login(iPlanetDirectoryPro)
    
    new_score = query_grades().json()['items']

    update_score(new_score, url)
    
if __name__ == "__main__":
    while True:
        try:
            scorenotification()
        except Exception as e:
            print(f"发生错误: {e}")

        time.sleep(random.randint(60, 300))  # 随机延时1到5秒
