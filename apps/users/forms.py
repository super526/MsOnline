# _*_ coding:utf-8 _*_
__author__ = 'supan'
__date__ = '2017/1/3 22:02'


from  django import forms


class LoginForm(forms.Form):
    username = forms.CharField(required=True,min_length=4)
    password = forms.CharField(required=True)
