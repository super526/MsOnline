# _*_ coding:utf-8 _*_
__author__ = 'supan'
__date__ = '2017/1/8 17:45'
from django.core.mail import send_mail
from random import Random

from users.models import EmailVerifyRecord
from MsOnline.settings import EMAIL_FROM


def random_str(randomlength=8):
    str = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    length = len(chars) - 1
    random = Random()
    for i in range(randomlength):
        str += chars[random.randint(0, length)]
    return str


# 发送邮件处理类
def send_register_email(email, send_type="register"):
    email_record = EmailVerifyRecord()
    verify_code = random_str(16)
    email_record.code = verify_code
    email_record.email = email
    email_record.send_type = send_type
    email_record.save()

    email_title = ""
    email_body = ""

    if send_type == "register":
        email_title = "慕学在线网注册激活链接"
        email_body = "请点击下面的链接激活你的账号:http://127.0.0.1:8000/active/{0}".format(verify_code)
        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
        if send_status:
            pass
