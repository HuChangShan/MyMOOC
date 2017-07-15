# coding:utf-8

import xadmin
from .models import *

__author__ = 'ChangShan Hu'
__date__ = '2017/6/12 13:57'


class CourseResourceInline(object):
	model = CourseResource
	extra = 0


class CourseAdmin(object):
	list_display = ['name', 'desc', 'detail', 'degree', 'learn_time', 'stu_nums', 'fav_nums', 'image', 'click_nums',
					'get_lesson_nums', 'add_time']
	search_fields = ['name', 'degree', 'stu_nums', 'fav_nums', 'click_nums']
	list_filter = ['name', 'desc', 'detail', 'degree', 'learn_time', 'stu_nums', 'fav_nums', 'image', 'click_nums', 'add_time']
	ordering = ['-click_nums']
	readonly_fields = ['click_nums']
	list_editable = ['name', 'degree']
	style_fields = {'detail':'ueditor'}
	inlines = [CourseResourceInline]

	# 在保存课程的时候，增加课程机构的课程数
	def save_model(self):
		obj = self.new_obj
		obj.save()
		if obj.course_org is not None:
			course_org = obj.course_org
			course_org.course_nums += 1
			course_org.save()


class LessonAdmin(object):
	list_display = ['course', 'name', 'add_time']
	search_fields = ['course', 'name']
	list_filter = ['course__name', 'name', 'add_time']


class VideoAdmin(object):
	list_display = ['lesson', 'name', 'add_time']
	search_fields = ['lesson', 'name']
	list_filter = ['lesson', 'name', 'add_time']


class CourseResourceAdmin(object):
	list_display = ['course', 'name', 'download', 'add_time']
	search_fields = ['course', 'name', 'download']
	list_filter = ['course', 'name', 'download', 'add_time']

xadmin.site.register(Course, CourseAdmin)
xadmin.site.register(Lesson, LessonAdmin)
xadmin.site.register(Video, VideoAdmin)
xadmin.site.register(CourseResource, CourseResourceAdmin)
