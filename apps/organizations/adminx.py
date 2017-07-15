#coding:utf-8
from .models import CityDict, CourseOrg, Teacher
import xadmin

__author__ = 'ChangShan Hu'
__date__ = '2017/6/11 21:37'


class CityDictAdmin(object):
	list_display = ['name', 'desc', 'add_time']
	search_fields = ['name', 'add_time']
	list_filter = ['name', 'desc', 'add_time']


class CourseOrgAdmin(object):
	list_display = ['name', 'desc', 'click_nums', 'fav_nums']
	search_fields = ['name', 'desc', 'click_nums', 'fav_nums']
	list_filter = ['name', 'desc', 'click_nums', 'fav_nums']


class TeacherAdmin(object):
	list_display = ['org', 'name', 'work_years', 'fav_nums']
	search_fields = ['org', 'name', 'work_years', 'fav_nums']
	list_filter = ['org', 'name', 'work_years', 'fav_nums']


xadmin.site.register(CityDict, CityDictAdmin)
xadmin.site.register(CourseOrg, CourseOrgAdmin)
xadmin.site.register(Teacher, TeacherAdmin)
