import requests
import json
import os

requests.packages.urllib3.disable_warnings()
requests = requests.Session()
requests.verify = False
def get_cms(phone):
    json_data = {
        'motivation':'LOGIN',
        'mobile':phone,
        'captcha':{
            'key':'',
            'code':''
            }
        }
    response = requests.post('https://api.sodalife.xyz/v1/sms-codes',json=json_data)
    print(response.json())
def sumbit_cms(phone,cms):

    json_data = {
        'mobile': phone,
        'smsCode': cms,
        'captcha': {
            'key': '',
            'code': '',
        },
        'app': 'MOBILE',
        'options': {
            'jpush': {
                'regId': '',
            },
        },
    }

    response = requests.post('https://api.sodalife.xyz/v1/session/accounts/actions/login',json=json_data)
    return response.json()
    # if response.json()['data']['token']:
    #     return response.json()['data']['token']
    # else:
    #     print(response.json())
    #     return response.json()

def set_os(name,key):
    os.environ[name] = key

if __name__ == '__main__':
    p = input("请输入手机号")
    get_cms(p)
    c = input("请输入验证码")
    token = sumbit_cms(p,c)
    print(token)
    set_os('SDXY',token)