from urllib.parse import parse_qs
from urllib.parse import urlsplit
import urllib3
import re
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--user',  type=str, help='user name')
parser.add_argument('--password', type=str, help='password')
parser.add_argument('--way', type=str, help='which carrier?[njxy|cmcc|[NULL]]')
args = parser.parse_args()

# 用户名/密码/运营商njxy|cmcc|[NULL]
login_data = [args.user, args.password, args.way]

# 请求头
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.84 "
                  "Safari/537.36",
}
# 请求链接
static_url = "http://1.1.1.1"

get_par = {
    "wlanuserip": "",  #
    "wlanacip": "",  #
    "wlanacname": "",
    "vlanid": "0",
    "ip": "",  #
    "ssid": "null",
    "areaID": "null",
    "mac": "00-00-00-00-00-00"
}

login_headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.84 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    "Referer": "",
}

post_par = {
    "hostname": "10.10.244.11",
    "iTermType": "1",
    "wlanuserip": "10.66.67.119",
    "wlanacip": "10.168.6.9",
    "wlanacname": "XL-BRAS-SR8806-X",
    "mac": "00-00-00-00-00-00",
    "ip": "10.66.67.119",
    "enAdvert": "0",
    "queryACIP": "0",
    "loginMethod": "1"
}


def get_url():
    # 获取静态链接的所有回复内容

    # static_response = requests.get(static_url, headers=headers,allow_redirects=True)
    ##static_response = requests.get(static_url, verify=False, allow_redirects=True,timeout=3)
    http = urllib3.PoolManager()
    static_response = http.request('GET', static_url)
    new_url = re.findall("[a-zA-z]+://[^\s]*", static_response.data.decode('utf-8'))

    for i in range(0, 2):
        new_url[i] = new_url[i].split('"')[0]
    # 从静态链接302中的跳转页面获取信，用于构造真实的登录页面地址
    if new_url[0] == new_url[1]:
        static_response_302_dict = dict(parse_qs(urlsplit(new_url[0]).query))
    else:
        for i in new_url:
            print(i)
            raise "BAD_URL"
        return

    # 写入请求参数
    get_par['wlanuserip'] = static_response_302_dict['wlanuserip'][0]
    get_par['wlanacip'] = static_response_302_dict['wlanacip'][0]
    get_par['ip'] = static_response_302_dict['wlanuserip'][0]

    real_url_head_str = "http://10.10.244.11/a70.htm?"
    real_url_par_str = 'wlanuserip=' + str(get_par['wlanuserip']) + \
                       '&wlanacip=' + str(get_par['wlanacip']) + \
                       '&wlanacname=' + str(get_par['wlanacname']) + \
                       '&vlanid=' + str(get_par['vlanid']) + \
                       '&ip=' + str(get_par['wlanuserip']) + \
                       '&ssid=' + str(get_par['ssid']) + \
                       '&areaID=' + str(get_par['areaID']) + \
                       '&mac=' + str(get_par['mac'])

    real_url = real_url_head_str + real_url_par_str

    # 构造Referer参数
    login_headers["Referer"] = real_url
    post_par["wlanuserip"] = get_par["wlanuserip"]
    post_par["wlanacip"] = get_par["wlanacip"]
    post_par["ip"] = get_par["ip"]

    # 最后的提交地址
    r_url_head = "http://10.10.244.11:801/eportal/?c=ACSetting&a=Login&protocol=http:"
    r_url_par = "&hostname=" + post_par["hostname"] + "&iTermType=" + post_par["iTermType"] + \
                "&wlanuserip=" + post_par["wlanuserip"] + "&wlanacip=" + post_par["wlanacip"] + \
                "&wlanacname=" + post_par["wlanacname"] + \
                "&mac=" + post_par["mac"] + "&ip=" + post_par["ip"] + \
                "&enAdvert=" + post_par["enAdvert"] + "&queryACIP=" + post_par["queryACIP"] + \
                "&loginMethod=" + post_par["loginMethod"]
    r_url = r_url_head + r_url_par

    return r_url


def isConnected():
    try:
        http = urllib3.PoolManager()
        http.request('GET', 'https://baidu.com', timeout=1)
        return True
    except:
        return False



user_post = {
    "DDDDD": "",
    "upass": "",
    "R1": "0",
    "R2": "0",
    "R3": "0",
    "R6": "0",
    "para": "00",
    "0MKKey": "123456",
    "buttonClicked": "",
    "redirect_url": "",
    "err_flag": "",
    "username": "",
    "password": "",
    "user": "",
    "cmd": "",
    "Login": ""
}

while not isConnected():
    try:
        # 获取真实地址
        URL = get_url()
        # dynamic_R6_data = ['0', '1', '2']
        # for i in range(len(dynamic_R6_data)):
        user_post["DDDDD"] = "," + user_post["R6"] + "," + login_data[0] + "@" + login_data[2]
        user_post["upass"] = login_data[1]

        # 提交表单
        http = urllib3.PoolManager()
        http.request('POST', URL, fields=user_post, headers=login_headers)
        # requests.post(URL, data=user_post, headers=login_headers)
        print("OK")
    except "BAD_URL":
        print("URL_BROKEN")

print("Connected,no operation!")
