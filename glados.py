import requests,json,os
# -------------------------------------------------------------------------------------------
# github workflows
# -------------------------------------------------------------------------------------------

def fqtt(sckey, status, msg):
    url = "https://sctapi.ftqq.com/" + sckey + ".send"
    payload = {'title': status + ":" + msg}
    response = requests.request("POST", url, headers={}, data=payload)
    print(response.text)

if __name__ == '__main__':
# pushplus秘钥 申请地址 http://www.pushplus.plus
    sckey = os.environ.get("PUSHPLUS_TOKEN", "")
# 推送内容
    sendContent = ''
# glados账号cookie 直接使用数组 如果使用环境变量需要字符串分割一下
    cookies = os.environ.get("GLADOS_COOKIE", []).split("&")
    if cookies[0] == "":
        print('未获取到COOKIE变量') 
        cookies = []
        exit(0)
    url= "https://glados.rocks/api/user/checkin"
    url2= "https://glados.rocks/api/user/status"
    referer = 'https://glados.rocks/console/checkin'
    origin = "https://glados.rocks"
    useragent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36"
    payload={
        'token': 'glados.one'
    }
    for cookie in cookies:
        checkin = requests.post(url,headers={'cookie': cookie ,'referer': referer,'origin':origin,'user-agent':useragent,'content-type':'application/json;charset=UTF-8'},data=json.dumps(payload))
        state =  requests.get(url2,headers={'cookie': cookie ,'referer': referer,'origin':origin,'user-agent':useragent})
    #--------------------------------------------------------------------------------------------------------#  
        time = state.json()['data']['leftDays']
        time = time.split('.')[0]
        # email = state.json()['data']['email']
        if 'message' in checkin.text:
            points = checkin.json()['points']
            print('结果--'+ str(points)+'----剩余'+ time+'天')  # 日志输出
            sendContent +=  'Get ' + points + 'P & Left ' + time + 'D'
        else:
            fqtt(sckey, "ERROR", "Cookie Invalid" )
            requests.get('https://sctapi.ftqq.com/' + sckey + '.send?title='+ 'ERROR-cookie已失效')
            print('cookie已失效')  # 日志输出
     #--------------------------------------------------------------------------------------------------------#   
    if sckey != "":
         fqtt(sckey, "SUCCESS", sendContent)
         print('ftqq 已经调用')


