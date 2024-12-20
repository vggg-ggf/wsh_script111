"""
name: 爱裹旧衣服回收，手机号验证码认证，兑换
Author: MK集团本部
Date: 2024-09-24
export aghs="Authorization"
cron: 0 5 * * *
"""
#import notify
import requests, json, os, sys, time, random, datetime
response = requests.get("https://mkjt.jdmk.xyz/mkjt.txt")
response.encoding = 'utf-8'
txt = response.text
print(txt)
#---------------------主代码区块---------------------
session = requests.session()

def userinfo(ck):
	url = 'https://alipay.haliaeetus.cn/recy/api/auth/asset/getInfo'
	urljf = 'https://alipay.haliaeetus.cn/fuli/api/jf/account'
	header = {
		"Connection": "keep-alive",
		"User-Agent": "Mozilla/5.0 (Linux; Android 10; MI 8 Build/QKQ1.190828.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/126.0.6478.188 Mobile Safari/537.36 XWEB/1260117 MMWEBSDK/20240501 MMWEBID/3169 MicroMessenger/8.0.50.2701(0x2800325B) WeChat/arm64 Weixin NetType/WIFI Language/zh_CN ABI/arm64 MiniProgramEnv/android",
		"content-type": "application/json",
		"Authorization": ck,
	}
	data = {}
	try:
		response = session.post(url=url, headers=header, data=data)
		info = json.loads(response.text)
		responsejf = session.post(url=urljf, headers=header, data=data)
		infojs = json.loads(responsejf.text)
		#print(info)
		if info["status"] == 200:
			return infojs["data"],info["data"]["userName"]
	except Exception as e:
		#print(e)
		pass

def run(id,ck):
	login = 'https://alipay.haliaeetus.cn/fuli/api/fuli/signed'
	header = {
		"Connection": "keep-alive",
		"User-Agent": "Mozilla/5.0 (Linux; Android 10; MI 8 Build/QKQ1.190828.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/126.0.6478.188 Mobile Safari/537.36 XWEB/1260117 MMWEBSDK/20240501 MMWEBID/3169 MicroMessenger/8.0.50.2701(0x2800325B) WeChat/arm64 Weixin NetType/WIFI Language/zh_CN ABI/arm64 MiniProgramEnv/android",
		"content-type": "application/json",
		"Authorization": ck,
	}
	data = {}
	try:
		userinfo(ck)
		response = session.get(url=login, headers=header, json=data)
		login = json.loads(response.text)
		#print(login)
		a,b = userinfo(ck)
		if login["status"] == 200:
			print(f"📱：{b}\n☁️签到：成功\n🌈积分：{a}分")
		else:
			print(f"📱：{b}\n☁️签到：成功\n🌈积分：{a}分")
		time.sleep(2)
	except Exception as e:
		print("📱：账号已过期或异常")

def main():
	if os.environ.get("aghs"):
		ck = os.environ.get("aghs")
	else:
		ck = ""
		if ck == "":
			print("请设置变量")
			sys.exit()
	if datetime.datetime.strptime('05:01', '%H:%M').time() <= datetime.datetime.now().time() <= datetime.datetime.strptime('06:59', '%H:%M').time():
		time.sleep(random.randint(100, 500))
	ck_run = ck.split('\n')
	print(f"{' ' * 10}꧁༺ 爱裹༒回收 ༻꧂\n")
	for i, ck_run_n in enumerate(ck_run):
		print(f'\n----------- 🍺账号【{i + 1}/{len(ck_run)}】执行🍺 -----------')
		try:
			ck = ck_run_n
			run(id,ck)
			time.sleep(random.randint(1, 2))
		except Exception as e:
			print(e)
			#notify.send('title', 'message')

	print(f'\n----------- 🎊 执 行  结 束 🎊 -----------')


if __name__ == '__main__':
	main()