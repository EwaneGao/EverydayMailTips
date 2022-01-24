#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2022/1/23 15：57
# @Author  : 高文俊
# @FileName: main.py
# @Software: PyCharm 2021.3.1

# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import requests
import smtplib
import datetime
from email.mime.text import MIMEText
from email.header import Header
import json
import time
import schedule

# 朋友圈 https://pyq.shadiao.app/api.php
# 彩虹屁 https://chp.shadiao.app/api.php
# Press the green button in the gutter to run the script.
weather_url = "http://t.weather.itboy.net/api/weather/city/"
word_url = "https://pyq.shadiao.app/api.php"
mail_host = "smtp.qq.com"  # 设置服务器
mail_user = "**************"  # 用户名
mail_pass = "**************"  # 口令
sender = '****************'


def GetHoneyWorld():
    honeyword_text = requests.get(word_url).text
    return honeyword_text


def GetMailText(city, honeyword_text):
    now_time = datetime.datetime.now()
    weather_url_get = weather_url + city
    weather_data_dict = requests.get(weather_url_get).json()
    mail_send_str = "每日提醒\n" + now_time.strftime("%Y-%m-%d %H:%M:%S") + "\n" + honeyword_text + "\n今天" + \
                    weather_data_dict['cityInfo']['city'] + "天气为" + weather_data_dict['data']['forecast'][0]['type'] + \
                    "\n温度" + weather_data_dict['data']['wendu'] + "℃" + "\n湿度" + weather_data_dict['data']['shidu'] + \
                    "\n风向" + weather_data_dict['data']['forecast'][0]['fx'] + "风力" + \
                    weather_data_dict['data']['forecast'][0]['fl'] + "\n空气质量" + weather_data_dict['data']['quality'] + \
                    "\n" + weather_data_dict['data']['ganmao'] + "\n" + weather_data_dict['data']['forecast'][0][
                        'notice']
    return mail_send_str


def SendMail(mail_send_str, ResName, Resurl):
    message = MIMEText(mail_send_str, 'plain', 'utf-8')
    message['From'] = Header("老高", 'utf-8')
    message['To'] = Header(ResName, 'utf-8')
    subject = '每日提醒'
    message['Subject'] = Header(subject, 'utf-8')
    smtpObj = smtplib.SMTP()
    smtpObj.connect(mail_host, 587)  # 25 为 SMTP 端口号
    smtpObj.login(mail_user, mail_pass)
    smtpObj.sendmail(sender, Resurl, message.as_string())

def SendTesk():
    mylog = open('./mailtext.log', mode='a', encoding='utf-8')
    with open('./receiver.json', 'r', encoding='utf8') as fp:
        json_data = json.load(fp)

    honeyword_text = GetHoneyWorld()

    for res in json_data['receivers']:
        mail_send_str = GetMailText(res['city'], honeyword_text)
        SendMail(mail_send_str, res['name'], res['mailurl'])
        print(res['name'] + ':' + res['mailurl'])
        print(mail_send_str)
        print("邮件发送成功")
        print(res['name'] + ':' + res['mailurl'], file=mylog)
        print(mail_send_str, file=mylog)
        print("邮件发送成功", file=mylog)
        time.sleep(0.5)

    mylog.close()

if __name__ == "__main__":
    schedule.every().day.at("8:00").do(SendTesk)
    schedule.every().day.at("12:00").do(SendTesk)
    schedule.every().day.at("18:00").do(SendTesk)
    schedule.every().day.at("21:00").do(SendTesk)
    while True:
        schedule.run_pending()  # 运行所有可以运行的任务
        time.sleep(1)