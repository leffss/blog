from django import forms
from .models import Comment
from django.forms.fields import CharField


class CommentForm(forms.ModelForm):
    # captcha = CaptchaField(error_messages={"invalid": "验证码错误"})
    
    class Meta:
        model = Comment
        # fields = ['name', 'email', 'url', 'text', 'captcha']
        fields = ['name', 'email', 'url', 'text']


class CommentFormCode(forms.ModelForm):
    captcha = CharField(error_messages={"invalid": "验证码错误"})
    
    class Meta:
        model = Comment
        fields = ['name', 'email', 'url', 'text', 'captcha']
        # fields = ['name', 'email', 'url', 'text']

