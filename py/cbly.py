import requests
import json
import os

requests.packages.urllib3.disable_warnings()
requests = requests.Session()
requests.verify = False

msg = ''

def Log(cont=''):
    global msg
    print(cont)
    if cont:
        msg += cont + '\n'

class Run():
    def __init__(self, token):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Linux; Android 10; MI 8 Lite Build/QKQ1.190910.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/122.0.6261.120 Mobile Safari/537.36 XWEB/1220089 MMWEBSDK/20240404 MMWEBID/8150 MicroMessenger/8.0.49.2600(0x28003156) WeChat/arm64 Weixin NetType/WIFI Language/zh_CN ABI/arm64 MiniProgramEnv/android',
            'Accept-Encoding': 'gzip, compress, br, deflate',
            'authorization': token,
            'charset': 'utf-8',
            'content-type': 'application/json',
            'Referer': 'https://servicewechat.com/wx2206cca563f6f937/82/page-frame.html'
        }
    def sign_in(self):
        url = 'https://cbxcx.weinian.com.cn/wnuser/v1/memberUser/daySign'
        response = requests.post(url, headers=self.headers)
        result = response.json()
        if result.get('status') == 200:
            Log(f'签到成功【{result.get("msg")}】')
        else:
            Log(f'签到失败【{result.get("msg")}】')
            
    def check_sign_num(self):
        url = 'https://cbxcx.weinian.com.cn/wnuser/v1/memberUser/checkSignNum'
        response = requests.post(url, headers=self.headers)
        result = response.json()
        if '今日已校验' in result.get('data'):
            Log(f'今日已校验【{result.get("data")}】')
        else:
            Log(f'今日未校验【{result.get("data")}】')
            self.sign_in()
        
            
            

    def get_user_info(self):
        url = 'https://cbxcx.weinian.com.cn/wnuser/v1/memberUser/getMemberUser'
        response = requests.post(url, headers=self.headers)
        result = response.json()
        if result.get('status') == 200:
            Log(f'获取用户信息成功【{result.get("msg")}】')
            Log(f'用户名【{result.get("data").get("nickName")}】')
            
        else:
            Log(f'获取用户信息失败【{result.get("msg")}】')
            ckFlag = False
def start(token):
    sattus = True
    try:
        main = Run(token)
        main.get_user_info()
        main.check_sign_num()
        
    except Exception as e:
        Log(f'发生错误【{e}】')
        sattus = False
        return sattus
    return sattus
if __name__ == '__main__':
    token = 'BearereyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3Mjg4MTEwODgsInVzZXJfbmFtZSI6Im9mc0tCNUgwbnN0REhKcmRkcTdSai1KNXQwekEiLCJhdXRob3JpdGllcyI6WyJXblByaW5jaXBhbDpleUppWVhOcFkxVnpaWElpT25zaWRYTmxja2xrSWpvek5UYzFOalUxTENKMWMyVnlRMjlrWlNJNklrMVZNakF5TkRBNU1UWXdNREEwTlRraUxDSjFjMlZ5VG1GdFpTSTZJbTltYzB0Q05VZ3dibk4wUkVoS2NtUmtjVGRTYWkxS05YUXdla0VpTENKdWFXTnJUbUZ0WlNJNkl1aUhyZVd1blVaQk1FTkNOREpFSWl3aWJXOWlhV3hsSWpvaU1UZ3dPRGMyTnpNd01qVWlMQ0p6WlhOemFXOXVTMlY1SWpwdWRXeHNMQ0p5YjJ4bFRHbHpkQ0k2Ym5Wc2JDd2laR1YyYVdObElqcHVkV3hzTENKcGMxQmpJanBtWVd4elpTd2lhWE5CWjNKbFpTSTZkSEoxWlN3aWJXOWlhV3hsVEc5bmIyWm1VM1JoZEhWeklqcG1ZV3h6WlgxOSJdLCJqdGkiOiI2YzBiMTNkNC1iNGI4LTQ5Y2EtOGZiOC1jMGQzODE1NTc0ZTciLCJjbGllbnRfaWQiOiJ3bi1jbG91ZCIsInNjb3BlIjpbIm9wZW5pZCJdfQ.F-rH8KTf0YlMn0vtyQz-FIoJZobxgSyjouSy9CeMGjP3sPRTp76nTAUeQXM68MPAu3UlJX9mNW7awah5uSMCO0RlaBSbYQIt3m5-N_sAfoedAhKgBXFKLwTAKjK06hHl-D_j2fxYLzOb5gcsSBDvvCLyn_A-xHreAhiG5Cc3QZD8YLlnj0bUiObXDlF55TeyouvJ7XYdYna5mMZg4RSL8CRfyeSt-GqBSjOO5Npvc9guwtV9przZddn6APosYyPUPdnlIlq68VZKp4lCfxNylODgSDqim5DZgBtzfjA7WBBpGrN70wzsQ66K-_jKb_gIO7beo40OVmWhTsadbHR_5g'
    tkname = 'hsy'
    if not token:
        token = os.getenv(tkname)
        if not token:
            Log(f"⛔️请设置环境变量:{tkname}⛔️")
            exit()
    tokens = token.split("@")
    Log(f"一共获取到{len(tokens)}个账号")
    i = 1
    for token in tokens:
        Log(f"\n--------开始第{i}个账号--------")
        if not start(token):
            Log(f"--------第{i}个账号异常结束，开始第{i+1}个账号--------\n")
            continue
        Log(f"--------第{i}个账号结束--------\n")
        i += 1
    
    
        