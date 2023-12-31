from django import forms
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth.models import User
from .models import Post,Category
from django.forms.widgets import PasswordInput,TextInput

class registrationForm(UserCreationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder':'username'}),
        label='',
        required=True,
        help_text='',
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder':'password'}),
        label='',
        required=True,
        help_text='',
    )
    
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder':'confirm password'}),
        label='',
        required=True
    )
    
    class Meta:
        model = User
        fields=['username','password1','password2']
        
class loginForm(AuthenticationForm):
    
    username = forms.CharField(widget=TextInput(attrs={'placeholder':'username'}),label='')
    password = forms.CharField(widget=PasswordInput(attrs={'placeholder':'password'}),label='')
    


class commentForm(forms.Form):
    author = forms.CharField(
        max_length=60,
        widget= forms.TextInput(
            attrs={"class":"form-control","placeholder":"Your Name",'readonly':'readonly','style':'width:100%'}
        ),
    )
    body = forms.CharField(
        widget=forms.Textarea(
            attrs={"class":"form-control","placeholder":"leave a comment",'rows':'3','style':'width:100%'}
        )
    )


class AddBlog(forms.ModelForm):
    title = forms.CharField(required=True,widget=forms.TextInput(attrs={'style':'width:100%'}))
    body = forms.CharField(required=True,widget=forms.Textarea(attrs={'style':'width:100%'}))
    custom_category = forms.CharField(max_length=255,required=False,label="custom category (optional)",help_text='add multiple categories sepereated with a ","',widget=forms.TextInput(attrs={'style':'width:100%'}))
    categories = forms.ModelMultipleChoiceField( queryset=Category.objects.all(),required=False,widget=forms.CheckboxSelectMultiple())
    # created_by = forms.CharField(required=True,widget=forms.TextInput(attrs={'style':'width:100%','readonly':'readonly'}))
    class Meta:
        model = Post
        fields =['title','body','categories']