from django.forms import Form, ModelForm
from .models import *
from django import forms
from django.contrib.auth.models import User


class UserRegisterForm(forms.ModelForm):
    password=forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = User 
        fields = ['username','email','password','first_name','last_name']


class Uploadpicture(forms.ModelForm):
    
    class Meta:
        model = Uploadpicture
        fields = '__all__'

class ProfileForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = '__all__'
        # fields =['Phone_number',' middle_name','Recent_address','Previous_address',
        #          ' annual_income','Average_income','date_of_birth','social_security',
        #          'Last_employer','Job_role','profile_picture']
        exclude=["user","is_frozen","account_number","routing_number",]


class PayBillForm(forms.Form):
    account_number=forms.CharField(max_length=30)
    routing_number=forms.CharField(max_length=30)
    bank_name=forms.CharField(max_length=100)
    amount=forms.DecimalField(decimal_places=2, max_digits=12)





        