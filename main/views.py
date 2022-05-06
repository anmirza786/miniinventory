from email import message
from django.shortcuts import redirect, render
from main.forms import CustomerFeeForm, CustomerForm, ShopForm, UserRegistrationForm
from django.db.models import Q
from main.models import Area, Customers, Fee, Shop, Subuser
from django.contrib.auth.decorators import login_required
import time
from io import BytesIO
import qrcode
import qrcode.image.svg
from datetime import date
# Create your views here.


@login_required
def home(request):
    # fee = Fee.objects.all()
    customer_active = Customers.objects.filter(
        customer_status='Active').count()
    total_customer = Customers.objects.all().count()
    customer_disabled = total_customer-customer_active

    return render(request, 'home.html', {'customer_active': customer_active, 'total_customer': total_customer, 'customer_disabled': customer_disabled})


@login_required
def show_subusers(request):
    subuser = Subuser.objects.all()
    return render(request, 'subusers.html', {'subuser': subuser})


@login_required
def add_subusers(request):
    user = request.user
    suser = Subuser.objects.filter(name=user.username)
    if not suser:
        if request.method == 'POST':
            form = UserRegistrationForm(request.POST)

            if form.is_valid():
                users = form.save()
                subuser = Subuser.objects.create(
                    name=users.username, created_by=user)
        else:
            form = UserRegistrationForm()
    else:
        return redirect('home')
    return render(request, 'add_subuser.html', {'form': form})


@login_required
def search(request):
    query = request.GET.get('query', '')
    user = request.user.username
    subuser = Subuser.objects.get(name=user)
    # user = user.username
    if not subuser:
        customers = Customers.objects.filter(
            Q(name__icontains=query) | Q(phone__icontains=query) | Q(address__icontains=query) | Q(customer_id__icontains=query))
    else:
        area = Area.objects.get(area_user=subuser)
        if not area:
            return redirect('home')
        else:
            customers = Customers.objects.filter(
                Q(name__icontains=query) | Q(phone__icontains=query) | Q(address__icontains=query) | Q(customer_id__icontains=query)).filter(area=area)

    return render(request, 'search.html', {'customers': customers, 'query': query})


@login_required
def edit_customer(request, pk):
    user = request.user
    customer = Customers.objects.get(pk=pk)
    if request.method == 'POST':
        form = CustomerForm(request.POST, instance=customer)

        if form.is_valid():
            custom = form.save(commit=False)
            custom.user = user
            custom.save()
            return redirect('search')
    else:
        form = CustomerForm(instance=customer)
    return render(request, 'edit_customer.html', {'form': form})


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
def edit_shopdetails(request, pk):
    user = request.user
    details = Shop.objects.get(pk=pk)
    if request.method == 'POST':
        form = ShopForm(request.POST, instance=details)

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
    if not details:
        subuser = Subuser.objects.filter(name=user.username)
        if not subuser:
            details = Shop.objects.filter(user=user)
        else:
            subuser = Subuser.objects.filter(name=user.username)[:1].get()
            user = subuser.created_by
            details = Shop.objects.filter(user=user)

    return render(request, 'details.html', {'details': details})


@login_required
def fee(request, pk):
    customer = Customers.objects.get(pk=pk)
    user = request.user
    if request.method == 'POST':
        form = CustomerFeeForm(request.POST)
        month = request.POST['month']
        if form.is_valid():
            fee = form.save(commit=False)
            fee.customer = customer
            fee.month = month
            fee.taken_by = user
            fee.save()
            return redirect('print', fee.id)
    else:
        form = CustomerFeeForm()
    # print(form)
    return render(request, 'fee.html', {'form': form, 'customer': customer})


@login_required
def print(request, pk):
    context = {}
    user = request.user
    fee = Fee.objects.get(pk=pk)
    shop_details = Shop.objects.get(user=user)
    if shop_details is None:
        message("Please Add Shop Details First")
        return redirect('add_details')
    factory = qrcode.image.svg.SvgImage
    link = "http://127.0.0.1:8000/print/"+str(fee.id)
    img = qrcode.make((link), image_factory=factory, box_size=5)
    stream = BytesIO()
    img.save(stream)
    svg = stream.getvalue().decode()
    return render(request, 'print.html', {'fee': fee, 'shopdetails': shop_details, 'svg': svg})


@login_required
def generatereport(request):
    Date = date.today()
    Date = Date.strftime("%Y-%m-%d")
    query = request.GET.get('query', '2000-01-01')
    query2 = request.GET.get('query2', Date)

    fee = Fee.objects.filter(month__range=[query, query2])
    return render(request, 'report.html', {'fee': fee})
