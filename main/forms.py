import csv
from dataclasses import field
from pyexpat import model
from django import forms
from .models import Area, Customers, Fee, Shop, SubArea,Subuser
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class DateInput(forms.DateInput):
    input_type = 'date'


class UserRegistrationForm(UserCreationForm):
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(
            attrs={'class': 'form-control', 'type': 'password', 'align': 'center', 'placeholder': 'password'}),
    )
    password2 = forms.CharField(
        label="Confirm password",
        widget=forms.PasswordInput(
            attrs={'class': 'form-control', 'type': 'password', 'align': 'center', 'placeholder': 'password'}),
    )

    class Meta:
        model = User
        fields = ['username']
        widgets = {
            'username': forms.TextInput(
                attrs={'class': 'form-control', 'type': 'text', 'align': 'center', 'placeholder': 'UserName'}),

        }


class AreaForm1 (forms.ModelForm):
    class Meta:
        model = Area
        fields = ['area_name', 'area_user']



class SubAreaForm(forms.ModelForm):
    class Meta:
        model = SubArea
        fields = ['subarea_name']


class CustomerForm(forms.ModelForm):
    def __init__(self,user,*args,**kwargs):
        super (CustomerForm,self ).__init__(*args,**kwargs) # populates the post
        if Subuser.objects.filter(name=user).exists():
            sub=Subuser.objects.filter(name=user).first()
            area = Area.objects.filter(area_user=sub)
            for area in area:
                self.fields['subarea'].queryset = SubArea.objects.filter(area=area)
            self.fields['area'].queryset = Area.objects.filter(area_user=sub)
        else:
            self.fields['area'].queryset = Area.objects.all()
            self.fields['subarea'].queryset = SubArea.objects.all()
    class Meta:
        model = Customers
        fields = ['name', 'phone', 'address', 'customer_status',
                  'area', 'subarea', 'customer_fee_assigned']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Enter Name', 'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'placeholder': 'Enter Phone Number', 'class': 'form-control'}),
            'address': forms.Textarea(attrs={'placeholder': 'Enter Address', 'class': 'form-control'}),

            # 'cnic': forms.TextInput(attrs={'placeholder': 'Enter CNIC Number', 'class': 'form-control'}),
        }


class CustomerFeeForm(forms.ModelForm):
    class Meta:
        model = Fee
        fields = ['fee_paid', 'debit', 'credit',  'Date']
        widgets = {
            'fee_paid': forms.TextInput(attrs={'placeholder': 'Enter Fee/Payment Paid', 'class': 'form-control'}),
            # 'remaining_fee': forms.TextInput(attrs={'placeholder': 'Enter CNIC Number', 'class': 'form-control'}),
            'Date': DateInput(attrs={'placeholder': 'Enter Fee/Payment Paid', 'class': 'form-control'}),
        }


class ShopForm(forms.ModelForm):
    class Meta:
        model = Shop
        fields = ['shop_name', 'shop_contact', 'shop_details']
        widgets = {
            'shop_name': forms.TextInput(attrs={'placeholder': 'Enter Your Shop`s Name', 'class': 'form-control'}),
            'shop_details': forms.Textarea(attrs={'placeholder': 'Enter Details', 'class': 'form-control'}),
        }



