'''
author: Jacob
describe: 获取上海大学学生最新课表
'''

import json

import requests
from bs4 import BeautifulSoup


def get_course_table():
    stdid = input('请输入学号: ')
    password = input('请输入密码: ')
    if stdid and password:
        Login_Data = {'j_username': stdid,
                      'j_password': password}
        s = requests.session()
        login(s, Login_Data)


def login(s, Login_Data):
    # POST 登陆
    print('正在登陆')
    url_login = 'http://xk.autoisp.shu.edu.cn:8080'
    a = s.get(url_login).content.decode()
    # 登录界面
    # print(a)
    # print("===================================================")
    soup = BeautifulSoup(a, 'lxml')
    url_sso = soup.body.form['action']
    data = {}
    for input_tag in soup.body.form.find_all('input'):
        data[input_tag['name']] = input_tag['value']
    b = s.post(url_sso, data)
    c = s.post(b.url, Login_Data)
    soup1 = BeautifulSoup(c.content, 'lxml')
    data = {}
    for input_tag in soup1.body.form.find_all('input'):
        if input_tag.get('name', False):
            data[input_tag['name']] = input_tag['value']
    s.post(soup1.body.form['action'], data)
    print('登录成功')
    print('正在获取课表....')
    # =======login-finished========
    url_course_info = "http://cj.shu.edu.cn/StudentPortal/StudentSchedule"
    url_course_table = "http://cj.shu.edu.cn/StudentPortal/CtrlStudentSchedule"
    course_info = s.get(url_course_info)  # 不知道为什么要访问两次，反正访问就对了
    course_info = s.get(url_course_info)  # 打开教务管理系统点击查看课程信息
    soup_info = BeautifulSoup(course_info.content, "lxml")
    term = soup_info.find_all('option')
    academicTermID = term[-1]['value']  # 获取最新的学期
    # 真正拿到课表
    e = s.post(url_course_table, {'academicTermID': academicTermID})  # 获取最新的课表儿
    # 课表界面
    # print(e.content.decode())
    soup2 = BeautifulSoup(e.content, "lxml")
    class_list = []
    for idx, tr in enumerate(soup2.find_all('tr')):
        classdetail = {}
        if idx != 0 and idx != 1 and idx % 2 != 1:
            tds = tr.find_all('td')
            classdetail['courseId'] = str(tds[0].contents[0]).replace('\n', "").replace('\r', "").replace(' ', "")
            classdetail['name'] = str(tds[1].contents[0]).replace('\n', "").replace('\r', "").replace(' ', "")
            classdetail['teacherId'] = str(tds[2].contents[0]).replace('\n', "").replace('\r', "").replace(' ', "")
            classdetail['teacher'] = str(tds[3].contents[0]).replace('\n', "").replace('\r', "").replace(' ', "")
            classdetail['time'] = str(tds[4].contents[0]).replace('\n', "").replace('\r', "").replace(' ', "")
            classdetail['classroom'] = str(tds[5].contents[0]).replace('\n', "").replace('\r', "").replace(' ', "")
            classdetail['questionTime'] = str(tds[6].contents[0]).replace('\n', "").replace('\r', "").replace(' ', "")
            classdetail['questionRoom'] = str(tds[7].contents[0]).replace('\n', "").replace('\r', "").replace(' ', "")
            class_list.append(classdetail)
    if '课程编号' in e.content.decode():
        print('获取课表成功')
    else:
        print('连接出错了呢,大概是账号密码有问题哦')
        return False
    print(class_list)
    return class_list

get_course_table()
