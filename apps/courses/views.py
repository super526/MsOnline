# _*_ encoding:utf-8 _*_
from django.core.paginator import PageNotAnInteger
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from django.views.generic import View

from courses.models import Course, CourseResource, Video
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger

from operation.models import UserFavorite, CourseComments, UserCourse
from utils.mixin_utils import LoginRequiredMixin


class CourseListView(View):
    def get(self,request):
        #查询所有课程 : 默认显示最新的课程 ->根据添加时间降序("-")排序
        all_courses = Course.objects.all().order_by("-add_time")
        #热门课程:根据课程点击数倒叙排序 取三条课程
        hot_courses = all_courses.order_by("-click_nums")[:3]
        
        #课程搜索
        search_keywords = request.GET.get('keywords', "")
        if search_keywords:
            all_courses = all_courses.filter(Q(name__icontains=search_keywords)|Q(desc__icontains=search_keywords)|Q(detail__icontains=search_keywords))

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



class CourseInfoView(LoginRequiredMixin,View):
    """
    课程章节视频信息页面
    """

    def get(self, request, course_id):
        course_detail = Course.objects.get(id=int(course_id))
        course_resource = CourseResource.objects.filter(course=course_detail)
        #查询用户是否已经关联了该课程
        user_course = UserCourse.objects.filter(user=request.user, course=course_detail)
        if not user_course:
            #方式一
            # user_course = UserCourse()
            # user_course.user = request.user
            # user_course.course = course_detail
            user_course = UserCourse(user=request.user, course=course_detail)
            user_course.save()
        #根据课程-->查询当前课程下的:用户课程对象集合
        user_courses = UserCourse.objects.filter(course=course_detail)
        #从用户课程对象集合中取出所有用户的id
        user_ids = [user_course.user.id for user_course in user_courses]
        #取出所有用户的用户课程对象
        all_user_courses = UserCourse.objects.filter(user_id__in=user_ids)
        #从所有用户课程对象中取出所有课程的id
        course_ids = [user_course.course.id for user_course in all_user_courses]
        #获取学过该课程的用户-->>学过的其他课程
        relate_courses = Course.objects.filter(id__in=course_ids).order_by("-click_nums")[:5]

        return render(request, 'course-video.html', {
            'course': course_detail,
            "course_resources": course_resource,
            'relate_courses':relate_courses
        })



class CourseCommentView(LoginRequiredMixin,View):
    """
    课程评论信息页面
    """
    def get(self, request, course_id):
        course_detail = Course.objects.get(id=int(course_id))
        # 查询用户是否已经关联了该课程
        user_course = UserCourse.objects.filter(user=request.user, course=course_detail)
        if not user_course:
            user_course = UserCourse(user=request.user, course=course_detail)
            user_course.save()
        # 根据课程-->查询当前课程下的:用户课程对象集合
        user_courses = UserCourse.objects.filter(course=course_detail)
        # 从用户课程对象集合中取出所有用户的id
        user_ids = [user_course.user.id for user_course in user_courses]
        # 取出所有用户的用户课程对象
        all_user_courses = UserCourse.objects.filter(user_id__in=user_ids)
        # 从所有用户课程对象中取出所有课程的id
        course_ids = [user_course.course.id for user_course in all_user_courses]
        # 获取学过该课程的用户-->>学过的其他课程
        relate_courses = Course.objects.filter(id__in=course_ids).order_by("-click_nums")[:5]
        course_resource = CourseResource.objects.filter(course=course_detail)
        all_course_comments = CourseComments.objects.all()
        return render(request, 'course-comment.html', {
            'course': course_detail,
            "course_resources": course_resource,
            "all_course_comments":all_course_comments,
            'relate_courses': relate_courses
        })


class VideoPlayView(View):
    """
    课程视频播放页面
    """
    def get(self, request, video_id):
        video = Video.objects.get(id=int(video_id))
        course_detail = video.lesson.course
        course_resource = CourseResource.objects.filter(course=course_detail)
        # 查询用户是否已经关联了该课程
        user_course = UserCourse.objects.filter(user=request.user, course=course_detail)
        if not user_course:
            # 方式一
            # user_course = UserCourse()
            # user_course.user = request.user
            # user_course.course = course_detail
            user_course = UserCourse(user=request.user, course=course_detail)
            user_course.save()
        # 根据课程-->查询当前课程下的:用户课程对象集合
        user_courses = UserCourse.objects.filter(course=course_detail)
        # 从用户课程对象集合中取出所有用户的id
        user_ids = [user_course.user.id for user_course in user_courses]
        # 取出所有用户的用户课程对象
        all_user_courses = UserCourse.objects.filter(user_id__in=user_ids)
        # 从所有用户课程对象中取出所有课程的id
        course_ids = [user_course.course.id for user_course in all_user_courses]
        # 获取学过该课程的用户-->>学过的其他课程
        relate_courses = Course.objects.filter(id__in=course_ids).order_by("-click_nums")[:5]

        return render(request, 'course-play.html', {
            'course': course_detail,
            "course_resources": course_resource,
            'relate_courses': relate_courses,
            'video':video
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











