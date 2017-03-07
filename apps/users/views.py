# _*_ encoding:utf-8 _*_
import json
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.views.generic.base import View
from django.contrib.auth.hashers import make_password

from courses.models import Course
from operation.models import UserCourse, UserMessage, UserFavorite
from organization.models import CourseOrg, Teacher
from utils.mixin_utils import LoginRequiredMixin
from .forms import LoginForm, RegisterForm,ForgetForm,ModifyPwdForm, UploadImageForm, UserInfoForm
from .models import UserProfile, EmailVerifyRecord
from utils.email_send import send_register_email
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger


# Create your views here.

class LoginView(View):
    def get(self, request):
        return render(request, "login.html", {})

    def post(self, request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user_name = request.POST.get("username", "")
            pass_word = request.POST.get("password", "")
            user = authenticate(username=user_name, password=pass_word)
            if user is not None:
                if user.is_active: #判断用户是否为激活状态
                    login(request, user)
                    return render(request, "index.html")
                else:
                    return render(request, "login.html", {"msg": "用户未激活"})
            else:
                return render(request, "login.html", {"msg": "用户名或密码错误"})
        else:
            return render(request, "login.html", {"login_form": login_form})


class RegisterView(View):
    def get(self, request):
        register_form = RegisterForm()
        return render(request, "register.html", {"register_form": register_form})

    def post(self, request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():#form表单校验
            user_name = request.POST.get("username", "")
            #判断用户邮箱帐号是否存在
            if UserProfile.objects.filter(email=user_name):
                return render(request, "register.html", {"register_form": register_form,"msg":"用户已经存在,请重新注册"})
            pass_word = request.POST.get("password", "")
            user_profile = UserProfile()
            user_profile.username = user_name
            user_profile.email = user_name
            user_profile.password = make_password(pass_word)
            user_profile.is_active = False #设置用户的为未激活状态.
            user_profile.save()
            send_register_email(user_name, "register")
            return render(request, "login.html")
        else:
            return render(request, "register.html", {"register_form": register_form})


class ActiveUserView(View) :
    def get(self, request, active_code):
        all_records = EmailVerifyRecord.objects.filter(code=active_code)
        if all_records:
            for record in all_records:
                email = record.email
                user = UserProfile.objects.get(email=email)
                user.is_active = True
                user.save()
                #用户注册，并激活成功时，系统向用户发送一条消息
                user_message = UserMessage()
                user_message.user = user.id
                user_message.message = u"欢迎注册慕学在线网，祝你学习愉快!"
                user_message.save()
        else:
            return render(request, "active_fail.html")
        return render(request, "login.html")


class ForgetPwdView(View):
    def get(self,request):
        forget_form = ForgetForm()
        return render(request,"forgetpwd.html",{"forget_form":forget_form})
    def post(self,request):
        forget_form = ForgetForm(request.POST)
        if forget_form.is_valid():
            email = request.POST.get("email","")
            send_register_email(email, "forget")
            return render(request,"send_success.html")
        else:
            return render(request, "forgetpwd.html", {"forget_form": forget_form})


class ResetPwdView(View) :
    def get(self, request, active_code):
        all_records = EmailVerifyRecord.objects.filter(code=active_code)
        if all_records:
            for record in all_records:
                email = record.email
                return render(request,"password_reset.html",{"email":email})
        else:
            return render(request, "active_fail.html")
        return render(request, "login.html")


class ModifyPwdView(View):
    def post(self,request):
        modify_pwd_form = ModifyPwdForm(request.POST)
        if modify_pwd_form.is_valid():
            password1 = request.POST.get("password1","")
            password2 = request.POST.get("password2","")
            email =  request.POST.get("email","")
            if password1 != password2:
                return render(request, "password_reset.html",{"email":email,"msg":"两次输入的密码不一致,请重新输入"})
            user = UserProfile.objects.get(email=email)
            user.password = make_password(password1)
            user.save()
            return render(request, "login.html")
        else:
            email = request.POST.get("email", "")
            return render(request, "password_reset.html", {"email": email,"modify_pwd_from":modify_pwd_form})


class UserInfoView(LoginRequiredMixin,View):
    """
    用户个人中心
    """
    def get(self,request):
        return render(request,'usercenter-info.html',{
        })
    def post(self,request):
        #修改用户个人中心属性
        user_info_form = UserInfoForm(request.POST, instance=request.user)
        if user_info_form.is_valid():
            user_info_form.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse(json.dumps(user_info_form.errors), content_type='application/json')


class UploadImageView(LoginRequiredMixin,View):
    """
    用户个人中心，用户头像上传
    """
    def post(self,request):
        image_form = UploadImageForm(request.POST, request.FILES,instance=request.user)
        if image_form.is_valid():
            #request.user.image = image_form.cleaned_data['image']
            #request.user.save()
            image_form.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail"}', content_type='application/json')


class UpdatePwdView(LoginRequiredMixin,View):
    def post(self,request):
        modify_pwd_form = ModifyPwdForm(request.POST)
        if modify_pwd_form.is_valid():
            password1 = request.POST.get("password1","")
            password2 = request.POST.get("password2","")
            if password1 != password2:
                return HttpResponse('{"status":"fail","msg":"两次输入不一致"}', content_type='application/json')
            user = request.user
            user.password = make_password(password1)
            user.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse(json.dumps(modify_pwd_form.errors), content_type='application/json')


class SendEmailCodeView(LoginRequiredMixin,View):
    """
    发送邮箱验证码
    """
    def get(self,request):
        #获取表单填写的邮箱
        email = request.GET.get('email', '')
        #判断邮箱是否存在(根据已有用户的邮箱来过滤)
        if UserProfile.objects.filter(email=email):
            #邮箱存在，则返回错误信息
            return HttpResponse('{"email":"邮箱已经存在"}', content_type='application/json')
        else:
            #不存在，则向修改的邮箱发送邮箱验证码
            send_register_email(email,"update")
            return HttpResponse('{"status":"success"}', content_type='application/json')


class UpdateEmailView(LoginRequiredMixin,View):
    def post(self,request):
        #获取邮箱
        email = request.POST.get('email', '')
        #获取验证码
        code = request.POST.get('code', '')
        #在邮箱验证码记录表中查询当前：邮箱、验证码、发送类型是否有匹配记录
        existed_records = EmailVerifyRecord.objects.filter(email=email,code=code,send_type="update")
        #若存在 则表示验证码正确，修改当前用户的邮箱
        if existed_records:
            user = request.user
            user.email = email
            user.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse('{"email":"验证码错误"}', content_type='application/json')


class UserCourseView(LoginRequiredMixin,View):
    """
    个人中心:我的课程
    """
    def get(self,request):
        user = request.user
        user_courses = UserCourse.objects.filter(user=user)
        return render(request,'usercenter-mycourse.html',{
            "user_courses":user_courses
        })


class MyFavOrgView(LoginRequiredMixin,View):
    """
    个人中心:我的收藏，收藏机构
    """
    def get(self,request):
        user = request.user
        #根据用户和收藏的类别，来获取用户收藏的课程机构列表
        fav_orgs = UserFavorite.objects.filter(user=user,fav_type=2)
        #定义一个空的课程机构列表
        org_list = []
        #遍历用户收藏的课程机构列表，获取每个用户收藏的fav_id，即:收藏课程机构的id
        for fav_org in  fav_orgs:
            #根据用户收藏来获取fav_id
            fav_id = fav_org.fav_id
            #收藏的fav_id==org_id，根据机构id获取机构
            org = CourseOrg.objects.get(id=fav_id)
            #添加到课程机构列表中
            org_list.append(org)
        return render(request,'usercenter-fav-org.html',{
            "org_list":org_list
        })


class MyFavTeacherView(LoginRequiredMixin,View):
    """
    个人中心:我的收藏，收藏讲师
    """
    def get(self,request):
        user = request.user
        #根据用户和收藏的类别，来获取用户收藏的课程机构列表
        fav_teachers = UserFavorite.objects.filter(user=user,fav_type=3)
        #定义一个空的课程讲师列表
        teacher_list = []
        #遍历用户收藏的课程讲师列表，获取每个用户收藏的fav_id，即:收藏课程讲师的id
        for fav_teacher in  fav_teachers:
            #根据用户收藏来获取fav_id
            fav_id = fav_teacher.fav_id
            #收藏的fav_id==org_id，根据机构id获取机构
            teacher = Teacher.objects.get(id=fav_id)
            #添加到课程机构列表中
            teacher_list.append(teacher)
        return render(request,'usercenter-fav-teacher.html',{
            "teacher_list":teacher_list
        })


class MyFavCourseView(LoginRequiredMixin,View):
    """
    个人中心:我的收藏，收藏课程
    """
    def get(self,request):
        user = request.user
        #根据用户和收藏的类别，来获取用户收藏的课程机构列表
        fav_courses = UserFavorite.objects.filter(user=user,fav_type=1)
        #定义一个空的课程机构列表
        course_list = []
        #遍历用户收藏的课程机构列表，获取每个用户收藏的fav_id，即:收藏课程机构的id
        for fav_course in  fav_courses:
            #根据用户收藏来获取fav_id
            fav_id = fav_course.fav_id
            #收藏的fav_id==org_id，根据机构id获取机构
            course = Course.objects.get(id=fav_id)
            #添加到课程机构列表中
            course_list.append(course)
        return render(request,'usercenter-fav-course.html',{
            "course_list":course_list
        })


class UserMessageView(LoginRequiredMixin,View):
    """
    个人中心:我的消息
    """
    def get(self,request):
        user_messages = UserMessage.objects.filter(user=request.user.id)
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(user_messages, 3, request=request)
        page_messages = p.page(page)
        return render(request, 'usercenter-message.html', {
            "user_messages": page_messages
        })


