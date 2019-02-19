#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Created by huangtao@oraro
from Mydb import Mydb
import datetime
import smtplib
# 多个MIME对象的集合
from email.mime.multipart import MIMEMultipart
# MIME文本对象
from email.mime.text import MIMEText
from email.header import Header
import time

db_info = {'ip': '192.168.9.52', 'user': 'root', 'password': 'Aa123456', 'db_name': 'omp', 'port': 27}
yesterday = (datetime.datetime.now() + datetime.timedelta(days=-4)).strftime("%Y-%m-%d")
print(yesterday)


# db_info = {'ip': '192.168.8.240', 'user': 'root', 'password': '123456', 'db_name': 'omp', 'port': 3306}


def check_user_hour():
    mydb = Mydb(host=db_info['ip'], user_name=db_info['user'], password=db_info['password'], db_name=db_info['db_name'],
                port=db_info['port'])
    all_user_sql = "SELECT id,username,organize_id from omp_user"
    get_hour_sql = "SELECT `hour` FROM omp_hours WHERE user_id={0} AND day='{1}'"
    get_user_leader_sql = "SELECT username FROM omp_user WHERE organize_id={0} AND rank='leader'"

    all_users = mydb.search_info(all_user_sql)
    for user in all_users:
        user_hour = mydb.search_info(get_hour_sql.format(user['id'], yesterday))
        if user_hour:
            # 填了,但是工时没有达到8h
            pass
        else:

            # 没有填写manpower
            leader_name = mydb.search_info(get_user_leader_sql.format(user['organize_id']))[0]['username']
            print(leader_name)
            # 发送邮件提醒
            send_mail(user=user['username'],cc_user=leader_name)


def send_mail(user, cc_user):
    # 设置服务器、用户名、口令及邮箱的后缀
    mail_host = 'smtp.263.net'
    mail_user = 'jenkins@oraro.net'
    mail_pass = 'Aa123456'
    sender = "jenkins@oraro.net"
    user = user + '@oraro.net'
    cc_user = cc_user + '@oraro.net'
    msg_root = MIMEMultipart()
    # 解决中文乱码
    all_msg = ''
    att_text = MIMEText(u'%s' % all_msg, 'html', 'UTF-8')
    # 添加邮件正文
    msg_root.attach(att_text)

    # 发件人
    msg_root['from'] = sender
    # 邮件标题
    msg_root['Subject'] = Header("[ManPower][%s工时计算异常提醒]" % yesterday, 'utf-8')
    # 设置时间
    msg_root['Date'] = time.ctime(time.time())
    msg_root['To'] = ';'.join([user])
    msg_root['Cc'] = ';'.join([cc_user])

    # 群发邮件
    smtp = smtplib.SMTP(mail_host, 25)
    smtp.login(mail_user, mail_pass)

    smtp.sendmail(sender, [user], msg_root.as_string())
    # 休眠5秒
    time.sleep(5)
    # 断开与服务器的连接
    smtp.quit()


if __name__ == '__main__':
    check_user_hour()
