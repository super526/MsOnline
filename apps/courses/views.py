# _*_ encoding:utf-8 _*_
from django.core.paginator import PageNotAnInteger
from django.shortcuts import render

# Create your views here.
from django.views.generic import View

from courses.models import Course
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger


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
        p = Paginator(all_courses, 3, request=request)
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
        return  render(request,'course-detail.html',{
            'course_detail':course_detail
        })
