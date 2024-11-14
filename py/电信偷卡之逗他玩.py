import requests
pushplus_token = "2c71f338b6604cba80490edfc7357276"
def send_push_notification(pushplus_token):
    pushplus_url = "http://www.pushplus.plus/send"
    payload = {
        "token": pushplus_token,
        "title": "抽中生肖卡-龙",
        "content": "抽中生肖卡-龙"  # 发送的消息内容
    }
    try:
        response = requests.post(pushplus_url, json=payload)
        response.raise_for_status()
        print("推送成功")
    except Exception as e:
        pass

if __name__ == '__main__':
    send_push_notification(pushplus_token)
