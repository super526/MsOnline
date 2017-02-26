# _*_ encoding:utf-8 _*_
from django.core.paginator import PageNotAnInteger
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from django.views.generic import View

from courses.models import Course, CourseResource
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger

from operation.models import UserFavorite, CourseComments


class CourseListView(View):
    def get(self,request):
        #查询所有课程 : 默认显示最新的课程 ->根据添加时间降序("-")排序
        all_courses = Course.objects.all().order_by("-add_time")
        #热门课程:根据课程点击数倒叙排序 取三条课程
        hot_courses = all_courses.order_by("-click_nums")[:3]
        #课程总数
        courses_counts = all_courses.count()
        #对课程记录进行分页
        # 排序  学习人数/点击数
        sort = request.GET.get('sort', '')
        if sort:
            if sort == 'students': #根据学习人数排序
                all_courses = all_courses.order_by("-students")
            elif sort == "hot": #根据热门程度排序
                all_courses = all_courses.order_by("-click_nums")
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_courses, 4, request=request)
        courses = p.page(page)
        return render(request,'course-list.html',{
            'all_courses':courses,
            'hot_courses':hot_courses,
            'sort':sort
        })


class CourseDetailView(View):
    """
    课程详情页面
    """
    def get(self,request,course_id):
        #根据课程id查询课程详情
        course_detail = Course.objects.get(id=int(course_id))
        #每点击课程一次，课程点击数+1
        course_detail.click_nums += 1
        course_detail.save()
        #收藏功能:课程收藏 + 机构收藏
        has_fav_course = False
        has_fav_org = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=course_detail.id, fav_type=1):
                has_fav_course = True
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=course_detail.course_org.id, fav_type=2):
                has_fav_org = True
        #获取课程的标签
        tag = course_detail.tag
        if tag:
            #根据课程的标签来查询相关课程
            relate_course = Course.objects.filter(tag=tag)[:1]
        else:
            relate_course = []
        return  render(request,'course-detail.html',{
            'course_detail':course_detail,
            'relate_course':relate_course,
            'has_fav_course':has_fav_course,
            'has_fav_org':has_fav_org
        })



class CourseInfoView(View):
    """
    课程章节视频信息页面
    """

    def get(self, request, course_id):
        course_detail = Course.objects.get(id=int(course_id))
        course_resource = CourseResource.objects.filter(course=course_detail)
        return render(request, 'course-video.html', {
            'course': course_detail,
            "course_resources": course_resource
        })



class CourseCommentView(View):
    """
    课程评论信息页面
    """
    def get(self, request, course_id):
        course_detail = Course.objects.get(id=int(course_id))
        course_resource = CourseResource.objects.filter(course=course_detail)
        all_course_comments = CourseComments.objects.all()
        return render(request, 'course-comment.html', {
            'course': course_detail,
            "course_resources": course_resource,
            "all_course_comments":all_course_comments
        })

class AddCourseCommentView(View):
    """
    添加课程评论
    """
    def post(self,request):
        if not request.user.is_authenticated():
            return HttpResponse('{"status":"fail","msg":"用户未登录"}', content_type='application/json')
        course_id = request.POST.get('course_id', 0)
        comments = request.POST.get('comments', '')
        if course_id > 0 and comments:
            course_comments = CourseComments()
            course = Course.objects.get(id=int(course_id))
            course_comments.course = course
            course_comments.comments = comments
            course_comments.user = request.user
            course_comments.save()
            return HttpResponse('{"status":"success","msg":"添加成功"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail","msg":"添加失败"}', content_type='application/json')











