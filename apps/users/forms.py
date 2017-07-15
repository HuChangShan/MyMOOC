#coding:utf-8

__author__ = 'ChangShan Hu'
__date__ = '2017/6/15 21:06'

from django import forms
from captcha.fields import CaptchaField

from .models import UserProfile

class LoginForm(forms.Form):
	username = forms.CharField(required=True)
	password = forms.CharField(required=True, min_length=5)


class RegisterForm(forms.Form):
	email = forms.EmailField(required=True)
	password = forms.CharField(required=True, min_length=5)
	captcha = CaptchaField(required=True, error_messages={'invalid': "验证码错误"})


class ForgetForm(forms.Form):
	email = forms.EmailField(required=True)
	captcha = CaptchaField(required=True, error_messages={'invalid': "验证码错误"})


class ModifyForm(forms.Form):
	pwd_first = forms.CharField(required=True, min_length=6)
	pwd_second = forms.CharField(required=True, min_length=6)


class ImageUploadForm(forms.ModelForm):
	class Meta:
		model = UserProfile
		fields = ['image']


class InfoUpdateForm(forms.ModelForm):
	class Meta:
		model = UserProfile
		fields = ['nick_name', 'birthday', 'gender', 'address', 'mobile' ]
