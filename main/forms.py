from dataclasses import field
from pyexpat import model
from django import forms
from .models import Area, Customers, Fee, Shop, SubArea
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


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
        fields = ['username', 'email']
        widgets = {
            'username': forms.TextInput(
                attrs={'class': 'form-control', 'type': 'text', 'align': 'center', 'placeholder': 'UserName'}),
            'email': forms.TextInput(
                attrs={'class': 'form-control', 'type': 'text', 'align': 'center', 'placeholder': 'Email'}),
        }


class AreaForm (forms.ModelForm):
    class Meta:
        model = Area
        fields = ['area_name','area_user']
class SubAreaForm(forms.ModelForm):
    class Meta:
        model = SubArea
        fields = ['area','subarea_name']
class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customers
        fields = ['name', 'phone', 'address', 'customer_status',
                  'area', 'subarea', 'customer_fee_assigned']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Enter Name', 'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'placeholder': 'Enter Phone Number', 'class': 'form-control'}),
            # 'cnic': forms.TextInput(attrs={'placeholder': 'Enter CNIC Number', 'class': 'form-control'}),
        }


class CustomerFeeForm(forms.ModelForm):
    class Meta:
        model = Fee
        fields = ['fee_paid',  'month', 'debit', 'credit']
        widgets = {
            'fee_paid': forms.TextInput(attrs={'placeholder': 'Enter Fee/Payment Paid', 'class': 'form-control'}),
            # 'remaining_fee': forms.TextInput(attrs={'placeholder': 'Enter CNIC Number', 'class': 'form-control'}),
            'month': forms.HiddenInput(),
        }


class ShopForm(forms.ModelForm):
    class Meta:
        model = Shop
        fields = ['shop_name', 'shop_contact', 'shop_details']
        widgets = {
            'shop_name': forms.TextInput(attrs={'placeholder': 'Enter Your Shop`s Name', 'class': 'form-control'}),
            'shop_details': forms.Textarea(attrs={'placeholder': 'Enter Details', 'class': 'form-control'}),
        }
