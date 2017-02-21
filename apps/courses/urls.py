# _*_ coding:utf-8 _*_
from courses.views import CourseListView, CourseDetailView

__author__ = 'supan'
__date__ = '2017/2/21 20:41'

from django.conf.urls import url, include

urlpatterns = [
    # 课程机构列表页
    url(r'^list/$', CourseListView.as_view(), name="course_list"),

    url(r'^detail/(?P<course_id>\d+)/$', CourseDetailView.as_view(), name="course_detail"),
    #课程收藏
    #url(r'^add_fav/$', AddFavView.as_view(), name="add_fav"),

]