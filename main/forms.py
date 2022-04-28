from dataclasses import field
from django import forms
from .models import Customers, Fee


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customers
        fields = ['name', 'phone', 'cnic', 'user']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Enter Name', 'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'placeholder': 'Enter Phone Number', 'class': 'form-control'}),
            'cnic': forms.TextInput(attrs={'placeholder': 'Enter CNIC Number', 'class': 'form-control'}),
            'user': forms.HiddenInput(),
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
