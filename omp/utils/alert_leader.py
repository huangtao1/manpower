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

# db_info = {'ip': '192.168.9.52', 'user': 'root', 'password': 'Aa123456', 'db_name': 'omp', 'port': 27}
yesterday = (datetime.datetime.now() + datetime.timedelta(days=-1)).strftime("%Y-%m-%d")
print(yesterday)

db_info = {'ip': '192.168.8.240', 'user': 'root', 'password': '123456', 'db_name': 'omp', 'port': 3306}


def check_user_hour():
    mydb = Mydb(host=db_info['ip'], user_name=db_info['user'], password=db_info['password'], db_name=db_info['db_name'],
                port=db_info['port'])
    all_user_sql = "SELECT id,display_name,organize_id from omp_user WHERE active=1"
    get_hour_sql = "SELECT SUM(hour) FROM omp_hours WHERE user_id={0} AND day='{1}'"

    all_users = mydb.search_info(all_user_sql)
    # 未达到8h的信息
    no_enough_users = []
    table_body = '<html><body><h4>Dear all:</h4><h4>%s日manpower统计中,工时未达到8小时的情况如下:</h4><table border="1" cellspacing="0" cellpadding="0"><thead><tr><th>姓名</th><th>工时</th></tr></thead>' % yesterday
    for user in all_users:
        if user['display_name'] in ["田勇"]:
            continue
        user_hour = mydb.search_info(get_hour_sql.format(user['id'], yesterday))
        if not user_hour[0]['SUM(hour)']:
            # 没填工时
            hour_info = {'name': user['display_name'], 'hour': 0}
            no_enough_users.append(hour_info)
        elif user_hour[0]['SUM(hour)'] < 8:
            hour_info = {'name': user['display_name'], 'hour': user_hour[0]['SUM(hour)']}
            no_enough_users.append(hour_info)
    for no_enough_user in no_enough_users:
        table_body = table_body + '<tr><td width="300" align="center">{0}</td><td width="300" align="center">{1}</td></tr>'.format(
            no_enough_user['name'],
            no_enough_user['hour'])
    table_body = table_body + '</table><h4>请及时前往<a href="http://manpower.oraro.net">ManPower</a>填写!!!<h4>Best Regards<br/>Manpower@oraro.net</body></html>'
    if len(no_enough_users) > 0:
        send_mail(user='huangtao', msg=table_body)


def send_mail(user, msg):
    # 设置服务器、用户名、口令及邮箱的后缀
    mail_host = 'smtp.263.net'
    mail_user = 'jenkins@oraro.net'
    mail_pass = 'Aa123456'
    sender = "jenkins@oraro.net"
    user = user + '@oraro.net'
    msg_root = MIMEMultipart()
    # 解决中文乱码
    all_msg = msg
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
