# _*_ coding:utf-8 _*_
from django.contrib.auth.models import User

import xadmin
from xadmin.layout import Fieldset, Side, Row
from xadmin.layout import Main
from xadmin.plugins.auth import UserAdmin
from xadmin.views import BaseAdminView,CommAdminView
from .models import EmailVerifyRecord, Banner, UserProfile

__author__ = 'supan'
__date__ = '2017/1/2 20:06'

class UserProfileAdmin(UserAdmin):
    """
    用户定制xadmin后台模块的详情页面
    """
    def get_form_layout(self):
        if self.org_obj:
            self.form_layout = (
                Main(
                    Fieldset('',
                             'username', 'password',
                             css_class='unsort no_title'
                             ),
                    Fieldset(_('Personal info'),
                             Row('first_name', 'last_name'),
                             'email'
                             ),
                    Fieldset(_('Permissions'),
                             'groups', 'user_permissions'
                             ),
                    Fieldset(_('Important dates'),
                             'last_login', 'date_joined'
                             ),
                ),
                Side(
                    Fieldset(_('Status'),
                             'is_active', 'is_staff', 'is_superuser',
                             ),
                )
            )
        return super(UserAdmin, self).get_form_layout()



class EmaiVerifyRecordAdmin(object):
    list_display = ['code', 'email', 'send_type', 'send_time']
    search_fields = ['code', 'email', 'send_type']
    list_filter = ['code', 'email', 'send_type', 'send_time']
    model_icon = 'fa fa-user'

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

# xadmin.site.unregister(User)
xadmin.site.register(EmailVerifyRecord, EmaiVerifyRecordAdmin)
xadmin.site.register(Banner, BannerAdmin)
# xadmin.site.register(UserProfile, UserProfileAdmin)
xadmin.site.register(BaseAdminView,BaseSetting)
xadmin.site.register(CommAdminView,GlobalSettings)