# _*_ coding:utf-8 _*_
from organization.views import OrgView, AddUserAskView, OrgHomeView, OrgCourseView, OrgDescriptionView, OrgTeacherView, \
    AddFavView, TeacherListView, TeacherDetailView

__author__ = 'supan'
__date__ = '2017/2/16 22:10'

from django.conf.urls import url, include


urlpatterns = [
    # 课程机构列表页
    url(r'^list/$', OrgView.as_view(), name="org_list"),
    url(r'^add_ask/$', AddUserAskView.as_view(), name="add_ask"),
    url(r'^home/(?P<org_id>\d+)/$', OrgHomeView.as_view(), name="org_home"),
    url(r'^course/(?P<org_id>\d+)/$', OrgCourseView.as_view(), name="org_course"),
    url(r'^desc/(?P<org_id>\d+)/$', OrgDescriptionView.as_view(), name="org_desc"),
    url(r'^org_teacher/(?P<org_id>\d+)/$', OrgTeacherView.as_view(), name="org_teacher"),
    #机构收藏
    url(r'^add_fav/$', AddFavView.as_view(), name="add_fav"),
    #机构教师
    url(r'^teacher/list/$', TeacherListView.as_view(), name="teacher_list"),
    #机构教师详情
    url(r'^teacher/detail/(?P<teacher_id>\d+)/$', TeacherDetailView.as_view(), name="teacher_detail"),

]


