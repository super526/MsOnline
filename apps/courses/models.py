# _*_ encoding:utf-8 _*_
from __future__ import unicode_literals

from datetime import datetime

from django.db import models

from organization.models import CourseOrg, Teacher


class Course(models.Model):
    course_org = models.ForeignKey(CourseOrg,verbose_name=u"课程机构",null=True)
    name = models.CharField(max_length=50, verbose_name=u"课程名")
    desc = models.CharField(max_length=300, verbose_name=u"课程描述")
    detail = models.TextField(verbose_name=u"课程详情")
    teacher  = models.ForeignKey(Teacher,verbose_name=u"课程讲师",null=True,blank=True)
    degree = models.CharField(max_length=5, choices=(("cj", u"初级"), ("zj", u"中级"), ("gj", u"高级")), verbose_name=u"课程等级")
    learn_time = models.IntegerField(default=0, verbose_name=u"学习时长(分钟表示)")
    students = models.IntegerField(default=0, verbose_name=u"学习人数")
    fav_nums = models.IntegerField(default=0, verbose_name=u"收藏人数")
    is_banner = models.BooleanField(default=False, verbose_name=u"是否为课程轮播图")
    image = models.ImageField(upload_to="courses/%Y/%m", verbose_name=u"封面图", max_length=100)
    category = models.CharField(default=u"后端开发", max_length=20,verbose_name=u"课程类别")
    click_nums = models.IntegerField(default=0, verbose_name=u"点击数")
    tag = models.CharField(default="",verbose_name=u"课程标签",max_length=50)
    youneed_know =  models.CharField(max_length=200, default="", verbose_name=u"课程须知")
    teacher_tell = models.CharField(max_length=200, default="", verbose_name=u"老师告诉你")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = u"课程"
        verbose_name_plural = verbose_name

    def get_lesson_count(self):
        #获取课程的章节数 根据课程章节Lesson的course外键关联
        return self.lesson_set.all().count()

    #获取课程章节信息 根据课程章节Lesson与Course的外键关联
    def get_course_lesson(self):
        return self.lesson_set.all()

    def get_learned_users(self):
        #获取课程的学习用户，取五个用户
        return self.usercourse_set.all()[:5]

    def __unicode__(self):
        return self.name


class Lesson(models.Model):
    course = models.ForeignKey(Course, verbose_name=u"课程")
    name = models.CharField(max_length=100, verbose_name=u"章节名")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = u'章节'
        verbose_name_plural = verbose_name

    #根据课程章节Lesson与Video的外键关联-->获取课程章节视频信息
    def get_lesson_video(self):
            return self.video_set.all()

    def __unicode__(self):
        return self.name


class Video(models.Model):
    lesson = models.ForeignKey(Lesson, verbose_name=u"章节")
    name = models.CharField(max_length=100, verbose_name=u"视频名")
    url = models.CharField(max_length=200,default="",verbose_name=u"访问地址")
    learn_time = models.IntegerField(default=0, verbose_name=u"学习时长(分钟表示)")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = u'视频'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name


class CourseResource(models.Model):
    course = models.ForeignKey(Course, verbose_name=u"课程")
    name = models.CharField(max_length=100, verbose_name=u"资源名称")
    download = models.FileField(upload_to="course/resource/%Y/%m", verbose_name=u"资源文件", max_length=100)
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = u'课程资源'
        verbose_name_plural = verbose_name


    def __unicode__(self):
        return self.name