# encoding:utf-8
from django.shortcuts import render
from django.views.generic import View
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse
from django.db.models import Q

from .models import CourseOrg, CityDict, Teacher
from .forms import UserAskForm
from operations.models import UserFavorite
from courses.models import Course, CourseOrg
from organizations.models import Teacher
# Create your views here.


class OrgView(View):
	"""
	课程机构列表展示功能
	"""
	def get(self, request):

		# 课程机构
		all_orgs = CourseOrg.objects.all()
		hot_orgs = all_orgs.order_by('click_nums')[0:3]
		# 城市
		all_citys = CityDict.objects.all()
		# 机构搜索
		keywords = request.GET.get('keywords', '')
		if keywords:
			all_orgs = all_orgs.filter(Q(name__icontains=keywords) | Q(desc__icontains=keywords))
		# 筛选城市
		city_id = request.GET.get('city', '')
		if city_id:
			all_orgs = all_orgs.filter(city_id=int(city_id))

		# 筛选类别
		category = request.GET.get('ct', '')
		if category:
			all_orgs = all_orgs.filter(category=category)

		# 排序
		sort = request.GET.get('sort', '')
		if sort:
			if sort == 'students':
				all_orgs = all_orgs.order_by('-student_nums')
			elif sort == 'courses':
				all_orgs = all_orgs.order_by('-course_nums')
		org_nums = all_orgs.count()

		# 对课程机构分页
		try:
			page = request.GET.get('page', 1)
		except PageNotAnInteger:
			page = 1

		p = Paginator(all_orgs, 5, request=request)
		orgs = p.page(page)
		return render(request, 'org-list.html', {
			'all_orgs': orgs,
			'all_citys': all_citys,
			'org_nums': org_nums,
			'city_id': city_id,
			'category': category,
			'hot_orgs': hot_orgs,
			'sort': sort,
		})


class AddUserAskView(View):
	"""
	用户添加咨询
	"""
	def post(self, request):
		userask_form = UserAskForm(request.POST)
		if userask_form.is_valid():
			user_ask = userask_form.save(commit=True)
			return HttpResponse("{'status':'success'}", content_type='application/json')
		else:
			return HttpResponse('{"status":"fail", "msg":"添加出错"}', content_type='application/json')


class OrgHomeView(View):
	"""
    机构首页
    """
	def get(self, request, org_id):
		current_page = 'home'
		course_org = CourseOrg.objects.get(id=int(org_id))
		course_org.click_nums += 1
		course_org.save()
		all_courses = course_org.course_set.all()[:3]
		all_teachers = course_org.teacher_set.all()[:1]
		has_fav = False
		if request.user.is_authenticated():
			if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
				has_fav = True
		return render(request, 'org-detail-homepage.html',{
			'all_courses': all_courses,
			'all_teachers': all_teachers,
			'course_org': course_org,
			'current_page': current_page,
			'has_fav': has_fav,
		})


class OrgCourseView(View):
	"""
    机构课程列表
    """
	def get(self, request, org_id):
		current_page = 'course'
		course_org = CourseOrg.objects.get(id=int(org_id))
		all_courses = course_org.course_set.all()
		has_fav = False
		if request.user.is_authenticated():
			if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
				has_fav = True
		return render(request, 'org-detail-course.html',{
			'all_courses': all_courses,
			'course_org': course_org,
			'current_page': current_page,
			'has_fav': has_fav,
		})


class OrgDescView(View):
	"""
	机构介绍
	"""
	def get(self, request, org_id):
		current_page = 'desc'
		course_org = CourseOrg.objects.get(id=int(org_id))
		has_fav = False
		if request.user.is_authenticated():
			if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
				has_fav = True
		return render(request, 'org-detail-desc.html', {
			'course_org': course_org,
			'current_page': current_page,
			'has_fav': has_fav,
		})


class OrgTeacherView(View):
	"""
	机构教师
	"""
	def get(self, request, org_id):
		current_page = 'teacher'
		course_org = CourseOrg.objects.get(id=int(org_id))
		all_teachers = course_org.teacher_set.all()
		has_fav = False
		if request.user.is_authenticated():
			if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
				has_fav = True
		return render(request, 'org-detail-teachers.html',{
			'course_org': course_org,
			'all_teachers': all_teachers,
			'current_page': current_page,
			'has_fav': has_fav,
		})


class AddFavView(View):
	"""
	用户收藏，取消收藏
	"""
	def post(self, request):
		fav_id = request.POST.get('fav_id', 0)
		fav_type = request.POST.get('fav_type', 0)

		if not request.user.is_authenticated():
			return HttpResponse('{"status":"fail", "msg":"用户未登录"}', content_type='application/json')

		added_fav = UserFavorite.objects.filter(user=request.user, fav_id=int(fav_id), fav_type=int(fav_type))
		# 用户已经收藏，则判断为取消收藏
		if added_fav:
			added_fav.delete()
			if int(fav_type) == 1:
				course = Course.objects.get(id=int(fav_id))
				course.fav_nums -= 1
				if course.fav_nums < 0:
					course.fav_nums = 0
				course.save()
			elif int(fav_type) == 2:
				org = CourseOrg.objects.get(id=int(fav_id))
				org.fav_nums -= 1
				if org.fav_nums < 0:
					org.fav_nums = 0
				org.save()
			elif int(fav_type) == 3:
				teacher = Teacher.objects.get(id=int(fav_id))
				teacher.fav_nums -= 1
				if teacher.fav_nums < 0:
					teacher.fav_nums = 0
				teacher.save()
			return HttpResponse('{"status":"success", "msg":"收藏"}', content_type='application/json')
		else:
			add_fav = UserFavorite()
			if int(fav_id)>0 and int(fav_type)>0:
				add_fav.user = request.user
				add_fav.fav_id = int(fav_id)
				add_fav.fav_type = int(fav_type)
				add_fav.save()
				if int(fav_type) == 1:
					course = Course.objects.get(id=int(fav_id))
					course.fav_nums += 1
					course.save()
				elif int(fav_type) == 2:
					org = CourseOrg.objects.get(id=int(fav_id))
					org.fav_nums += 1
					org.save()
				elif int(fav_type) == 3:
					teacher = Teacher.objects.get(id=int(fav_id))
					teacher.fav_nums += 1
					teacher.save()
				return HttpResponse('{"status":"success", "msg":"已收藏"}', content_type='application/json')
			else:
				return HttpResponse('{"status":"fail", "msg":"收藏出错"}', content_type='application/json')


class TeacherListView(View):
	"""
	授课教师列表
	"""
	def get(self, request):
		all_teachers = Teacher.objects.all()
		hot_teachers = Teacher.objects.all().order_by('-fav_nums')[:3]
		all_nums = all_teachers.count()
		# 机构搜索
		keywords = request.GET.get('keywords', '')
		if keywords:
			all_teachers = all_teachers.filter(Q(name__icontains=keywords) | Q(work_position__icontains=keywords) | Q(work_company__icontains=keywords))
		sort = request.GET.get('sort', '')
		if sort:
			if sort == 'hot':
				all_teachers = all_teachers.order_by('-click_nums')
		try:
			page = request.GET.get('page', '1')
		except PageNotAnInteger:
			page = 1
		p = Paginator(all_teachers, 3, request=request)
		teachers = p.page(page)
		return render(request, 'teachers-list.html', {
			'all_teachers': teachers,
			'all_nums': all_nums,
			'hot_teachers': hot_teachers,
			'sort': sort,
		})


class TeacherDetailView(View):
	def get(self, request, teacher_id):
		teacher = Teacher.objects.get(id=int(teacher_id))
		# 增加教师的点击数
		teacher.click_nums += 1
		teacher.save()
		hot_teachers = Teacher.objects.all().order_by('-fav_nums')[:3]
		org = teacher.org
		all_courses = teacher.course_set.all()
		has_fav_teacher = False
		has_fav_org = False
		if request.user.is_authenticated():
			# 教师是否收藏
			if UserFavorite.objects.filter(user=request.user, fav_id=teacher.id, fav_type=3):
				has_fav_teacher = True
			# 机构是否收藏
			if UserFavorite.objects.filter(user=request.user, fav_id=org.id, fav_type=2):
				has_fav_org = True
			# 增加教师的点击数
			org.click_nums += 1
			org.save()
		return render(request, 'teacher-detail.html', {
			'teacher': teacher,
			'hot_teachers': hot_teachers,
			'org': org,
			'all_courses': all_courses,
			'has_fav_teacher': has_fav_teacher,
			'has_fav_org': has_fav_org,
		})