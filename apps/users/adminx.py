# _*_ coding:utf-8 _*_

import xadmin

from .models import EmailVerifyRecord, Banner

__author__ = 'supan'
__date__ = '2017/1/2 20:06'

class EmaiVerifyRecordAdmin(object):
    list_display = ['code', 'email', 'send_type', 'send_time']
    search_fields = ['code', 'email', 'send_type']
    list_filter = ['code', 'email', 'send_type', 'send_time']


class BannerAdmin(object):
    list_display = ['title', 'image', 'url', 'index', 'add_time']
    search_fields = ['title', 'image', 'url', 'index']
    list_filter = ['title', 'image', 'url', 'index', 'add_time']


xadmin.site.register(EmailVerifyRecord, EmaiVerifyRecordAdmin)
xadmin.site.register(Banner, BannerAdmin)
