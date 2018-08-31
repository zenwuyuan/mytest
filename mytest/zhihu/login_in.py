# 英文验证码的登录方式

# 中文登录（点击倒立文字）

import requests,time,json
from hashlib import sha1
import hmac

import urllib3
urllib3.disable_warnings()

#from requests.packages.urllib3.exceptions import InsecureRequestWarning,InsecurePlatformWarning
#requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
#requests.packages.urllib3.disable_warnings(InsecurePlatformWarning)

headers = {
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:60.0) Gecko/20100101 Firefox/60.0",
    "Referer": "https://www.zhihu.com/signup?next=%2F",
    "origin": "https://www.zhihu.com",
    "Authorization": "oauth c3cef7c66a1843f8b3a9e6a1e3160e20",
    "Host": "www.zhihu.com"
}

# cookies的自动化管理。
# 获取的服务器的Set-Cookie用session直接自动解析并保存，在后续的请求中，会在请求头中自动携带这些cookie
# LWPCookieJar:对cookie进行自动操作，load() save()
from http.cookiejar import LWPCookieJar

session = requests.Session()
session.cookies = LWPCookieJar(filename='zhihucookie.txt')

try:
    session.cookies.load(filename='zhihucookie.txt', ignore_expires=True, ignore_discard=True)
except Exception as e:
    print('暂时没有Cookie')

# res = session.get('https://www.zhihu.com/', headers=headers, verify=False)
# print(res)

def zhihu_login():

    global session
    has_captcha = is_captcha()
    if has_captcha:
        # 获取验证码
        captcha = get_captcha()
        # 在提交登陆之前，还需要对输入的验证码的正确性进行单独验证
        is_true = check_captcha(captcha)
        if is_true == False:
            return
    else:
        captcha = ''

    # 1528450244046.0112
    # print(time.time())
    login_url = "https://www.zhihu.com/api/v3/oauth/sign_in"

    # key(配合着加密数据而使用的Key:d1b964811afb40118a12068ff74a12f4),
    # msg = None, 要加密的重要数据。（适合一个数据加密）
    # digestmod = None, 采用的加密方式, md5, sha1

    # 1. 创建哈希加密对象
    hm = hmac.new(str.encode('d1b964811afb40118a12068ff74a12f4'), msg=None, digestmod=sha1)

    tm = str(int(time.time() * 1000))
    print('tm = ',tm)

    # 2. 开始向加密对象中传入需要加密的数据
    # 注意添加顺序。
    hm.update(str.encode('password'))
    hm.update(str.encode('c3cef7c66a1843f8b3a9e6a1e3160e20'))
    hm.update(str.encode('com.zhihu.web'))
    hm.update(str.encode(tm))

    # 3. 获取加密后的结果(就是signature签名。)
    res = hm.hexdigest()

    print('signature = ',res)

    post_params = {
        "client_id":"c3cef7c66a1843f8b3a9e6a1e3160e20",
        "grant_type": "password",
        "timestamp": tm,
        "source": "com.zhihu.web",
        "signature": res,
        "username": "13633809656",
        "password": "wjf#18650@",
        "captcha": captcha,
        "lang": "cn",
        "ref_source": "homepage",
        "utm_source": "",
    }

    try:
        response = session.post(login_url, data=post_params, headers=headers, verify=False)
        if response.status_code == 201:
            print('登录成功')
            session.cookies.save(ignore_discard=True, ignore_expires=True)
            print(response.text)
        else:
            print('登录失败')
            print(response.text)
    except Exception as e:
        print('请求失败',e)

def is_captcha():
    global COOKIE
    captcha_url = 'https://www.zhihu.com/api/v3/oauth/captcha?lang=en'
    try:
        response = session.get(url=captcha_url, headers=headers,verify=False)
        if response.status_code == 200:
            show_captcha = json.loads(response.text)['show_captcha']
            if show_captcha:
                print('有验证码')
                return True
            else:
                print('没有验证码')
                return False
    except Exception as e:
        print('')

import base64
from PIL import Image
from io import BytesIO


def get_captcha():
    captcha_url = 'https://www.zhihu.com/api/v3/oauth/captcha?lang=en'

    # set-cookie: capsion_ticket="2|1:0|10:1528448404|14:capsion_ticket|44:MjIyMTdjMDNlNWQ0NDU4NDk3YWJiYTJhMGNhYzdhMGU=|27fc1b86cbb52d627f270fdc6ee72f58f88ae09b76483d30ff1026418d83bfce"; Domain=zhihu.com; expires=Sun, 08 Jul 2018 09:00:04 GMT; httponly; Path=/

    try:
        # 索取验证码图片，在保证有验证码的前提下才会发送PUT
        response = session.put(url=captcha_url, headers=headers,verify=False)
        if response.status_code == 202:
            captcha_url = json.loads(response.text)['img_base64']
            # 解码captcha_url

            url = base64.b64decode(captcha_url)
            url = BytesIO(url)
            image = Image.open(url)
            image.show()

            captcha = input('请输入验证码：')
            return captcha
    except Exception as e:
        print('')


def check_captcha(captcha):
    captcha_url = 'https://www.zhihu.com/api/v3/oauth/captcha?lang=en'
    post_params = {
        'input_text': captcha
    }

    # verify=False: 在发送https请求的时候，关闭证书认证
    response = session.post(url=captcha_url, data=post_params, headers=headers, verify=False)
    json_obj = json.loads(response.text)
    if 'success' in json_obj:
        print('输入验证码正确')
        return True
    else:
        print('输入验证码不正确')
        return False


if __name__ == '__main__':
    zhihu_login()
    # res = session.get('https://www.zhihu.com/', headers=headers, verify=False).text
    # print(res)



# [SSL: CERTIFICATE_VERIFY_FAILED]: 在requests发送https请求时，出现的证书认证失败，解决办法：verify=False
# InsecureRequestWarning: Unverified HTTPS request is being made. Adding certificate verification is strongly advised. See: https://urllib3.readthedocs.io/en/latest/advanced-usage.html#ssl-warnings
#   InsecureRequestWarning)