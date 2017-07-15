#coding:utf-8

__author__ = 'ChangShan Hu'
__date__ = '2017/6/27 21:06'

from django.conf.urls import url

from .views import UserInfoView, ImageUploadView, UpdatePwdView, SendEmailCodeView, UpdateEmailView, MyCoursesView,\
	MyFavView, FavTeacherView, FavCourseView, MyMessageView


urlpatterns = [
	# 用户个人信息
	url(r'^info/$', UserInfoView.as_view(), name='my_info'),
	# 用户头像修改
	url(r'^image/upload/$', ImageUploadView.as_view(), name='image_upload'),
	# 个人中心修改密码
	url(r'^update/pwd/$', UpdatePwdView.as_view(), name="update_pwd"),
	# 个人中心发送邮箱验证码
	url(r'^sendemail_code/$', SendEmailCodeView.as_view(), name='sendemail_code'),
	# 个人中心修改邮箱
	url(r'^update/email/$', UpdateEmailView.as_view(), name='update_email'),
	# 个人中心我的课程
	url(r'^course/$', MyCoursesView.as_view(), name='my_course'),
	# 个人中心我的收藏-课程机构
	url(r'^fav_org/$', MyFavView.as_view(), name='fav_org'),
	# 个人中心我的收藏-授课教师
	url(r'^fav_teacher/$', FavTeacherView.as_view(), name='fav_teacher'),
	# 个人中心我的收藏-公开课程
	url(r'^fav_course/$', FavCourseView.as_view(), name='fav_course'),
	# 个人中心我的消息
	url(r'^message/$', MyMessageView.as_view(), name='my_message'),
]