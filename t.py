import http.client
import re
import argparse
import json
import sys

def isConnected():
    try:
        conn = http.client.HTTPSConnection("p.njupt.edu.cn", 802)
        payload = ''
        headers = {
            'User-Agent': 'Apifox/1.0.0 (https://apifox.com)',
            'Accept': '*/*',
            'Host': 'p.njupt.edu.cn:802',
            'Connection': 'keep-alive'
        }
        conn.request("GET", "/eportal/portal/online_list?callback=dr1002", payload, headers)
        res = conn.getresponse()
        data = res.read()
        json_data = json.loads(data.decode('UTF-8')[len('dr1002('):-len(');')])
        if json_data["result"] == 0:
            return False
        else:
            return True
    except:
        return True
 
while not isConnected():
    try:
        conn = http.client.HTTPSConnection("p.njupt.edu.cn")
        payload = ''
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.84 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
            "Referer": "",
        }


        parser = argparse.ArgumentParser()
        parser.add_argument('--user',  type=str, help='user name')
        parser.add_argument('--password', type=str, help='password')
        parser.add_argument('--way', type=str, help='which carrier?[njxy|cmcc|[NULL]]')
        args = parser.parse_args()
        # 用户名/密码/运营商njxy|cmcc|[NULL]

        conn.request("GET", "/a79.htm", payload, headers)
        res = conn.getresponse()
        data = res.read()
        ## print(data.decode("GBK"))
        pattern = r"v46ip='(\d+\.\d+\.\d+\.\d+)'"
        match = re.search(pattern, data.decode("GBK"))
        ip_address = match.group(1)

        get_par_fin = {
            "callback":"dr1003",
            "login_method":"1",
            "user_account":",0,"+args.user+"@"+args.way,
            "user_password":args.password,
            "wlan_user_ip":ip_address,
            "wlan_user_ipv6":"",
            "wlan_user_mac":"000000000000",
            "wlan_ac_ip":"",
            "wlan_ac_name":"",
            "jsVersion":"4.1.3",
            "terminal_type":"1",
            "lang":"zh-cn",
            "lang":"zh",
            "v":""
        }

        conn1 = http.client.HTTPSConnection("p.njupt.edu.cn", 802)
        query_params = "&".join([f"{key}={value}" for key, value in get_par_fin.items()])
        conn1.request("GET","/eportal/portal/login?"+query_params,payload,headers)


    except:
        print("Unknow ERROR")
        sys.exit(1)
        pass