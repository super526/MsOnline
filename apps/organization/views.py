# _*_ encoding:utf-8 _*_
from django.core.paginator import PageNotAnInteger
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from django.views.generic import View

from operation.models import UserFavorite
from organization.forms import UserAskForm
from organization.models import CityDict, CourseOrg, Teacher
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger


class OrgView(View):
    '''
    课程机构列表功能
    '''

    def get(self, request):
        # 列表数据填充:机构城市+课程机构
        all_citys = CityDict.objects.all()
        all_orgs = CourseOrg.objects.all()
        # 热门机构
        hot_orgs = all_orgs.order_by("-click_nums")[:3]

        # 机构搜索(根据机构名称、机构介绍)
        search_keywords = request.GET.get('keywords', "")
        if search_keywords:
            all_orgs = all_orgs.filter(
                Q(name__icontains=search_keywords) | Q(desc__icontains=search_keywords))

        # 取出筛选城市
        city_id = request.GET.get('city', '')
        # 若筛选城市存在，则对课程机构再次筛选(指定课程所属城市)
        if city_id:
            all_orgs = all_orgs.filter(city_id=int(city_id))
        # 取出筛选课程机构-->类别
        category = request.GET.get('ct', '')
        # 若筛选机构存在，则对课程机构再次筛选(制定课程所属机构)
        if category:
            all_orgs = all_orgs.filter(category=category)
        # 排序
        sort = request.GET.get('sort', '')
        if sort:
            if sort == 'students':
                all_orgs = all_orgs.order_by("-students")
            elif sort == "courses":
                all_orgs = all_orgs.order_by("-course_nums")

        # 课程机构总数
        org_nums = all_orgs.count()
        # 对课程机构进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        # Provide Paginator with the request object for complete querystring generation

        p = Paginator(all_orgs, 2, request=request)

        orgs = p.page(page)

        return render(request, 'org-list.html', {
            "all_citys": all_citys,
            "all_orgs": orgs,
            "org_nums": org_nums,
            "city_id": city_id,
            "category": category,
            "hot_orgs": hot_orgs,
            "sort": sort
        })


class AddUserAskView(View):
    '''
    用户添加资源
    '''

    def post(self, request):
        userask_form = UserAskForm(request.POST)
        if userask_form.is_valid():
            user_ask = userask_form.save(commit=True)
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail","msg":"添加出错"}', content_type='application/json')


class OrgHomeView(View):
    """
    机构首页视图
    """
    def get(self, request, org_id):
        current_page = 'home'
        course_org = CourseOrg.objects.get(id=int(org_id))
        all_courses = course_org.course_set.all()[:3]
        all_teachers = course_org.teacher_set.all()[:1]
        has_fav = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True
        return render(request, 'org-detail-homepage.html', {
            'all_courses': all_courses,
            'all_teachers': all_teachers,
            'course_org': course_org,
            'current_page': current_page,
            'has_fav':has_fav
        })


class OrgCourseView(View):
    """
    机构课程视图
    """
    def get(self, request, org_id):
        current_page = 'course'
        course_org = CourseOrg.objects.get(id=int(org_id))
        all_courses = course_org.course_set.all()
        has_fav = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True
        return render(request, 'org-detail-course.html', {
            'all_courses': all_courses,
            'course_org': course_org,
            'current_page': current_page,
            'has_fav':has_fav
        })


class OrgDescriptionView(View):
    """
    机构介绍视图
    """
    def get(self, request, org_id):
        current_page = 'desc'
        course_org = CourseOrg.objects.get(id=int(org_id))
        has_fav = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True
        return render(request, 'org-detail-desc.html', {
            'course_org': course_org,
            'current_page':current_page,
            'has_fav': has_fav
        })


class OrgTeacherView(View):
    """
    机构讲师视图
    """
    def get(self, request, org_id):
        current_page = 'teacher'
        course_org = CourseOrg.objects.get(id=int(org_id))
        all_teachers = course_org.teacher_set.all()
        has_fav = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True
        return render(request, 'org-detail-teachers.html', {
            'all_teachers': all_teachers,
            'course_org': course_org,
            'current_page': current_page,
            'has_fav': has_fav
        })


class AddFavView(View):
    """
    用户收藏 + 用户取消收藏
    """
    def post(self,request):
        fav_id = request.POST.get('fav_id', 0)
        fav_type = request.POST.get('fav_type', 0)
        if not request.user.is_authenticated():
            return HttpResponse('{"status":"fail","msg":"用户未登录"}', content_type='application/json')
        exist_records = UserFavorite.objects.filter(user=request.user, fav_id=int(fav_id), fav_type=int(fav_type))
        #如果用户收藏的记录已经存在，则表示用户取消收藏
        if exist_records:
            exist_records.delete()
            return HttpResponse('{"status":"success","msg":"收藏"}', content_type='application/json')
        else:
            user_favorite = UserFavorite()
            if int(fav_id) > 0 and int(fav_type) > 0:
                user_favorite.user = request.user
                user_favorite.fav_id = int(fav_id)
                user_favorite.fav_type = int(fav_type)
                user_favorite.save()
                return HttpResponse('{"status":"success","msg":"已收藏"}', content_type='application/json')

            else:
                return HttpResponse('{"status":"fail","msg":"收藏出错"}', content_type='application/json')


class TeacherListView(View):
    def get(self,request):
        all_teachers = Teacher.objects.all()
        # 授课讲师总数
        teacher_nums = all_teachers.count()
        # 教师搜索(根据讲师名称、讲师公司、讲师职位)
        search_keywords = request.GET.get('keywords', "")
        if search_keywords:
            all_teachers = all_teachers.filter(
                Q(name__icontains=search_keywords) | Q(work_company__icontains=search_keywords) | Q(
                    work_position__icontains=search_keywords))

        # 排序-->按人气(teacher的点击数)排序
        sort = request.GET.get('sort', '')
        if sort:
            if sort == 'popularity':
                all_teachers = all_teachers.order_by("-click_nums")
        #讲师排行榜，也是根据讲师的点击数倒叙排列，取前三个
        sorted_teachers = Teacher.objects.all().order_by("-click_nums")[:3]
        # 对授课讲师进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        # Provide Paginator with the request object for complete querystring generation
        p = Paginator(all_teachers, 2, request=request)
        all_teachers = p.page(page)
        return render(request,'teachers-list.html',{
            "all_teachers":all_teachers,
            "teacher_nums":teacher_nums,
            "sorted_teachers":sorted_teachers
        })


class TeacherDetailView(View):
    def get(self,request,teacher_id):
        teacher_detail = Teacher.objects.get(id=int(teacher_id))
        sorted_teachers = Teacher.objects.all().order_by("-click_nums")[:3]
        # 收藏功能:课程收藏 + 机构收藏
        has_fav_teacher = False
        has_fav_org = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=teacher_detail.id, fav_type=3):
                has_fav_teacher = True
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=teacher_detail.org.id, fav_type=2):
                has_fav_org = True
        return render(request,'teacher-detail.html',{
            "teacher_detail":teacher_detail,
            "sorted_teachers": sorted_teachers,
            "has_fav_teacher":has_fav_teacher,
            "has_fav_org":has_fav_org
        })
