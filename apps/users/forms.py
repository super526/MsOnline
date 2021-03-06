# _*_ coding:utf-8 _*_
from users.models import UserProfile

__author__ = 'supan'
__date__ = '2017/1/3 22:02'

from  django import forms
from captcha.fields import CaptchaField


class LoginForm(forms.Form):
    username = forms.CharField(required=True, min_length=4)
    password = forms.CharField(required=True)


class RegisterForm(forms.Form):
    username = forms.EmailField(required=True)
    password = forms.CharField(required=True, min_length=4)
    captcha = CaptchaField(error_messages={"invalid": u"验证码错误"})


class ForgetForm(forms.Form):
    email = forms.EmailField(required=True)
    captcha = CaptchaField(error_messages={"invalid": u"验证码错误"})


class ModifyPwdForm(forms.Form):
    password1 = forms.CharField(required=True,min_length=5)
    password2 = forms.CharField(required=True, min_length=5)


class UploadImageForm(forms.ModelForm):
    class Meta:
        model  = UserProfile
        fields = ['image']


class UserInfoForm(forms.ModelForm):
    """
    用户个人中心修改:ModelForm
    """
    class Meta:
        model  = UserProfile
        fields = ['nick_name','gender','birday','mobile']