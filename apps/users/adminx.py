#coding:utf-8
from models import *
import xadmin
from xadmin	import views

__author__ = 'ChangShan Hu'
__date__ = '2017/6/11 21:34'

class EmailVerifyRecordAdmin(object):
	list_display = ['code', 'email', 'send_type', 'send_time']
	search_fields = ['code', 'email', 'send_type']
	list_filter = ['code', 'email', 'send_type', 'send_time']

class BannerAdmin(object):
	list_display = ['title', 'image', 'url', 'index', 'add_time']
	search_fields = ['title', 'image', 'url', 'index']
	list_filter = ['title', 'image', 'url', 'index', 'add_time']


class BaseSetting(object):
	enable_themes = True
	use_bootswatch = True


class GlobalSetting(object):
	site_title = "慕学后台管理系统"
	site_footer = "慕学在线网"
	menu_style = "accordion"


xadmin.site.register(EmailVerifyRecord, EmailVerifyRecordAdmin)
xadmin.site.register(Banner, BannerAdmin)

xadmin.site.register(views.BaseAdminView, BaseSetting)
xadmin.site.register(views.CommAdminView, GlobalSetting)
