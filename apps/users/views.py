# _*_ encoding:utf-8 _*_
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.views.generic.base import View
from django.contrib.auth.hashers import make_password

from .forms import LoginForm, RegisterForm,ForgetForm,ModifyPwdForm
from .models import UserProfile, EmailVerifyRecord
from utils.email_send import send_register_email


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


