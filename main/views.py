from django.shortcuts import redirect, render
from main.forms import CustomerFeeForm, CustomerForm
from django.db.models import Q
from main.models import Customers, Fee
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
            customer = form.save()
            customer.user = user
            customer.save()
    else:
        form = CustomerForm()
    return render(request, 'add_customer.html', {'form': form})


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
            return redirect('search')
    else:
        form = CustomerFeeForm()
    # print(form)
    return render(request, 'fee.html', {'form': form, 'customer': customer})


@login_required
def print(request, pk):
    fee = Fee.objects.get(pk=pk)
    return render(request, 'print.html', {'fee': fee})
