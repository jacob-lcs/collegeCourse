'''
author: Jacob
describe: 获取青岛大学学生最新课表
'''

from io import BytesIO
from pytesseract import image_to_string
import requests
from PIL import Image
import time


def get_course_table():
    stdid = input('请输入学号: ')
    password = input('请输入密码: ')
    if stdid and password:
        Login_Data = {'j_username': stdid,
                      'j_password': password}
        s = requests.session()
        login(s, Login_Data)


def login(s, Login_Data):
    print('正在登陆')
    url_login = 'http://jw.qdu.edu.cn/academic/student/currcourse/currcourse.jsdo?year=39&term=2'
    code_url = 'http://jw.qdu.edu.cn/academic/getCaptcha.do?0.3851235093964869'
    s.get(url_login).content.decode("utf8", "ignore")
    res = s.get(code_url)
    byte_stream = BytesIO(res.content)
    verification_code = get_verification_code(byte_stream)
    is_right_code = s.post(
        "http://jw.qdu.edu.cn/academic/checkCaptcha.do?captchaCode=" + verification_code).content.decode('utf8')
    while is_right_code != 'true':
        print(is_right_code)
        print("验证码错误，正在重试")
        time.sleep(1)
        res = s.get(code_url)
        byte_stream = BytesIO(res.content)
        verification_code = get_verification_code(byte_stream)
        is_right_code = s.post(
            "http://jw.qdu.edu.cn/academic/checkCaptcha.do?captchaCode=" + verification_code).content.decode('utf8')
    a = s.post(
        "http://jw.qdu.edu.cn/academic/j_acegi_security_check?j_username=" + Login_Data['j_username'] + "&j_password=" +
        Login_Data['j_password'] + "&j_captcha=" + verification_code)
    print(a.content.decode('utf8', 'ignore'))


def get_verification_code(byte_stream):
    image = Image.open(byte_stream)
    res = image_to_string(image)
    return res.replace(" ", "")


get_course_table()
