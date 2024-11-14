import requests,re,time,random,json,os
from datetime import datetime, timedelta
from threading import Thread

requests.packages.urllib3.disable_warnings()
request = requests.session()
request.verify = False
headers = {
    "Content-Type": "application/x-www-form-urlencoded; charset=utf-8",
    "Host": "api.weibo.cn"
}



def get_timescope():
    # 获取当前日期
    today = datetime.now()
    # 计算前一天的日期
    yesterday = today - timedelta(days=1)
    # 计算前两天的日期
    day_before_yesterday = yesterday - timedelta(days=1)
    # 格式化日期为字符串
    timescope = f"{day_before_yesterday.strftime('%Y-%m-%d')}-0:{yesterday.strftime('%Y-%m-%d')}-0"
    return timescope

def friendship(uid,ck):
    url = "https://api.weibo.cn/2/friendships/create?"+ck
    headers = {
    "Content-Type": "application/x-www-form-urlencoded; charset=utf-8",
    }
    data = f"uid={uid}"

    res = request.post(url, headers=headers, data=data)
    
    try:
        print(f'{res.json()["name"]}关注成功')
    except Exception as e:
        print(e)
        print(res.text)

def report(mid,ck):
    def replace_pattern_with_regex(s, pattern, replacement):
            # 使用 re.sub() 函数进行替换，pattern 需要是一个正则表达式
            return re.sub(pattern, replacement, s)
    comments = []
    pattern = r'\[[^\]]*\]'
    data = {
    'count': '20',
    'id': mid,
    'is_mix': '1',
    'is_show_bulletin': '2',
    }
    response = requests.post('https://api.weibo.cn/2/comments/build_comments?'+ck,headers=headers, data=data)
    try:
        datas=response.json().get('datas',['占沙发','111',"44","试一试","万一呢"])
        if datas[1]=='111':
            comments=datas
        else:
            for d in datas:
                if d['type']==0:
                    new_s = replace_pattern_with_regex(d['data']['text'], pattern, '')
                    comments.append(new_s)
        selected_comments = str(random.sample(comments, 1)).strip("[]'") 
    except:
        datas = response.json().get('root_comments',['占沙发','111',"44","试一试","万一呢"])
        if datas[1]=='111':
            comments=datas
        else:
            for d in datas:
                new_s = replace_pattern_with_regex(d['text'], pattern, '')
                comments.append(new_s)
        selected_comments = str(random.sample(comments, 1)).strip("[]'") 
    url = "https://api.weibo.cn/2/statuses/repost?"+ck
   
    print(f"随机选择的评论是：{selected_comments}")
    data = f"id={mid}&is_comment=1&status={selected_comments}"

    res = request.post(url, headers=headers, data=data.encode('utf-8'))
    try:
        print('抽奖内容转发成功')
    except Exception as e:
        print(e)
        print(res.text)
def set_like(mid,ck):

    url = "https://api.weibo.cn/2/like/set_like?"+ck
    data = {'id': mid}
    res = requests.post(url, headers=headers, data=data)
    #print(res.text)
    print('点赞成功')

def get_search_max_page(data):
    page_pattern = re.compile(r'<li><a href="[^"]*page=(\d+)">第\1页</a></li>')
    pages = page_pattern.findall(data)
    # 提取页码并找到最大值
    if pages:
        last_page = max(int(page) for page in pages)
        print(f"最后一页的页数是：{last_page}")
        return last_page
    else:
        print("没有找到匹配的页码")
        return 1

def search(keyword, timescope='2024-11-09-0:2024-10-09-0', page=1):
    url = f"https://s.weibo.com/weibo?q={keyword}&scope=ori&suball=1&timescope=custom:{timescope}-0&Refer=g&page={page}"
    cookies = {
    "SUB": "_2A25KK0-zDeRhGeBI6lMZ9CrKzz2IHXVpSc17rDV8PUNbmtANLVHHkW9NRrygYRrIMPTTF_qaIhVACoQa2kB86IsE",
    }

    headers = {
    "Host": "s.weibo.com"
    }

    res = requests.get(url, headers=headers, cookies=cookies)
    return res.text
    
def get_search_list(data):
    pattern = re.compile(r'mid=(\d+)&name=[^&]+&uid=(\d+)')
    # 搜索匹配项
    matches = pattern.findall(data)

    # 将匹配的 mid 和 uid 组合成一个列表
    result = [match for match in matches]

    print("提取的mid和uid列表:", result)
    return result

def start(ck,keyword='转 关 抽'):
    counts = 1
    timescope = get_timescope()
    data = search(keyword)
    max_page = get_search_max_page(data)
    print(f"最大页数是：{max_page}")
    
    for i in range(1, max_page+1):
        data = search(keyword,page=i)
        l = get_search_list(data)
        for j in l:
            report(j[0],ck)
            friendship(j[1],ck)
            set_like(j[0],ck)
            r_time = random.randint(100, 300)
            print(f"第{counts}个动态转发，休眠{r_time}秒")
            time.sleep(r_time)
            counts += 1
        r_time = random.randint(100, 300)
        print(f"第{i}页转发完成，休眠{r_time}秒")
        time.sleep(r_time)
    


if __name__ == '__main__':
    ck=''
    #ck = 'gsid=_2A25KNElFDeRxGeFH7VMX-CrJyDuIHXVnYNuNrDV6PUJbkdAGLVL8kWpNesRXzyLtZnPA4VqKWBmyiZLwR8Soz_km&s=b223ebea@gsid=_2A25KNE31DeRxGeBI6lMZ9CrKzz2IHXVnYMY9rDV6PUJbgdAbLXatkWpNRrygYWzA9B5Vde6o2desSg3EtuqG1Y4F&s=f4689af5'
    name = 'weibo'
    if not ck:
        ck = os.getenv(name)
        if not ck:
            print(f"⛔️请设置环境变量:{name}⛔️")
            exit()
    cks = ck.split("@") if "@" in ck else (ck, "")
    print(f"一共获取到{len(cks)}个账号")
    # 获取当前时间
    now = datetime.now()
    # 获取当前时间的小时数
    current_hour = now.hour
    # 检查是否在早上5点到10点之间
    if 4 <= current_hour < 10:
        keyword = ["转 关 抽"]
    if 10 <= current_hour < 18:
        keyword = ["%23转发抽奖"]
    else:
        keyword = ["转发 关注 评论"]
    #keyword = ["转发关注评论"]
    for j in range(0, len(keyword)):
        print(f"第{j+1}轮开始")
        thread1 = Thread(target=start, args=(cks[0], keyword[j]))
        thread2 = Thread(target=start, args=(cks[1], keyword[j]))
        print("线程1启动")
        thread1.start()
        print("线程2启动")
        thread2.start()
        thread1.join()
        thread2.join()
 

