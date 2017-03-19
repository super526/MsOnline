# _*_ coding:utf-8 _*_

import xadmin

from .models import Course, Lesson, Video, CourseResource,BannerCourse

__author__ = 'supan'
__date__ = '2017/1/2 21:54'


class LessonInline(object):
    model = Lesson
    extra = 0


class CourseResourseInline(object):
    model = CourseResource
    extra = 0


class CourseAdmin(object):
    list_display = ['name', 'desc', 'detail', 'degree', 'learn_time', 'students', 'get_lesson_count','go_to']
    search_fields = ['name', 'desc', 'detail', 'degree', 'learn_time', 'students', 'fav_nums', 'image', 'click_nums']
    list_filter = ['name', 'desc', 'detail', 'degree', 'learn_time', 'students', 'fav_nums', 'image', 'click_nums',
                   'add_time']
    model_icon = 'fa fa-list-alt'
    #设置课程可编辑字段
    list_editable  = ['degree','desc']
    #定义默认排序规则，根据课程点击数倒叙排列
    ordering = ['-click_nums']
    #设置后台课程属性字段为只读:as 点击数、学习人数、收藏数为动态产生，不能修改
    readonly_fields = ['fav_nums','students']
    #设置后台不显示属性字段 as:点击数
    exclude = ['click_nums']
    #在添加课程时，可同时添加课程章节、课程资源,（只能实现一层嵌套，不能再章节中在添加课程视频)
    inlines = [LessonInline,CourseResourseInline]
    #自动刷新时间
    refresh_times = [3,5]
    #自定义富文本编辑器插件
    style_fields = {"detail":"ueditor"}
    #自定义导入excel文件
    import_excel = True
    #自定义返回课程列表,返回不是轮播课程的课程集合
    def queryset(self):
        qs = super(CourseAdmin, self).queryset()
        qs_filter = qs.filter(is_banner=False)
        return qs_filter

    #在新增课程的时候统计课程机构的课程总数：重载课程save_models()
    def save_models(self):
        #得到当前课程对象
        obj = self.new_obj
        #先保存当前课程
        obj.save()
        #当前课程的课程机构存在
        if obj.course_org is not None:
            #获取当前课程的课程机构
            course_org = obj.course_org
            #根据课程的课程机构来查询--当前课程机构的课程数量
            course_org.course_nums = Course.objects.filter(course_org=course_org).count()
            #保存课程机构，-->更新课程机构课程数量
            course_org.save()

    def post(self,request,*args,**kwargs):
        if 'excel' in request.FILES:
            pass
        return super(CourseAdmin,self).post(request,args,kwargs)


class BannerCourseAdmin(object):
    """
    实现同一个model（ 课程Course）注册两个管理器（课程/轮播课程）
    """
    list_display = ['name', 'desc', 'detail', 'degree', 'learn_time', 'students', 'fav_nums', 'image', 'click_nums',
                    'add_time']
    search_fields = ['name', 'desc', 'detail', 'degree', 'learn_time', 'students', 'fav_nums', 'image', 'click_nums']
    list_filter = ['name', 'desc', 'detail', 'degree', 'learn_time', 'students', 'fav_nums', 'image', 'click_nums',
                   'add_time']
    model_icon = 'fa fa-list-alt'
    #定义默认排序规则，根据课程点击数倒叙排列
    ordering = ['-click_nums']
    #设置后台课程属性字段为只读:as 点击数、学习人数、收藏数为动态产生，不能修改
    readonly_fields = ['fav_nums','students']
    #设置后台不显示属性字段 as:点击数
    exclude = ['click_nums']
    #在添加课程时，可同时添加课程章节、课程资源,（只能实现一层嵌套，不能再章节中在添加课程视频)
    inlines = [LessonInline,CourseResourseInline]
    
    def queryset(self):
        qs = super(BannerCourseAdmin, self).queryset()
        qs_filter = qs.filter(is_banner=True)
        return qs_filter


class LessonAdmin(object):
    list_display = ['course', 'name', 'add_time']
    search_fields = ['course', 'name']
    list_filter = ['course__name', 'name', 'add_time']
    model_icon = 'fa fa-arrow-right'

class VideoAdmin(object):
    list_display = ['lesson', 'name', 'add_time']
    search_fields = ['lesson', 'name']
    list_filter = ['lesson__name', 'name', 'add_time']
    model_icon = 'fa fa-play-circle-o'


class CourseResourceAdmin(object):
    list_display = ['course', 'name', 'download', 'add_time']
    search_fields = ['course', 'name', 'download']
    list_filter = ['course__name', 'name', 'download', 'add_time']
    model_icon = 'fa fa-files-o'

xadmin.site.register(Course, CourseAdmin)
xadmin.site.register(BannerCourse, BannerCourseAdmin)
xadmin.site.register(Lesson, LessonAdmin)
xadmin.site.register(Video, VideoAdmin)
xadmin.site.register(CourseResource, CourseResourceAdmin)
