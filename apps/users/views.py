# coding:utf-8
import json

from django.shortcuts import render, render_to_response
from django.core.urlresolvers import reverse
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q
from django.views.generic import View
from django.contrib.auth.hashers import make_password
from django.http import HttpResponse, HttpResponseRedirect
from pure_pagination import Paginator, PageNotAnInteger

from .models import UserProfile, EmailVerifyRecord, Banner
from .forms import LoginForm, RegisterForm, ForgetForm, ModifyForm, ImageUploadForm, InfoUpdateForm
from utils.email_send import send_register_email
from utils.mixin_utils import LoginRequiredMixin
from operations.models import UserCourse, UserFavorite, UserMessage
from courses.models import Course
from organizations.models import CourseOrg, Teacher
# Create your views here.


class CustomBackend(ModelBackend):

	def authenticate(self, username=None, password=None, **kwargs):
		try:
			user = UserProfile.objects.get(Q(username=username) | Q(email=username))
			if user.check_password(password):
				return user
		except Exception as e:
			return None


class LogoutView(View):
	"""
	用户退出登录
	"""
	def get(self, request):
		logout(request)
		return HttpResponseRedirect(reverse('index'))

class LoginView(View):

	def get(self, request):
		return render(request, 'login.html', {})

	def post(self, request):
		login_form = LoginForm(request.POST)
		if login_form.is_valid():
			user_name = request.POST.get('username', '')
			pass_word = request.POST.get('password', '')
			user = authenticate(username=user_name, password=pass_word)
			if user is not None:
				if user.is_active:
					login(request, user)
					return HttpResponseRedirect(reverse('index'))
				else:
					return render(request, 'login.html', {'msg': "用户未激活"})
			else:
				return render(request, 'login.html', {'msg': "用户名或密码错误"})
		else:
			return render(request, 'login.html', {'login_form': login_form})


class RegisterView(View):
	"""用户注册"""
	def get(self, request):
		register_form = RegisterForm()
		return render(request, 'register.html', {'register_form': register_form})

	def post(self, request):
		register_form = RegisterForm(request.POST)
		if register_form.is_valid():
			user_name = request.POST.get('email', '')
			if UserProfile.objects.get(email=user_name):
				return render(request, 'register.html', {'register_form': register_form, 'msg': "用户已存在"})
			pass_word = request.POST.get('password', '')
			user_profile = UserProfile()
			user_profile.username = user_name
			user_profile.email = user_name
			user_profile.is_active = False
			user_profile.password = make_password(pass_word)
			user_profile.save()
			# 注册消息
			message = UserMessage(user=user_profile.id, message="欢迎注册慕课在线网！")
			message.save()
			# 发送注册邮件
			send_register_email(user_name, 'register')
			return render(request, 'login.html')
		else:
			return render(request, 'register.html', {'register_form': register_form})


class ActiveUserView(View):

	def get(self, request, active_code):
		all_records = EmailVerifyRecord.objects.filter(code=active_code)
		if all_records:
			for record in all_records:
				email = record.email
				user = UserProfile.objects.get(email=email)
				user.is_active = True
				user.save()
		else:
			return render(request, 'active_fail.html')
		return render(request, 'login.html')


class ForgetPwdView(View):

	def get(self, request):
		forget_form = ForgetForm()
		return render(request, 'forgetpwd.html', {'forget_form': forget_form})

	def post(self, request):
		forget_form = ForgetForm(request.POST)
		if forget_form.is_valid():
			user_name = request.POST.get('email', '')
			user = UserProfile.objects.get(email=user_name)
			if user is not None:
				send_register_email(user_name, 'forget')
				return render(request, 'send_success.html')
			else:
				return render(request, 'forgetpwd.html', {'forget_form': forget_form, 'msg': "用户不存在"})
		else:
			return render(request, 'forgetpwd.html', {'forget_form': forget_form})


class ResetPwdView(View):

	def get(self, request, active_code):
		all_records = EmailVerifyRecord.objects.filter(code=active_code)
		if all_records:
			for record in all_records:
				email = record.email
				return render(request, 'password_reset.html', {'emial': email})
		else:
			return render(request, 'active_fail.html')


class ModifyPwdView(View):
	"""
	未登录修改密码
	"""
	def post(self, request, active_code):
		modify_form = ModifyForm(request.POST)
		if modify_form.is_valid():
			email = request.POST.get('email', '')
			first = request.POST.get('pwd_first', '')
			second = request.POST.get('pwd_second', '')
			if first == second:
				user = UserProfile.objects.get(email=email)
				user.password = make_password(second)
				user.save()
				return render(request, 'login.html')
			else:
				return render(request, 'password_reset.html', {'email': email, 'msg': "输入密码不一致！"})
		else:
			email = request.POST.get('email', '')
			return render(request, 'password_reset.html', {'email': email, 'msg': "输入密码不合法"})


class UserInfoView(LoginRequiredMixin, View):
	"""
	用户个人信息
	"""
	def get(self, request):
		return render(request, 'usercenter-info.html', {})

	def post(self, request):
		user_info = InfoUpdateForm(request.POST, instance=request.user)
		if user_info.is_valid():
			user_info.save()
			return HttpResponse('{"status":"success"}', content_type='application/json')
		else:
			return HttpResponse(json.dumps(user_info.errors), content_type='application/json')


class ImageUploadView(LoginRequiredMixin, View):
	"""
	用户头像修改
	"""
	def post(self, request):
		imageupload_form = ImageUploadForm(request.POST, request.FILES, instance=request.user)
		if imageupload_form.is_valid():
			imageupload_form.save()
			return HttpResponse('{"status":"success"}', content_type='application/json')
		else:
			return HttpResponse('{"status":"fail"}', content_type='application/json')


class UpdatePwdView(LoginRequiredMixin, View):
	"""
	个人中心修改密码
	"""
	def post(self, request):
		modify_form = ModifyForm(request.POST)
		if modify_form.is_valid():
			first = request.POST.get('pwd_first', '')
			second = request.POST.get('pwd_second', '')
			if first == second:
				user = request.user
				user.password = make_password(second)
				user.save()
				return HttpResponse('{"status":"success"}', content_type='application/json')
			else:
				return HttpResponse('{"status":"fail", "msg":"密码不一致"}', content_type='application/json')
		else:
			return HttpResponse(json.dumps(modify_form.errors), content_type='application/json')


class SendEmailCodeView(LoginRequiredMixin, View):
	"""
	个人中心发送邮箱验证码
	"""
	def get(self, request):
		email = request.GET.get('email', '')
		if UserProfile.objects.filter(email=email):
			return HttpResponse('{"email":"邮箱已存在"}', content_type='application/json')
		send_register_email(email, 'update')
		return HttpResponse('{"status":"success"}', content_type='application/json')


class UpdateEmailView(LoginRequiredMixin, View):
	"""
	个人中心修改邮箱
	"""
	def post(self, request):
		email = request.POST.get('email', '')
		code = request.POST.get('code', '')
		record = EmailVerifyRecord.objects.filter(email=email, code=code, send_type='update')
		if record:
			user = request.user
			user.email = email
			user.save()
			return HttpResponse('{"status":"success"}', content_type='application/json')
		else:
			return HttpResponse('{"email":"验证码不正确"}', content_type='application/json')


class MyCoursesView(View):
	"""
	个人中心我的课程
	"""
	def get(self, request):
		suit_records = UserCourse.objects.filter(user=request.user)
		all_courses_id = [record.course_id for record in suit_records]
		all_courses = Course.objects.filter(id__in=all_courses_id)
		return render(request, 'usercenter-mycourse.html', {
			'all_courses': all_courses,
		})


class MyFavView(View):
	"""
	个人中心我的收藏-课程机构
	"""
	def get(self, request):
		all_records = UserFavorite.objects.filter(user=request.user, fav_type=2)
		fav_ids = [record.fav_id for record in all_records]
		all_orgs = CourseOrg.objects.filter(id__in=fav_ids)
		return render(request, 'usercenter-fav-org.html', {
			'all_orgs': all_orgs,
		})


class FavTeacherView(View):
	"""
	个人中心我的收藏-授课教师
	"""
	def get(self, request):
		all_records = UserFavorite.objects.filter(user=request.user, fav_type=3)
		fav_ids = [record.fav_id for record in all_records]
		all_teachers = Teacher.objects.filter(id__in=fav_ids)
		return render(request, 'usercenter-fav-teacher.html', {
			'all_teachers': all_teachers,
		})


class FavCourseView(View):
	"""
	个人中心我的收藏-公开课程
	"""
	def get(self, request):
		all_records = UserFavorite.objects.filter(user=request.user, fav_type=1)
		fav_ids = [record.fav_id for record in all_records]
		all_courses = Course.objects.filter(id__in=fav_ids)
		return render(request, 'usercenter-fav-course.html', {
			'all_courses': all_courses,
		})


class MyMessageView(View):
	"""
	个人中心我的消息
	"""
	def get(self, request):
		all_messages = UserMessage.objects.filter(user=request.user.id).order_by('-add_time')
		all_unread_messages = UserMessage.objects.filter(user=request.user.id, has_read=False)
		for unread_message in all_unread_messages:
			unread_message.has_read = True
			unread_message.save()
		# 对消息进行分页
		try:
			page = request.GET.get('page', 1)
		except PageNotAnInteger:
			page = 1
		p = Paginator(all_messages, 3, request=request)
		messages = p.page(page)
		return render(request, 'usercenter-message.html', {
			'all_messages': messages,
		})


class IndexView(View):
	# 慕课网首页
	def get(self, request):
		all_banners = Banner.objects.all()
		banner_courses = Course.objects.filter(is_banner=True)[:3]
		courses = Course.objects.filter(is_banner=False).order_by('-add_time')[:6]
		course_orgs = CourseOrg.objects.all()[:15]
		return render(request, 'index.html', {
			'all_banners': all_banners,
			'courses': courses,
			'banner_courses': banner_courses,
			'course_orgs': course_orgs,
		})


def page_not_found(request):
	# 全局404配置
	response = render_to_response('404.html', {})
	response.status_code = 404
	return response


def page_error(request):
	# 全局500配置
	response = render_to_response('500.html', {})
	response.status_code = 500
	return response