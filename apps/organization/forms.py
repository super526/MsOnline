# _*_ coding:utf-8 _*_
__author__ = 'supan'
__date__ = '2017/2/16 21:59'
import re
from django import forms
from operation.models import UserAsk

# class UserAskForm(forms.Form):
#     name = forms.CharField(required=True,min_length=2,max_length=20)
#     phone = forms.CharField(required=True,min_length=11,max_length=11)
#     course_name = forms.CharField(required=True,min_length=5,max_length=50)
class UserAskForm(forms.ModelForm):
    class Meta:
        model  = UserAsk
        fields = ['name','mobile','course_name']
    
    def clean_mobile(self):
        """
        验证手机号码是否合法
        :return:
        """
        mobile = self.cleaned_data['mobile']
        REGEX_MOBILE = "^1[358]\d{9}$|^147\d{8}$|^176\d{8}$"
        re_compile = re.compile(REGEX_MOBILE)
        if re_compile.match(mobile):
            return mobile
        else:
            raise forms.ValidationError(u"非法手机号码",code="mobile_invalidation")