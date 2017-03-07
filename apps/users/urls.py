# _*_ coding:utf-8 _*_
from users.views import UserInfoView,UploadImageView, UpdatePwdView, UpdateEmailView, SendEmailCodeView, UserCourseView, \
    UserMessageView

__author__ = 'supan'
__date__ = '2017/3/1 22:03'


from django.conf.urls import url, include

urlpatterns = [
    # 用户个人中心页面
    url(r'^info/$', UserInfoView.as_view(), name="user_info"),
    # 个人中心:我的课程
    url(r'^mycourse/$', UserCourseView.as_view(), name="user_course"),
    # 个人中心:我的消息
    url(r'^mymessage/$', UserMessageView.as_view(), name="user_message"),

    # 用户头像上传
    url(r'^image/upload/$', UploadImageView.as_view(), name="image_upload"),
    #用户个人中心修改密码
    url(r'^update/pwd/$', UpdatePwdView.as_view(), name="update_pwd"),
    #用户个人中心修改邮箱-->>获取新邮箱验证码
    url(r'^sendemail_code/$', SendEmailCodeView.as_view(), name="sendemail_code"),
    #用户个人中心修改邮箱-->>验证新邮箱验证码是否正确，若正确则修改邮箱
    url(r'^update_email/$', UpdateEmailView.as_view(), name="update_email"),

]