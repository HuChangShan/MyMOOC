# coding:utf-8
from __future__ import unicode_literals
from datetime import datetime

from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class UserProfile(AbstractUser):
	nick_name = models.CharField(max_length=60, default="", verbose_name="昵称")
	image = models.ImageField(max_length=100, upload_to='image/%Y/%m', default="image/default.png", verbose_name="用户头像")
	gender = models.CharField(max_length=6, choices=(('male', "男"), ('female', "女")), verbose_name="性别")
	birthday = models.DateField(verbose_name="生日", null=True, blank=True)
	address = models.CharField(max_length=100, verbose_name="用户地址")
	mobile = models.CharField(max_length=20, null=True, blank=True, verbose_name="手机号码")

	class Meta:
		verbose_name = "用户信息"
		verbose_name_plural = verbose_name

	def __unicode__(self):
		return self.username

	def get_unread_nums(self):
		from operations.models import UserMessage
		number = UserMessage.objects.filter(user=self.id, has_read=False).count()
		return number


class EmailVerifyRecord(models.Model):
	code = models.CharField(max_length=20, verbose_name="验证码")
	email = models.EmailField(max_length=50, verbose_name="验证邮箱")
	send_type = models.CharField(max_length=10, choices=(('register', "注册"), ('forget', "找回密码"),
								('update', "修改邮箱")), verbose_name="发送类型")
	send_time = models.DateTimeField(default=datetime.now, verbose_name="发送时间")

	class Meta:
		verbose_name = "邮箱验证码"
		verbose_name_plural = verbose_name

	def __unicode__(self):
		return '{0}-{1}'.format(self.code, self.email)


class Banner(models.Model):
	title = models.CharField(max_length=100, verbose_name="标题")
	image = models.ImageField(max_length=100, upload_to="banner/%Y/%m", verbose_name="图片")
	url = models.URLField(max_length=200, verbose_name="访问地址")
	index = models.IntegerField(default=100, verbose_name="顺序")
	add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

	class Meta:
		verbose_name = "轮播图"
		verbose_name_plural = verbose_name

	def __unicode__(self):
		return "轮播图"
