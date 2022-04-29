from django.shortcuts import redirect, render
from main.forms import CustomerFeeForm, CustomerForm, ShopForm
from django.db.models import Q
from main.models import Customers, Fee, Shop
from django.contrib.auth.decorators import login_required
import time
# Create your views here.


@login_required
def home(request):
    fee = Fee.objects.all()
    return render(request, 'home.html', {'fee': fee})


@login_required
def search(request):
    query = request.GET.get('query', '')
    customers = Customers.objects.filter(
        Q(name__icontains=query) | Q(phone__icontains=query) | Q(cnic__icontains=query))

    return render(request, 'search.html', {'customers': customers, 'query': query})


@login_required
def delete(request, pk):
    Customers.objects.filter(pk=pk).delete()

    return redirect('search')


@login_required
def addcustomer(request):
    user = request.user
    if request.method == 'POST':
        form = CustomerForm(request.POST)

        if form.is_valid():
            customer = form.save(commit=False)
            customer.user = user
            customer.save()
            return redirect('search')
    else:
        form = CustomerForm()
    return render(request, 'add_customer.html', {'form': form})

@login_required
def shopdetails(request):
    user = request.user
    if request.method == 'POST':
        form = ShopForm(request.POST)

        if form.is_valid():
            details = form.save(commit=False)
            details.user = user
            details.save()
            return redirect('home')
    else:
        form = ShopForm()
    return render(request, 'add_details.html', {'form': form})
@login_required
def edit_shopdetails(request,pk):
    user = request.user
    details = Shop.objects.get(pk=pk)
    if request.method == 'POST':
        form = ShopForm(request.POST,instance=details)

        if form.is_valid():
            details = form.save(commit=False)
            details.user = user
            details.save()
            return redirect('details')
    else:
        form = ShopForm(instance=details)
    return render(request, 'edit_details.html', {'form': form})
@login_required
def show_details(request):
    user = request.user
    details = Shop.objects.filter(user=user)
    return render(request, 'details.html', {'details': details})


@login_required
def fee(request, pk):
    customer = Customers.objects.get(pk=pk)
    if request.method == 'POST':
        form = CustomerFeeForm(request.POST)
        month = request.POST['month']
        if form.is_valid():
            fee = form.save(commit=False)
            fee.customer = customer
            fee.month = month
            fee.save()
            return redirect('print',fee.id)
    else:
        form = CustomerFeeForm()
    # print(form)
    return render(request, 'fee.html', {'form': form, 'customer': customer})


@login_required
def print(request, pk):
    user = request.user
    fee = Fee.objects.get(pk=pk)
    shop_details = Shop.objects.get(user=user)
    return render(request, 'print.html', {'fee': fee,'shopdetails':shop_details})


@login_required
def generatereport(request):
    query = request.GET.get('query', '2000-01-01')
    query2 = request.GET.get('query2', '2000-12-30')
    fee = Fee.objects.filter(month__range=[query, query2])
    return render(request, 'report.html', {'fee': fee})
