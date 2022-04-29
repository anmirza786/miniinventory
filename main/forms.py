from dataclasses import field
from django import forms
from .models import Customers, Fee, Shop


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customers
        fields = ['name', 'phone', 'cnic']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Enter Name', 'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'placeholder': 'Enter Phone Number', 'class': 'form-control'}),
            'cnic': forms.TextInput(attrs={'placeholder': 'Enter CNIC Number', 'class': 'form-control'}),
        }


class CustomerFeeForm(forms.ModelForm):
    class Meta:
        model = Fee
        fields = ['fee', 'remaining_fee', 'month']
        widgets = {
            'fee': forms.TextInput(attrs={'placeholder': 'Enter Fee/Payment Paid', 'class': 'form-control'}),
            'remaining_fee': forms.TextInput(attrs={'placeholder': 'Enter CNIC Number', 'class': 'form-control'}),
            'month': forms.HiddenInput(),
        }


class ShopForm(forms.ModelForm):
    class Meta:
        model = Shop
        fields = ['shop_name', 'shop_details']
        widgets = {
            'shop_name': forms.TextInput(attrs={'placeholder': 'Enter Your Shop`s Name', 'class': 'form-control'}),
            'shop_details': forms.Textarea(attrs={'placeholder': 'Enter Details', 'class': 'form-control'}),
        }
