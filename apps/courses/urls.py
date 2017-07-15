#coding:utf-8

__author__ = 'ChangShan Hu'
__date__ = '2017/6/25 22:52'


from django.conf.urls import url

from .views import CourseListView, CourseDetailView, CourseInfoView, CourseCommentView, Add_CommentView

urlpatterns = [
	# 公开课列表
	url(r'^list/$', CourseListView.as_view(), name='course_list'),

	# 课程详情
	url(r'^detail/(?P<course_id>\d+)$', CourseDetailView.as_view(), name='course_detail'),

	# 课程信息
	url(r'^info/(?P<course_id>\d+)$', CourseInfoView.as_view(), name='course_info'),

	# 课程评论
	url(r'^comment/(?P<course_id>\d+)$', CourseCommentView.as_view(), name='course_comment'),

	# 添加评论
	url(r'^add_comment/$', Add_CommentView.as_view(), name='add_comment'),
]