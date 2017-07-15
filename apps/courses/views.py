# coding:utf-8
from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import View
from pure_pagination import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q

from .models import Course, CourseOrg, CourseResource
from operations.models import UserFavorite, CourseComments, UserCourse
from utils.mixin_utils import LoginRequiredMixin
# Create your views here.


class CourseListView(View):
	"""
	公开课列表显示
	"""
	def get(self, request):
		all_courses = Course.objects.all().order_by('-add_time')
		hot_courses = all_courses.order_by('-click_nums')[:3]
		# 课程搜索
		keywords = request.GET.get('keywords', '')
		if keywords:
			all_courses = all_courses.filter(Q(name__icontains=keywords)|Q(desc__icontains=keywords)|Q(detail__icontains=keywords))
		# 课程排序
		sort = request.GET.get('sort', '')
		if sort:
			if sort == 'hot':
				all_courses = all_courses.order_by('-click_nums')
			elif sort == 'students':
				all_courses = all_courses.order_by('-stu_nums')
		# 课程分页
		try:
			page = request.GET.get('page', 1)
		except PageNotAnInteger:
			page = 1
		p = Paginator(all_courses, 3, request=request)
		courses = p.page(page)
		return render(request, 'course-list.html', {
			'all_courses': courses,
			'hot_courses': hot_courses,
			'sort': sort,
		})


class CourseDetailView(View):
	"""
	课程详情页
	"""
	def get(self, request, course_id):
		course = Course.objects.get(id=int(course_id))
		course_org = course.course_org
		# 课程点击数+1
		course.click_nums += 1
		course.save()
		# 用户是否已收藏课程和机构
		has_fav_course = False
		has_fav_org = False
		if request.user.is_authenticated():
			# 课程是否收藏
			if UserFavorite.objects.filter(user=request.user, fav_id=course.id, fav_type=1):
				has_fav_course = True
			elif UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
				has_fav_org = True

		# 相关课程推荐
		tag = course.tag
		if tag:
			related_courses = Course.objects.filter(tag=tag)[:1]
		else:
			related_courses = []
		return render(request, 'course-detail.html', {
			'course': course,
			'course_org': course_org,
			'related_courses': related_courses,
			'has_fav_course': has_fav_course,
			'has_fav_org': has_fav_org,
		})


class CourseInfoView(LoginRequiredMixin, View):
	"""
	课程章节信息
	"""
	def get(self, request, course_id):
		course = Course.objects.get(id=int(course_id))
		course.stu_nums += 1
		course.save()
		all_resource = CourseResource.objects.filter(course=course)
		# 关联用户与课程
		user_course = UserCourse.objects.filter(user=request.user, course=course)
		if not user_course:
			user_course = UserCourse(user=request.user, course=course)
			user_course.save()
		#用户学过其它课程
		user_courses = UserCourse.objects.filter(course=course)
		users_id = [user_course.user_id for user_course in user_courses]
		courses  = UserCourse.objects.filter(user_id__in=users_id)
		courses_id = [course.course_id for course in courses]
		related_courses = Course.objects.filter(id__in=courses_id).order_by('-click_nums')[:3]
		return render(request, 'course-video.html', {
			'course': course,
			'all_resource': all_resource,
			'related_courses': related_courses,
		})


class CourseCommentView(View):
	"""
	课程评论
	"""
	def get(self, request, course_id):
		course = Course.objects.get(id=int(course_id))
		all_resource = CourseResource.objects.filter(course=course)
		all_comments= CourseComments.objects.filter(course=course)
		all_comments = all_comments.order_by('-add_time')
		return render(request, 'course-comment.html', {
			'course': course,
			'all_resource': all_resource,
			'all_comments': all_comments,
		})


class Add_CommentView(View):
	"""
	添加课程评论
	"""
	def post(self, request):
		if not request.user.is_authenticated():
			return HttpResponse('{"status":"fail", "msg":"用户未登录"}', content_type='application/json')
		course_id = request.POST.get('course_id', 0)
		comments = request.POST.get('comments', '')
		if course_id>0 and comments:
			to_add_comment = CourseComments()
			to_add_comment.user = request.user
			to_add_comment.course = Course.objects.get(id=int(course_id))
			to_add_comment.comment = comments
			to_add_comment.save()
			return HttpResponse('{"status":"success", "msg":"添加成功"}', content_type='application/json')
		else:
			return HttpResponse('{"status":"fail", "msg":"添加失败"}', content_type='application/json')