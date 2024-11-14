import hashlib
import requests
import json
import os

requests.packages.urllib3.disable_warnings()
requests = requests.Session()
requests.verify = False

secret = 'UppwYkfBlk'
msg = ''

def Log(cont=''):
    global msg
    print(cont)
    if cont:
        msg += cont + '\n'


def get_md5(string):
    return hashlib.md5((string).encode()).hexdigest()

def daily_checkin(username):
    cookies = {
        'SERVERID': '3310242e62b8cc41b4d3f4b22307d237|1728661431|1728661117',
    }
    url = f'action=user&app=hsywx&appkey=1079fb245839e765&merchant_id=2&method=qiandao&username={username}&version=2UppwYkfBlk'
    sign = get_md5(url)
    params = {
        'action': 'user',
        'app': 'hsywx',
        'appkey': '1079fb245839e765',
        'merchant_id': '2',
        'method': 'qiandao',
        'username': username,
        'version': '2',
        'sign': sign,
    }
    
    response = requests.get('https://www.52bjy.com/api/app/hsy.php', params=params, cookies=cookies)
    # print(response.json())
    msg = response.json().get('message', '')
    Log(msg)

if __name__ == '__main__':
    token = ''
    tkname = 'wsh_hsy'
    if not token:
        token = os.getenv(tkname)
        if not token:
            Log(f"⛔️请设置环境变量:{tkname}⛔️")
            exit()
    tokens = token.split("@") if "@" in token else (token, "")
    Log(f"一共获取到{len(tokens)}个账号")
    i = 1
    for token in tokens:
        Log(f"\n--------开始第{i}个账号--------")
        daily_checkin(token)
        Log(f"--------第{i}个账号结束--------\n")
        i += 1
    
    
        