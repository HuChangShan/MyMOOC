#coding:utf-8

__author__ = 'ChangShan Hu'
__date__ = '2017/6/16 14:35'
from random import Random

from django.core.mail import send_mail

from users.models import EmailVerifyRecord
from MOOC.settings import EMAIL_FROM

def random_str(randomlength=8):
	str = ''
	chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
	length = len(chars)-1
	random = Random()
	for i in range(randomlength):
		str += chars[random.randint(0, length)]
	return str


def send_register_email(email, send_type='register'):
	email_record = EmailVerifyRecord()
	if send_type == 'update':
		code = random_str(8)
	else:
		code = random_str(8)
	email_record.code = code
	email_record.email = email
	email_record.send_type = send_type
	email_record.save()

	email_title = ''
	email_body = ''

	if send_type == 'register':
		email_title = "慕学在线网注册激活链接"
		email_body = "请点击下面的链接激活你的帐号：http://127.0.0.1:8000/active/{0}".format(email_record.code)

		send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
		if send_status:
			pass

	elif send_type == 'forget':
		email_title = "慕学在线网找回密码链接"
		email_body = "请点击下面的链接重置密码：http://127.0.0.1:8000/reset/{0}".format(email_record.code)
		send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
		if send_status:
			pass

	elif send_type == 'update':
		email_title = "慕学在线网修改邮箱"
		email_body = "邮箱验证码为:{0}".format(email_record.code)
		send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
		if send_status:
			pass