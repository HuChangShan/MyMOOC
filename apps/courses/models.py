#coding:utf-8
from __future__ import unicode_literals
from datetime import datetime

from django.db import models
from DjangoUeditor.models import UEditorField

from organizations.models import CourseOrg, Teacher
# Create your models here.


class Course(models.Model):
	name = models.CharField(max_length=50, verbose_name="课程名称")
	desc = models.CharField(max_length=300, verbose_name="课程描述")
	degree = models.CharField(max_length=6, choices=(('cj', "初级"), ('zj', "中级"), ('gj', "高级")), verbose_name="课程难度")
	detail = UEditorField(verbose_name="课程详情", width=600, height=300, imagePath='courses/ueditor/image',
						  filePath='courses/ueditor/file')
	learn_time = models.IntegerField(default=0, verbose_name="学习时长（分钟）")
	is_banner = models.BooleanField(default=False, verbose_name="是否轮播")
	stu_nums = models.IntegerField(default=0, verbose_name="学习人数")
	fav_nums = models.IntegerField(default=0, verbose_name="收藏人数")
	image = models.ImageField(upload_to="course/%Y/%m", max_length=100, verbose_name="课程封面")
	click_nums = models.IntegerField(default=0, verbose_name="点击数")
	add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")
	category = models.CharField(default='', max_length=50, verbose_name="课程类别")
	tag = models.CharField(default='', max_length=20, verbose_name="课程标签")
	need_know = models.CharField(default='', max_length=300, verbose_name="课程须知")
	teacher_tell = models.CharField(default='', max_length=300, verbose_name="老师告诉你能学到什么")
	course_org = models.ForeignKey(CourseOrg, verbose_name="课程机构", null=True, blank=True)
	teacher = models.ForeignKey(Teacher, verbose_name="教师", null=True, blank=True)

	class Meta:
		verbose_name = "课程"
		verbose_name_plural = verbose_name

	def __unicode__(self):
		return self.name

	def get_lesson_nums(self):
		return self.lesson_set.all().count()

	get_lesson_nums.short_description = "章节数"

	def get_learn_user(self):
		return self.usercourse_set.all()[:5]

	def get_lesson(self):
		return self.lesson_set.all()



class Lesson(models.Model):
	name = models.CharField(max_length=100, verbose_name="章节名称")
	add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")
	course = models.ForeignKey(Course, verbose_name="课程")

	class Meta:
		verbose_name = "章节"
		verbose_name_plural = verbose_name

	def __unicode__(self):
		return self.name

	def get_video(self):
		return self.video_set.all()


class Video(models.Model):
	name = models.CharField(max_length=100, verbose_name="视频名称")
	url = models.CharField(max_length=200, default='', verbose_name="访问链接")
	learn_time = models.IntegerField(default=0, verbose_name="学习时长（分钟）")
	add_time = models.DateTimeField(default=datetime.now)
	lesson = models.ForeignKey(Lesson, verbose_name="章节")

	class Meta:
		verbose_name = "视频"
		verbose_name_plural = verbose_name

	def __unicode__(self):
		return self.name


class CourseResource(models.Model):
	name = models.CharField(max_length=100, verbose_name="课程资源名称")
	download = models.FileField(upload_to="courses/resource/%Y/%m", verbose_name="下载文件")
	add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")
	course = models.ForeignKey(Course, verbose_name="课程")

	class Meta:
		verbose_name = "课程资源"
		verbose_name_plural = verbose_name

	def __unicode__(self):
		return self.name
