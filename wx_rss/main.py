from bs4 import BeautifulSoup
import requests
import json
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta, timezone   
  

rrs_url = "http://47.120.15.38:604/feeds/all.atom"
key='84b0e0c1-fc64-40a7-a965-4004f17ed073'
keyword1='大专'
keyword2='专科'
keyword3='中专'
keyword4='预防医学'
keyword5='公卫'


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


def find_url_with_keywords(url, keyword1, keyword2,keyword3,keyword4,keyword5):
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        text = soup.get_text(strip=True).lower() 
        found1 = keyword1 in text or keyword2 in text or keyword3 in text
        found2 = keyword4 in text or keyword5 in text

        if found1 and found2:
            return url

def write(text):
    with open('link.txt', 'a',encoding='utf-8') as file:
        file.write(text)
        file.write('\n')

def get_soup(url):
    response = requests.get(url).text
    with open('rrs.xml', 'w',encoding='utf-8') as file:
        file.write(response)
   
               
    


def start(key,keyword1,keyword2,keyword3,keyword4,keyword5):
    try:
        root = ET.parse('rrs.xml').getroot()  
        ns = {'atom': 'http://www.w3.org/2005/Atom'}   
        for entry in root.findall('atom:entry', ns):  
            updated_elem = entry.find('atom:updated', ns).text
            if check_date_difference(updated_elem):
                link = entry.find('atom:link', ns).get("href")
                with open('link.txt', 'r',encoding='utf-8') as file:
                    links = file.read()  
                    if  link in links: 
                        print('已经无最新文章')
                    else:
                        write(link)
                        url = find_url_with_keywords(link,keyword1,keyword2,keyword3,keyword4,keyword5)
                        if url is not None:
                            description,picurl = get_title_and_cover_image(url)
                            send_wechat_robot_message(key, url,description,picurl)
    
    except Exception as e:
        print(f"发生错误: {e}")

   
 
  
def check_date_difference(target_date_str):  
    # 使用dateutil.parser解析ISO 8601格式的日期时间字符串  
    target_datetime = datetime.strptime(target_date_str, "%Y-%m-%dT%H:%M:%S.%fZ")  
    target_datetime = target_datetime.replace(tzinfo=timezone.utc)  # 添加UTC时区信息  
      
    # 获取当前UTC时间  
    current_datetime = datetime.now(timezone.utc)  # 使用带有UTC时区信息的now方法  
      
    # 计算日期时间差  
    datetime_difference = current_datetime - target_datetime  
      
    # 检查是否超过3天  
    if datetime_difference > timedelta(days=7):
        print('时间大于规定时间')  
        return False
    else:  
        return True
    

get_soup(rrs_url)
start(key,keyword1,keyword2,keyword3,keyword4,keyword5)




    
