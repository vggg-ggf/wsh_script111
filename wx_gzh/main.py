import time
import random
import requests
import json
from bs4 import BeautifulSoup



 

def get_content(key,keyword,Cookie,token):
    url = "https://mp.weixin.qq.com/cgi-bin/appmsg"
    headers = {
    "Cookie": Cookie,        
    "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.0.0'
        }
    search_url = 'https://mp.weixin.qq.com/cgi-bin/searchbiz?action=search_biz&begin=0&count=5&query={}&token={}&lang=zh_CN&f=json&ajax=1'.format(keyword,token)
    doc = requests.get(search_url,headers=headers).text
    jstext = json.loads(doc)
    if 'list' in jstext:
        fakeid = jstext['list'][0]['fakeid']
    else:
        txt = 'cookie失效'
        send_txt_message(key,txt)
        fakeid = None
    
    data = {
        "token": token,
        "lang": "zh_CN",
        "f": "json",
        "ajax": "1",
        "action": "list_ex",
        "begin": 0,
        "count": "5",
        "query": "",
        "fakeid": fakeid,
        "type": "9",
        }
    json_res= requests.get(url, headers=headers, params=data).text
    json_res = json.loads(json_res)
    return json_res

def getLinks(json_res):
    links = [item['link'] for item in json_res['app_msg_list']]
    return links

def getImages(json_res):
    image = [item['cover'] for item in json_res['app_msg_list']] 
    return image

def get_title_and_cover_image(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    title = soup.find(id='activity-name').text
    cover_image = soup.find('meta', property='og:image')['content']
    return title, cover_image

def send_wechat_robot_message(key, url,description,picurl):
    webhook = f'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key={key}'
    url = url
    description = description
    picurl = picurl
    headers = {'Content-Type': 'application/json'}
    data = {
    "msgtype": "news",
    "news": {
       "articles" : [
           {
               "title" : "公众号招聘信息",
               "description" : f"{description}",
               "url" : f"{url}",
               "picurl" : f"{picurl}"
           }
        ]
    }
}
    response = requests.post(webhook, headers=headers, data=json.dumps(data))
    if response.status_code == 200:
        print("消息发送成功")
    else:
        print("消息发送失败，错误码：", response.status_code)


def send_txt_message(key,txt):
    webhook = f'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key={key}'
    txt = txt
    headers = {'Content-Type': 'application/json'}
    data = {
    "msgtype": "text",
    "text": {
        "content": f"main脚本出错，内容：{txt}",
		"mentioned_mobile_list":["18087673025"]
    }
    }
    response = requests.post(webhook, headers=headers, data=json.dumps(data))
    if response.status_code == 200:
        print("消息发送成功")
    else:
        print("消息发送失败，错误码：", response.status_code)



def find_url_with_keywords(url, keyword1, keyword2,keyword3,keyword4,keyword5):
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        text = soup.get_text(strip=True).lower() 
        found1 = keyword1 in text or keyword2 in text or keyword3 in text
        found2 = keyword4 in text or keyword5 in text

        if found1 and found2:
            return url

def write_link(url):
    with open('links.txt', 'a',encoding='utf-8') as file:
        file.write(url)
        file.write('\n')

def check_link(link):
    with open('links.txt', 'r',encoding='utf-8') as file:
        urls = file.read()
        if  link in urls:
            return False
        else: return True


def start(key,Cookie,token,keyword1,keyword2,keyword3,keyword4,keyword5):
    try:
        with open('name.txt', 'r',encoding='utf-8') as file:  
            names = file.readlines()  
            for name in names:  
                print(f'开始爬取{name}的文章') 
                links = getLinks(get_content(key,name.strip(),Cookie,token))
                t=random.randint(160, 180)
                print(f"随机等待{t}秒")
                time.sleep(t)
                for link in links:
                    if check_link(link):
                        write_link(link)
                        print(f'写入文章：{link}')
                        url = find_url_with_keywords(link,keyword1,keyword2,keyword3,keyword4,keyword5)
                        if url is not None:
                            description,picurl = get_title_and_cover_image(url)
                            send_wechat_robot_message(key, url,description,picurl)
                    else:
                        print(f'{name}已经无最新文章')        

                        

    except Exception as e:
        print(f"An error occurred: {e}")
        send_txt_message(key,e)

def init():
        # 打开JSON文件并读取内容  
    with open('env1.json', 'r') as file:  
        data = json.load(file)  
    
    # 获取变量  
    Cookie= data['Cookie']  
    token = data['token']  
    keyword1 = data['keyword1']
    keyword2 = data['keyword2']  
    keyword3 = data['keyword3']  
    keyword4 = data['keyword4']  
    keyword5 = data['keyword5']  
    key = data['key'] 
    start(key,Cookie,token,keyword1,keyword2,keyword3,keyword4,keyword5)  

def main():
    init()
   

main()