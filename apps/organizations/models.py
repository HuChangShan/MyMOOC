# coding:utf-8
from __future__ import unicode_literals
from datetime import datetime

from django.db import models

# Create your models here.


class CityDict(models.Model):
	name = models.CharField(max_length=20, verbose_name="城市名称")
	desc = models.CharField(max_length=200, verbose_name="城市介绍")
	add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

	class Meta:
		verbose_name = "城市"
		verbose_name_plural = verbose_name

	def __unicode__(self):
		return self.name


class CourseOrg(models.Model):
	name = models.CharField(max_length=50, verbose_name="机构名称")
	desc = models.TextField(verbose_name="机构描述")
	category = models.CharField(max_length=20, verbose_name="机构类别",
								choices=(('pxjg', "培训机构"), ('gx', "高校"), ('gr', "个人")),
								default='pxjg')
	tag = models.CharField(max_length=10, default="全国知名", verbose_name="机构标签")
	click_nums = models.IntegerField(default=0, verbose_name="点击数")
	fav_nums = models.IntegerField(default=0, verbose_name="收藏数")
	student_nums = models.IntegerField(default=0, verbose_name="学习人数")
	course_nums = models.IntegerField(default=0, verbose_name="课程数")
	image = models.ImageField(max_length=100, upload_to='org/%Y/%m', verbose_name="机构图片")
	address = models.CharField(max_length=150, verbose_name="机构地址")
	city = models.ForeignKey(CityDict, verbose_name="所在城市")
	add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

	class Meta:
		verbose_name = "课程机构"
		verbose_name_plural = verbose_name

	def __unicode__(self):
		return self.name

	def get_teacher_nums(self):
		return self.teacher_set.all().count()


class Teacher(models.Model):
	name = models.CharField(max_length=50, verbose_name="教师姓名")
	image = models.ImageField(default='', max_length=100, upload_to='org/%Y/%m', verbose_name="教师头像")
	age = models.IntegerField(default=0, verbose_name="年龄")
	work_years = models.IntegerField(default=0, verbose_name="工作年限")
	work_company = models.CharField(max_length=50, verbose_name="就职公司")
	work_position = models.CharField(max_length=50, verbose_name="公司职位")
	points = models.CharField(max_length=50, verbose_name="教学特点")
	click_nums = models.IntegerField(default=0, verbose_name="点击数")
	fav_nums = models.IntegerField(default=0, verbose_name="收藏数")
	add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")
	org = models.ForeignKey(CourseOrg, verbose_name="所属机构")

	class Meta:
		verbose_name = "教师"
		verbose_name_plural = verbose_name

	def __unicode__(self):
		return self.name
