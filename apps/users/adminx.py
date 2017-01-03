# _*_ coding:utf-8 _*_

import xadmin
from xadmin.views import BaseAdminView,CommAdminView
from .models import EmailVerifyRecord, Banner

__author__ = 'supan'
__date__ = '2017/1/2 20:06'


class EmaiVerifyRecordAdmin(object):
    list_display = ['code', 'email', 'send_type', 'send_time']
    search_fields = ['code', 'email', 'send_type']
    list_filter = ['code', 'email', 'send_type', 'send_time']


class BaseSetting(object):
    enable_themes = True
    use_bootswatch = True

class GlobalSettings(object):
    site_title = "慕学后台管理系统"
    site_footer = "慕学在线网"
    menu_style = "accordion"


class BannerAdmin(object):
    list_display = ['title', 'image', 'url', 'index', 'add_time']
    search_fields = ['title', 'image', 'url', 'index']
    list_filter = ['title', 'image', 'url', 'index', 'add_time']


xadmin.site.register(EmailVerifyRecord, EmaiVerifyRecordAdmin)
xadmin.site.register(Banner, BannerAdmin)
xadmin.site.register(BaseAdminView,BaseSetting)
xadmin.site.register(CommAdminView,GlobalSettings)