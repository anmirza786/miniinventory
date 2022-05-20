from dataclasses import field
from email import message
from tkinter.tix import Form
from unicodedata import name
from django import forms
import django
from django.urls import path
from django.contrib import admin, messages
from django.shortcuts import redirect, render
# from django.contrib.auth import User
# from main.forms import CSVImport
from .models import Area, Customers, Fee, Shop, SubArea, Subuser
import csv
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect
# Register your models here.


class ExportCsvMixin:
    def export_as_csv(self, request, queryset):
        meta = self.model._meta
        field_names = [field.name for field in meta.fields]
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(
            meta)
        writer = csv.writer(response)
        writer.writerow(field_names)
        for obj in queryset:
            row = writer.writerow([getattr(obj, field)
                                  for field in field_names])
        return response
        export_as_csv.short_description = "Export Selected"


class ShopAdmin(admin.ModelAdmin):
    list_display = ['shop_name',
                    'shop_contact', 'shop_details', 'user']


class FeeAdmin(admin.ModelAdmin, ExportCsvMixin):
    list_display = ["customer", "fee_paid", 'fee_status', "debit", "credit",
                    "Date", 'given_on_date', 'taken_by']
    list_filter = ['Date']
    actions = ["export_as_csv"]

    # change_list_template = "entities/heroes_changelist.html"

    # def get_urls(self):
    #     urls = super().get_urls()
    #     my_urls = [
    #         path('import-csv/', self.import_csv),
    #     ]
    #     return my_urls + urls

    # def import_csv(self, request):
    #     form = CsvImportForm(request.POST, request.FILES)
    #     payload = {"form": form}
    #     if request.method == "POST":
    #         csv_file = request.FILES["csv_file"]
    #         reader = csv.reader(csv_file)
    #         self.message_user(request, "Your csv file has been imported")
    #         return redirect("..")
    #     return render(
    #         request, "admin/csv_form.html", payload
    #     )


class CsvImportForm(forms.Form):
    csv_file = forms.FileField()


class CustomerAdmin(admin.ModelAdmin, ExportCsvMixin):
    list_display = ["name", "phone", "address", 'customer_status', 'user',
                    'area', 'subarea', 'customer_fee_assigned', 'assigned_to_subuser']
    # list_filter = ['month']
    actions = ["export_as_csv"]
    change_list_template = "entities/heroes_changelist.html"

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('import-csv/', self.import_csv),
        ]
        return my_urls + urls

    def import_csv(self, request):
        if request.method == "POST":
            csv_file = request.FILES["csv_file"]
            if not csv_file.name.endswith('.csv'):
                messages.warning(request, 'This is the wrong file formate')
                return HttpResponseRedirect(request.path_info)
            file_data = csv_file.read().decode('utf-8', 'ignore')
            csv_data = file_data.split('\r\n')
            a = 1
            for x in csv_data:
                fields = x.split(',')
                if a == 1:
                    pass
                    a = a+1
                else:

                    a = a+1
                    # print(fields[0])
                    # print(fields[1])
                    print(fields[2])
                    print(fields[3])
                    print(fields[4])
                    print(fields[5])
                    print(fields[6])
                    print(fields[7])
                    print(fields[8])
                    print(fields[9])
                    print(fields[10])
                    area = Area.objects.filter(area_name=fields[6]).first()
                    subarea = SubArea.objects.filter(
                        subarea_name=fields[7]).first()
                    subuser = Subuser.objects.filter(name=fields[10]).first()
                    # user = User.objects.filter(username=fields[9]).first()
                    cust = Customers(name=fields[2], phone=fields[3], address=fields[4], customer_status=fields[5],
                                     area=area, subarea=subarea, customer_fee_assigned=fields[8], user=subuser.created_by, assigned_to_subuser=subuser)
                    try:
                        cust.save()
                    except:
                        print("problem")
            # Create Hero obj8cts from passed in data
            # ..5
            self.message_user(request, "Your csv file has been imported")
            return redirect("..")
        form = CsvImportForm()
        payload = {"form": form}
        return render(
            request, "admin/csv_form.html", payload
        )


class AreaAdmin(admin.ModelAdmin):
    list_display = ['area_name', 'area_user']


class SubAreaAdmin(admin.ModelAdmin):
    list_display = ['area', 'subarea_name']


class SubuserAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_by']


admin.site.register(Fee, FeeAdmin)
admin.site.register(Customers, CustomerAdmin)
admin.site.register(Shop, ShopAdmin)
admin.site.register(Area, AreaAdmin)
admin.site.register(SubArea, SubAreaAdmin)
admin.site.register(Subuser, SubuserAdmin)
