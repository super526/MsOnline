# _*_ coding:utf-8 _*_
from courses.views import CourseListView, CourseDetailView, CourseInfoView, CourseCommentView, AddCourseCommentView, \
    VideoPlayView

__author__ = 'supan'
__date__ = '2017/2/21 20:41'

from django.conf.urls import url, include

urlpatterns = [
    # 课程机构列表页
    url(r'^list/$', CourseListView.as_view(), name="course_list"),
    #课程详情页
    url(r'^detail/(?P<course_id>\d+)/$', CourseDetailView.as_view(), name="course_detail"),
    #课程章节视频页
    url(r'^info/(?P<course_id>\d+)/$', CourseInfoView.as_view(), name="course_info"),
    #课程评论url
    url(r'^comment/(?P<course_id>\d+)/$', CourseCommentView.as_view(), name="course_comment"),
    #用户添加课程评论
    url(r'^add_comment/$', AddCourseCommentView.as_view(), name="add_comment"),
    #课程视频
    url(r'^video/(?P<video_id>\d+)/$', VideoPlayView.as_view(), name="video_play"),

]