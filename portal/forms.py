from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core import validators
from django.forms import fields
from django.forms.widgets import DateTimeInput
from .models import Work,Assignment,Person,Graded,Grader_sh

class RegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=100, required=True, help_text='Required', widget=forms.TextInput())
    email = forms.CharField(max_length=100, required=True, help_text='Required', widget=forms.TextInput())
    last_name = forms.CharField(max_length=100, required=False, help_text='Optional', widget=forms.TextInput())
    class Meta:
        model=User
        fields=['username','password1','password2','email','first_name','last_name']

class WorkForm(forms.Form):
 #   owner = forms.CharField(max_length=100, required=True, help_text='Required', widget=forms.TextInput())
    name = forms.CharField(max_length=100, required=True, help_text='Required', widget=forms.TextInput())
    total_marks = forms.IntegerField(required=True, help_text='Required', widget=forms.TextInput())
    deadline = forms.DateTimeField(required=True, help_text='2021-01-11 08:10:20', error_messages={'required':'Can\'t be empty','invalid':'Wrong Format'}, widget=forms.DateTimeInput())
    ################################################################
    weightage_parameter = forms.IntegerField(required=True, min_value=0, max_value=5)


class CreateForm(forms.Form):
        name = forms.CharField(max_length=100, required=True, help_text='Required', widget=forms.TextInput())
        total_marks = forms.IntegerField(required=True, help_text='Required', widget=forms.TextInput())


class AssignmentForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = ('submission',)

class graded_csv_Form(forms.ModelForm):
    class Meta:
        model = Graded
        fields = ('submission',)

class grader_sh_Form(forms.ModelForm):
    class Meta:
        model = Grader_sh
        fields = ('submission',)

class updatePass(forms.Form):
    old_password=forms.CharField(max_length=100, required=True, help_text='Required', widget=forms.PasswordInput)
    username=forms.CharField(max_length=100, required=True, widget=forms.TextInput)
    first_name = forms.CharField(max_length=100, required=True, widget=forms.TextInput())
    email = forms.CharField(max_length=100, required=True, widget=forms.TextInput())
    last_name = forms.CharField(max_length=100, required=False, widget=forms.TextInput())
    password=forms.CharField(max_length=100, required=False, widget=forms.PasswordInput)


class feedbackForm(forms.Form):
    Marks_Obtained = forms.IntegerField(min_value=0,required=True,help_text='Required',widget=forms.TextInput) 

class codeForm(forms.Form):
    Code =  forms.CharField(max_length=201, required=True, widget=forms.TextInput())
                  
class CourseForm(forms.Form):
    name = forms.CharField(max_length=150, required=True, widget=forms.TextInput())
    Member_allowance_to_TA = forms.IntegerField(min_value=0, max_value=1, required=True)
    Creation_allowance_to_TA = forms.IntegerField(min_value=0, max_value=1, required=True)
    
class ChatSearchForm(forms.Form):
    name = forms.CharField(max_length=150, required=True, widget=forms.TextInput())

class OTP(forms.Form):
    otp_enter=forms.IntegerField(required=True, help_text='Required', widget=forms.TextInput())

class OTP_update():
    def __init__(self,otp):
        self.otp_real=otp
    def clear(self):
        self.otp_real=-1
    def check(self,otp_challenge):
        if(self.otp_real==-1):
            return -1
        elif(self.otp_real==otp_challenge):
            return 1
        else:
            return 0
    