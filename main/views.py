from itertools import count
from pprint import pprint
from sqlite3 import Date
from unicodedata import name
from django.shortcuts import redirect, render
from main.forms import AreaForm1, CustomerFeeForm, CustomerForm, ShopForm, SubAreaForm, UserRegistrationForm
from django.db.models import Q
from main.models import Area, Customers, Fee, Shop, Subuser, SubArea
from django.contrib.auth.decorators import login_required
import time
from io import BytesIO
import qrcode
import qrcode.image.svg
from datetime import date, datetime, timedelta
from .constants import constant_url
# Create your views here.


@login_required
def home(request):
    # fee = Fee.objects.all()
    customer_active = 0
    customer_disabled = 0
    customer_paid = 0
    total_customer = 0
    not_paid = 0

    if Customers.objects.filter(customer_status='active').exists():
        if Subuser.objects.filter(name=request.user.username).exists():
            subuser = Subuser.objects.filter(name=request.user.username).first()
            customer_active = Customers.objects.filter(
                customer_status='active').filter(assigned_to_subuser=subuser).count()
            total_customer = Customers.objects.filter(assigned_to_subuser=subuser).count()
            customer_disabled = total_customer-customer_active
            d = date.today()
            Date = d.strftime("%Y-%m-%d")
            Month = d.strftime("%B-%Y")
            active_customers = Customers.objects.filter(
                customer_status='active').filter(assigned_to_subuser=subuser)
            for customer in active_customers:
                paid = Fee.objects.filter(fee_status="paid").filter(
                    customer=customer).filter(Month=Month)
                if not paid:
                    pass
                else:
                    customer_paid = customer_paid + 1
            not_paid = customer_active-customer_paid
        else:
            customer_active = Customers.objects.filter(
                customer_status='active').count()
            total_customer = Customers.objects.all().count()
            customer_disabled = total_customer-customer_active
            d = date.today()
            Date = d.strftime("%Y-%m-%d")
            Month = d.strftime("%B-%Y")
            active_customers = Customers.objects.filter(
                customer_status='active')
            for customer in active_customers:
                paid = Fee.objects.filter(fee_status="paid").filter(
                    customer=customer).filter(Month=Month)
                if not paid:
                    pass
                else:
                    customer_paid = customer_paid + 1
            not_paid = customer_active-customer_paid

        # if Customers.objects.filter(customer_status='active').exists:
        #     customers = Customers.objects.filter(customer_status='active')
        #     for customer in customers:
        #         if Fee.objects.filter(Month=Month).filter(customer=customer).exists():
        #             a = 0
        #         else:
        #             Fee.objects.create(customer=customer, fee_paid=0,
        #                                Date=Date, Month=Month, taken_by=request.user)
        #             pass

    return render(request, 'home.html', {'customer_active': customer_active, 'total_customer': total_customer, 'customer_disabled': customer_disabled, 'customer_paid': customer_paid, 'not_paid': not_paid})


@login_required
def show_subusers(request):
    subuser = {}
    if Subuser.objects.all().exists():
        subuser = Subuser.objects.filter(created_by=request.user)
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
    user = request.user
    subuser = Subuser.objects.filter(name=user.username).first()
    # user = user.username
    if not subuser:
            customers = Customers.objects.filter(
                Q(name__icontains=query) | Q(phone__icontains=query) | Q(address__icontains=query) | Q(customer_id__icontains=query))
    else:
            customers = Customers.objects.filter(
                Q(name__icontains=query) | Q(phone__icontains=query) | Q(address__icontains=query) | Q(customer_id__icontains=query)).filter(assigned_to_subuser=subuser)

    return render(request, 'search.html', {'customers': customers, 'query': query})


@login_required
def edit_customer(request, pk):
    user = request.user
    username=request.user.username
    customer = Customers.objects.get(pk=pk)
    if request.method == 'POST':
        form = CustomerForm(username,request.POST, instance=customer)

        if form.is_valid():
            custom = form.save(commit=False)
            if Subuser.objects.filter(name=user.username).exists():
                subuser_admin = Subuser.objects.filter(name=user.username).first()
                subuser_admin = subuser_admin.created_by
                customer.user = subuser_admin
            else:
                customer.user = user
            custom.save()
            return redirect('search')
    else:
        form = CustomerForm(username,instance=customer)
    return render(request, 'edit_customer.html', {'form': form})


@login_required
def delete(request, pk):
    Customers.objects.filter(pk=pk).delete()

    return redirect('search')


@login_required
def addcustomer(request):
    user = request.user
    username=request.user.username
    if request.method == 'POST':
        form = CustomerForm(username,request.POST)

        if form.is_valid():
            customer = form.save(commit=False)
            if Subuser.objects.filter(name=user.username).exists():
                subuser = Subuser.objects.filter(name=user.username).first()
                subuser_admin = subuser.created_by
                customer.assigned_to_subuser = subuser
                customer.user = subuser_admin
            else:
                area = Area.objects.filter(area_name=customer.area).first()
                customer.assigned_to_subuser = area.area_user
                customer.user = user
            customer.save()
            return redirect('search')
    else:
        form = CustomerForm(username)
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
            # user = subuser.created_by
            details = Shop.objects.filter(user=user)

    return render(request, 'details.html', {'details': details})


@login_required
def fee(request, pk):
    customer = Customers.objects.get(pk=pk)
    user = request.user
    pFee = {}
    dt = date.today()
    df = date.today().replace(day=1) - timedelta(days=1)
    pMonth = df.strftime("%B-%Y")
    Month = dt.strftime("%B-%Y")
    pprint(pMonth)
    if Fee.objects.filter(customer=customer).filter(Month=pMonth).exists():
        pFee = Fee.objects.filter(customer=customer).filter(Month=pMonth).first()
    if Fee.objects.filter(customer=customer).filter(Month=Month).exists():
        return redirect('edit-fee', pk=pk)
    else:
        if request.method == 'POST':
            form = CustomerFeeForm(request.POST)
            if form.is_valid():
                fee = form.save(commit=False)
                fee.customer = customer
                fee.taken_by = user
                fee.fee_status = 'paid'
                fee.save()
                remaining = fee.debit
                # while remaining > 0:
                #     fee1 = Fee.objects.get(id=fee.id)
                #     month_only = fee1.Date
                #     split = str(month_only).split("-")
                #     # print(month_only)
                #     month_only = split[1]
                #     month_only = int(month_only) + 1
                #     year_only = int(split[0])
                #     if month_only > 12:
                #         year_only = int(year_only)+1
                #         month_only = 1
                #     new_date = datetime(year_only,
                #                         month_only, int(split[2]))
                #     new_date = new_date.strftime("%Y-%m-%d")
                #     new_month = new_date.strftime("%B-%Y")
                #     if remaining >= fee1.customer.customer_fee_assigned:
                #         fee2 = Fee.objects.create(customer=fee1.customer, fee_paid=remaining,
                #                                   fee_status="paid", debit=(remaining-fee1.customer.customer_fee_assigned), Date=new_date, Month=new_month,
                #                                   taken_by=fee1.taken_by)
                #         fee1 = fee2
                #         remaining = fee1.debit
                #     elif remaining < fee1.customer.customer_fee_assigned:
                #         fee2 = Fee.objects.create(customer=fee1.customer, fee_paid=remaining,

                #                                   fee_status="not_paid", credit=(fee1.customer.customer_fee_assigned-remaining), Date=new_date, Month=new_month,
                #                                   taken_by=fee1.taken_by)
                #         fee1 = fee2
                #         remaining = fee1.debit
                return redirect('print', fee.id)
        else:
            form = CustomerFeeForm()
        # print(form)
    return render(request, 'fee.html', {'form': form, 'customer': customer, 'pFee': pFee})


@login_required
def fee_paid(request):
    return render(request, 'FeePaid.html')


@login_required
def edit_fee(request, pk):
    customer = Customers.objects.get(pk=pk)
    user = request.user
    pFee = {}
    dt = date.today()
    df = date.today().replace(day=1) - timedelta(days=1)
    pMonth = df.strftime("%B-%Y")
    Month = dt.strftime("%B-%Y")
    if Fee.objects.filter(customer=customer).filter(Month=pMonth).exists():
        pFee = Fee.objects.filter(customer=customer).filter(Month=pMonth)
    fee = Fee.objects.filter(customer=customer).filter(Month=Month).first()
    if fee.fee_status == 'paid':
        return redirect('fee_paid')
    if request.method == 'POST':
        form = CustomerFeeForm(request.POST, instance=fee)
        if form.is_valid():
            fee = form.save(commit=False)
            fee.customer = customer
            fee.taken_by = user
            fee.fee_status = 'paid'
            fee.save()
            remaining = fee.debit
            # while remaining > 0:
            #     fee1 = Fee.objects.get(id=fee.id)
            #     month_only = fee1.Date
            #     split = str(month_only).split("-")
            #     # print(month_only)
            #     month_only = split[1]
            #     month_only = int(month_only) + 1
            #     year_only = int(split[0])
            #     if month_only > 12:
            #         year_only = int(year_only)+1
            #         month_only = 1
            #     new_date = datetime(year_only,
            #                         month_only, int(split[2])).strftime("%Y-%m-%d")
            #     new_month = datetime(year_only,
            #                          month_only, int(split[2])).strftime("%B-%Y")
            #     if remaining >= fee1.customer.customer_fee_assigned:
            #         fee2 = Fee.objects.create(customer=fee1.customer, fee_paid=remaining,
            #                                   fee_status="paid", debit=(remaining-fee1.customer.customer_fee_assigned), Date=new_date, Month=new_month,
            #                                   taken_by=fee1.taken_by)
            #         fee1 = fee2
            #         remaining = fee1.debit
            #     elif remaining < fee1.customer.customer_fee_assigned:
            #         fee2 = Fee.objects.create(customer=fee1.customer, fee_paid=remaining,

            #                                   fee_status="not_paid", credit=(fee1.customer.customer_fee_assigned-remaining), Date=new_date, Month=new_month,
            #                                   taken_by=fee1.taken_by)
            #         fee1 = fee2
            #         remaining = fee1.debit
            return redirect('print', fee.id)
    else:
        form = CustomerFeeForm(instance=fee)
        # print(form)
    return render(request, 'fee.html', {'form': form, 'customer': customer, 'pFee': pFee})


@login_required
def print(request, pk):
    context = {}
    user = request.user
    fee = Fee.objects.get(pk=pk)
    if Shop.objects.filter(user=user).exists():
        shop_details = Shop.objects.filter(user=user).first()

        factory = qrcode.image.svg.SvgImage
        link = constant_url+"show/"+str(fee.id)
        img = qrcode.make((link), image_factory=factory, box_size=7)
        stream = BytesIO()
        img.save(stream)
        svg = stream.getvalue().decode()
    else:
        # message("Please Add Shop Details First")
        return redirect('add-details')
    return render(request, 'print.html', {'fee': fee, 'shopdetails': shop_details, 'svg': svg})


def showprint(request, pk):
    context = {}
    user = request.user
    fee = Fee.objects.get(pk=pk)
    if Shop.objects.filter(user=user).exists():
        shop_details = Shop.objects.filter(user=user).first()
        factory = qrcode.image.svg.SvgImage
        link = constant_url+"show/"+str(fee.id)
        img = qrcode.make((link), image_factory=factory, box_size=7)
        stream = BytesIO()
        img.save(stream)
        svg = stream.getvalue().decode()
    else:
        # message("Please Add Shop Details First")
        return redirect('add_details')
    return render(request, 'showprint.html', {'fee': fee, 'shopdetails': shop_details, 'svg': svg})


@login_required
def generatereport(request):
    dt = date.today()
    dt = dt.strftime("%Y-%m-%d")
    query = request.GET.get('query', '2000-01-01')
    query2 = request.GET.get('query2', dt)
    customer = []
    fee=[]
    if Subuser.objects.filter(name=request.user.username).exists():
        subuser = Subuser.objects.filter(name=request.user.username).first()

        customers = Customers.objects.filter(assigned_to_subuser=subuser)
        for customer in customers:
            fee = Fee.objects.filter(
                Date__range=[query, query2]).filter(customer=customer)

    else:
        c = Customers.objects.filter(user=request.user)
        for customer in c:
            fee = Fee.objects.filter(Date__range=[query, query2])

    return render(request, 'report.html', {'fee': fee})


@login_required
def generatereport_month(request):
    Date = date.today()
    Date = Date.strftime("%B-%Y")
    # pprint(Date)
    fee = []
    if Fee.objects.filter(Month=Date).exists():
        if Subuser.objects.filter(name=request.user.username):
            subuser = Subuser.objects.filter(
                name=request.user.username).first()
            customers = Customers.objects.filter(assigned_to_subuser=subuser)
            for customer in customers:
                fe = Fee.objects.filter(Month=Date).filter(customer=customer)
                for fe in fe:
                    fee.append(fe)
        else:
            customers = Customers.objects.filter(user=request.user)
            for customer in customers:
                fe = Fee.objects.filter(Month=Date).filter(customer=customer)
                for fe in fe:
                    fee.append(fe)

    return render(request, 'monthly_report.html', {'fee': fee})


@login_required
def get_disabled(request):
    customer_disabled = {}
    user = request.user
    subuser = Subuser.objects.filter(name=user.username).first()
    if not subuser:
        if Customers.objects.filter(customer_status='disabled').exists():
            customer_disabled = Customers.objects.filter(
                customer_status='disabled')
    else:
        if Customers.objects.filter(customer_status='disabled').exists():
            customer_disabled = Customers.objects.filter(
                customer_status='disabled').filter(assigned_to_subuser=subuser)
    return render(request, 'disabled_customers.html', {'customer_disabled': customer_disabled})


@login_required
def get_active(request):
    customer_active = {}
    user = request.user
    subuser = Subuser.objects.filter(name=user.username).first()
    if not subuser:
        if Customers.objects.filter(customer_status='active').exists():
            customer_active = Customers.objects.filter(
                customer_status='active')
    else:
        if Customers.objects.filter(customer_status='active').exists():
            customer_active = Customers.objects.filter(
                customer_status='active').filter(assigned_to_subuser=subuser)
    return render(request, 'active_customers.html', {'customer_active': customer_active})


@login_required
def get_total(request):
    customer_total = {}
    subuser = Subuser.objects.filter(name=request.user.username).first()
    if not subuser:
        if Customers.objects.all().exists():
            customer_total = Customers.objects.all()
    else:
         if Customers.objects.all().exists():
            customer_total = Customers.objects.all().filter(assigned_to_subuser=subuser)
    return render(request, 'total_customers.html', {'customer_total': customer_total})


@login_required
def get_paid(request):
    customer_paid = []
    subuser = Subuser.objects.filter(name=request.user.username).first()
    if not subuser:
        if Customers.objects.filter(customer_status='active').exists():
            customer_active = Customers.objects.filter(
                customer_status='active')
            d = date.today()
            Month = d.strftime("%B-%Y")
            for customer in customer_active:
                paid = Fee.objects.filter(fee_status="paid").filter(
                    customer=customer).filter(Month=Month)
                if not paid:
                    pass
                else:
                    customer_paid.append(customer)
    else:
        if Customers.objects.filter(customer_status='active').exists():
            customer_active = Customers.objects.filter(
                customer_status='active').filter(assigned_to_subuser=subuser)
            d = date.today()
            Month = d.strftime("%B-%Y")
            for customer in customer_active:
                paid = Fee.objects.filter(fee_status="paid").filter(
                    customer=customer).filter(Month=Month)
                if not paid:
                    pass
                else:
                    customer_paid.append(customer)
    return render(request, 'paid_customers.html', {'customer_paid': customer_paid})


@login_required
def get_notpaid(request):
    customer_notpaid = []
    subuser = Subuser.objects.filter(name=request.user.username).first()
    if not subuser:
        if Customers.objects.filter(customer_status='active').exists():
            customer_active = Customers.objects.filter(
                customer_status='active')
            d = date.today()
            Month = d.strftime("%B-%Y")
            for customer in customer_active:
                notpaid = Fee.objects.filter(fee_status="not_paid").filter(
                    customer=customer).filter(Month=Month)
                if not notpaid:
                    if Fee.objects.filter(customer=customer).filter(fee_status="paid").exists():
                        pass
                    else:
                        customer_notpaid.append(customer)
                else:
                    customer_notpaid.append(customer)
    else:
        if Customers.objects.filter(customer_status='active').exists():
            customer_active = Customers.objects.filter(
                customer_status='active').filter(assigned_to_subuser=subuser)
            d = date.today()
            Month = d.strftime("%B-%Y")
            for customer in customer_active:
                notpaid = Fee.objects.filter(fee_status="not_paid").filter(
                    customer=customer).filter(Month=Month)
                if not notpaid:
                    if Fee.objects.filter(customer=customer).filter(fee_status="paid").exists():
                        pass
                    else:
                        customer_notpaid.append(customer)
                else:
                    customer_notpaid.append(customer)
    return render(request, 'notpaid_customers.html', {'customer_notpaid': customer_notpaid})


@login_required
def search_and_print(request):
    fee = []
    if Fee.objects.filter(fee_status="paid").exists():
        if Subuser.objects.filter(name=request.user.username).exists():

            subuser = Subuser.objects.filter(
                name=request.user.username).first()
            area = Area.objects.filter(area_user=subuser).first()
            customers = Customers.objects.filter(area=area)
            for customer in customers:
                if Fee.objects.filter(fee_status="paid").exists():
                    f = Fee.objects.filter(customer=customer)
                    for f in f:
                        fee.append(f)

        else:
            area = Area.objects.filter(area_added_by=request.user).first()
            customers = Customers.objects.filter(area=area)
            for customer in customers:
                fee = Fee.objects.filter(fee_status="paid")
    return render(request, 'searchandprint.html', {'fee': fee})


@login_required
def area(request):
    area = {}
    user = request.user
    if Subuser.objects.filter(name=user.username).exists():
        su = Subuser.objects.filter(name=user.username).first()
        if Area.objects.filter(area_user=su).exists():
            area = Area.objects.filter(area_user=su)
        else:
            return redirect('add_area')
    else:
        if Area.objects.filter(area_added_by=user).exists():
            area = Area.objects.filter(area_added_by=user)
        else:
            return redirect('add_area')
    return render(request, 'area.html', {'area': area})


@login_required
def add_area(request):
    user = request.user
    su=Subuser.objects.filter(name = request.user.username).first()
    if request.method == 'POST':
            form = AreaForm1(request.POST)
            if form.is_valid:
                details = form.save(commit=False)
                if Subuser.objects.filter(name = request.user.username).exists():
                    details.area_user = su
                    details.area_added_by = su.created_by
                else:
                    details.area_added_by = request.user
                details.save()
    else:
        form = AreaForm1()
    return render(request, 'add-area.html', {'form': form})


@login_required
def add_subarea(request, pk):
    area = Area.objects.get(pk=pk)
    if request.method == 'POST':
        form = SubAreaForm(request.POST)
        if form.is_valid:
            details = form.save(commit=False)
            details.area = area
            details.save()
            return redirect('area')
    else:
        form = SubAreaForm(request.POST)
    return render(request, 'add-subarea.html', {'form': form})
