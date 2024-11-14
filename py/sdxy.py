import requests
import json
import os
import time
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

requests = requests.Session()
requests.verify = False
watering_key_1 = 'DZNOHI90Q8'
watering_key_5 = 'ES8FHKR9VP'

def timestamp():
    return int(time.time()*1000)

def get_headers(token):
    return {
        'authorization': f'Bearer {token}',
    }


def watering(watering_key,token):
    headers = {
    'authorization': f'Bearer {token}',
    }
    data = {
        'configKey': watering_key
    }
    response = requests.post('https://api.sodalife.xyz/hydr/v1/task/wish-forest/mine/trees/TKH2ICE43YZVWR8N/actions/watering', headers=headers,json=data)
    #print(response.json())
    if response.json()['data']: 
        print(f"浇水成功！{response.json()['data']['watered']['title']}")
        return True
    else:
        print(f"浇水失败！{response.json()['message']}")
        return False





class user():
    def __init__(self,token) -> None:
        self.headers = {
        'authorization': f'Bearer {token}',
        }

    
    def check_water(self):
        url = 'https://api.sodalife.xyz/hydr/v1/asset/mine/assets/T0VRH8SCA3YNXO4Q'
        response = requests.get(url,headers=self.headers).json()
        if response:
            current_water = response['data']['value']
            print(f"当前水量:{current_water}")
            return current_water
    
    def get_user_info(self):

        url = 'https://api.sodalife.xyz/v1/session/user'
        response = requests.get(url,headers=self.headers)
        if response.json()['data']: 
            user_name = response.json().get('data').get('nickname','未获取到用户名')
            user_phone = response.json().get('data').get('mobile','未获取到手机号')
            print(f'当前用户：{user_name}，手机号：{user_phone}')
            return True
        else:
            print(response.json()['message'])
            return False
        

class get_water():
    def __init__(self,token) -> None:
        self.headers = {
        'authorization': f'Bearer {token}',
        }
    def get_water_key(self):
        url = "https://api.sodalife.xyz/hydr/v1/task/mine/tasks"
        params = {
            'tag': 'WISH_FOREST_TREE',
            'limit': '50',
            'offset': '0',
        }
        response = requests.get(url, params=params, headers=self.headers)
        #print('==========================key=====================')
        #print(response.json())
        reservoir_key = response.json()['data']['objects'][0]['key']
        reservoir_recordKey = response.json()['data']['objects'][0]['recordKey']
        bottle_key = response.json()['data']['objects'][1]['key']
        bottle_recordKey = response.json()['data']['objects'][1]['recordKey']

        #print(response.json())
        return reservoir_key, bottle_key, reservoir_recordKey, bottle_recordKey

    def get_activity_key(self):
        url = "https://api.sodalife.xyz/hydr/v1/task/mine/tasks"
        params = {
            "tag": "WISH_FOREST_BOARD",
            "limit": "50",
            "offset": "0"
        }
        response = requests.get(url, headers=self.headers, params=params)
        timer_water_key = response.json()['data']['objects'][0]['key']
        timer_water_recordKey = response.json()['data']['objects'][0]['recordKey']
        task_5_water_key = response.json()['data']['objects'][4]['key']
        task_5_water_recordKey = response.json()['data']['objects'][4]['recordKey']
        #print(response.json())
        return timer_water_key, timer_water_recordKey, task_5_water_key, task_5_water_recordKey

        
    def get_reservoir(self):
        reservoir_key, bottle_key, reservoir_recordKey, bottle_recordKey = self.get_water_key()
        reservoir = requests.post(f'https://api.sodalife.xyz/hydr/v1/task/mine/tasks/{reservoir_key}/records/{reservoir_recordKey}', headers=self.headers)
        print(reservoir.json())
        print('水缸领取成功')
    def get_bottle(self):
        reservoir_key, bottle_key, reservoir_recordKey, bottle_recordKey = self.get_water_key()
        data = json.dumps({"taskKey":bottle_key})
        bottle_start = requests.post('https://api.sodalife.xyz/hydr/v1/task/wish-forest/mine/actions/countdown-start', headers=self.headers,data=data)
        print('水瓶计时开始')
        #print(bottle_start.json())
        watering(watering_key_5,token)
        time.sleep(70)
        bottle = requests.post(f'https://api.sodalife.xyz/hydr/v1/task/mine/tasks/{bottle_key}/records/{bottle_recordKey}', headers=self.headers)
        print(bottle.json())
        print('水瓶领取成功')
       
    def get_timer_water(self):
        timer_water_key, timer_water_recordKey, task_5_water_key, task_5_water_recordKey = self.get_activity_key()
        url = f'https://api.sodalife.xyz/hydr/v1/task/mine/tasks/{timer_water_key}/records/{timer_water_recordKey}'
        timer_water = requests.post(url, headers=self.headers)
        print(url)
        print(timer_water.json())
        print('定时水领取成功')
        print(timer_water_key, timer_water_recordKey)
        
    def task_5_water(self):
        timer_water_key, timer_water_recordKey, task_5_water_key, task_5_water_recordKey = self.get_activity_key()
        url = f'https://api.sodalife.xyz/hydr/v1/task/mine/tasks/{task_5_water_key}/records/{task_5_water_recordKey}'
        response = requests.post(url, headers=self.headers)
        print(response.json())
        print('5次浇水奖励领取成功')



class task():
    def __init__(self,token) -> None:
        self.headers = {
        'authorization': f'Bearer {token}',
        }
    def task_visit(self):
        i = 1
        posterPositionIds = ['SODA_APP:WISH_FOREST:TASKS:VISIT1','SODA_APP:WISH_FOREST:TASKS:VISIT2','SODA_APP:WISH_FOREST:TASKS:VISIT3','SODA_APP:WISH_FOREST:TASKS:VISIT4','SODA_APP:WISH_FOREST:TASKS:VISIT5',]
        for pid in posterPositionIds:
            response = requests.get(f'https://api.sodalife.xyz/hydr/v1/poster/posters?posterPositionIds={pid}', headers=self.headers)
            try:
                sourceId = response.json()['data'][0]['sources']['dynamic'][0]['sourceId']
                time.sleep(15)
            except:
                sourceId = ''
                print(f'第个{i}任务已经完成')
                i += 1
                continue
            params = {
                '__t': timestamp(),
                'isPrivate': '1',
                'sourceId': sourceId,
            }
            response = requests.post('https://api.sodalife.xyz/hydr/v1/poster/platforms/SODA_ACTIVITY/notification', params=params, headers=self.headers)
            print(response.json())
            print(f'第{i}任务{pid}完成')
            i += 1

    def task_click(self):
        skid_ids = ['7JO9X1702869877','0DIU91724840898','7D4AS1724744240','O2Z131712550848','17BMN1703144411','BNMG31697108477','HL5WD1712541999','SP6GJ1697108693','P9B3D1717123798','TXKWS1702870772','2S96W1697107796']
        for sku_id in skid_ids:
            time.sleep(2)
            params = {
                'isPrivate': '1',
                'sourceId': 'MjUxNS1TT0RBX0FQUDpXSVNIX0ZPUkVTVDpHT09EU0xJU1Q6Q0xJQ0s',
                '__t': timestamp(),
            }
            data = json.dumps({"payload": {"skuId": sku_id}})
            response = requests.post('https://api.sodalife.xyz/hydr/v1/poster/platforms/SODA_ACTIVITY/notification', params=params,data=data, headers=self.headers)
            print(response.json())
            print(f'商品id:{sku_id}点击成功')
            

    def daily_checkin(self):
        url = 'https://api.sodalife.xyz/hydr/v1/task/wish-forest/mine/actions/daily-checkin'
        response = requests.post(url, headers=self.headers)
        print(response.json())
        print('签到成功')
        

    def task_finish_reword(self):
        def get_task_id():
            url = 'https://api.sodalife.xyz/hydr/v1/task/mine/tasks/E768JX2LY04UORAP/records'
            response = requests.get(url, headers=self.headers)
            return response.json()['data']['objects']
        for task_id in get_task_id():
            task_key = task_id['taskKey']
            record_key = task_id['recordKey']
            url = f'https://api.sodalife.xyz/hydr/v1/task/mine/tasks/{task_key}/records/{record_key}'
            response = requests.post(url, headers=self.headers)

            print(response.json())
            print('任务累计完成领取')
    

        

class points():
    def __init__(self, token):
        self.headers = {
            'authorization': f'Bearer {token}',
        }
        self.headers['x-token'] = self.headers['authorization'].replace('Bearer ','')
    def lottery(self):
        params = {
            '__t': timestamp(),
        }
        url = 'https://api.sodalife.xyz/act/202207-lucky-goods/active/4QKZRVNU1PW0/me'
        response = requests.post(url, headers=self.headers, params=params)
        print(response.json())
        print('开始积分抽奖')
        if response.json()['data']:
            print(response.json()['data']['skus'][0]['name'])
        else:
            print(response.json()['message'])
    

def lucky(token):
    headers = {
        'authorization': f'Bearer {token}',
    }
    response = requests.post('https://api.sodalife.xyz/act/202207-lucky-goods/active/OLSP94XHMB0J/me', headers=headers)
    try:
        data = response.json()['gotPrizeName']
        print(data)
    except:
        print(response.json()['message'])

def lottery_egg(token):
    headers = {
        'authorization': f'Bearer {token}',
    }
    headers['x-token'] = headers['authorization'].replace('Bearer ','')
    def lottery_start():
        params = {
            '__t': timestamp(),
        }
        url = 'https://api.sodalife.xyz/act/202409-lucky-goods/active/LG2YOJ710C49/me'
        response = requests.post(url, headers=headers, params=params)
        print('开始抽奖')
        print(response.json())
    def lottery_share():
        url = 'https://api.sodalife.xyz/act/202409-lucky-goods/active/LG2YOJ710C49/actions/active-share'
        params = {
            '__t': timestamp(),
        }
        response = requests.post(url, headers=headers,params=params)
        print('分享成功')
        # print(response.json())
    lottery_share()
    time.sleep(3)
    for i in range(2):
        time.sleep(2)
        lottery_start()

def start(token):
    task_i = task(token)
    get_water_i = get_water(token)
    task_i.daily_checkin()
    time.sleep(2)
    get_water_i.get_reservoir()
    get_water_i.get_bottle()
    get_water_i.get_reservoir()
    get_water_i.get_timer_water()
    get_water_i.task_5_water()
    task_i.task_visit()
    task_i.task_click()
    task_i.task_finish_reword()
    get_water_i.get_bottle()
    get_water_i.get_reservoir()
    get_water_i.get_bottle()
    lucky(token)



if __name__ == '__main__':
    #token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MzkwOTAzMDUsImlzcyI6ImFwaS5zb2RhbGlmZS54eXoiLCJzZXNzaW9uSWQiOiJZV1V6Tm1Ka01EWXROV1U1WVMwME1XUTVMV0UyWldZdFpqUTBabVEwTVRoalltVTEifQ.HIwewKiR3tDxhn6xP786a3vkA4gww1HR77CxejrN9ZM@eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MzkxNzU2ODIsImlzcyI6ImFwaS5zb2RhbGlmZS54eXoiLCJzZXNzaW9uSWQiOiJPRFE0T1dZd09XTXRaalV6TmkwME1qUmpMV0ZpTm1RdE1tSTRZalkxTm1FNE9ETmkifQ.OT451di8xkT0F9oY_Yo49Mi3WXsX3DmuqXe7ha38I1w'
    #token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MzkwOTAzMDUsImlzcyI6ImFwaS5zb2RhbGlmZS54eXoiLCJzZXNzaW9uSWQiOiJZV1V6Tm1Ka01EWXROV1U1WVMwME1XUTVMV0UyWldZdFpqUTBabVEwTVRoalltVTEifQ.HIwewKiR3tDxhn6xP786a3vkA4gww1HR77CxejrN9ZM'
    token = ''
    if not token:
        token = os.getenv("wsh_sdxy")
        if not token:
            print("⛔️请设置环境变量:wsh_sdxy⛔️")
            exit()
    tokens = token.split("@")#转成列表
    print(f"一共获取到{len(tokens)}个账号")
    i = 1
    for token in tokens:
        print(f"\n--------开始第{i}个账号--------")
        try:
            user_i = user(token)
            if not user_i.get_user_info():
                print("获取用户信息失败,请检查token是否正确")
                print(f"--------第{i}个账号执行完毕--------")
                i += 1
                continue
            start(token)
            while user_i.check_water() > 300:
                time.sleep(3)
                status = watering(watering_key_1,token)
                if not status:
                    break
                print("开始浇水")
        except Exception as e:
                print(f"出现异常,程序退出,异常信息为{e}")
                continue
        points_i = points(token)
        points_i.lottery()
        print(f"--------第{i}个账号执行完毕--------")
        time.sleep(10)
        i += 1
