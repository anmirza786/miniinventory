from django import forms
from django.urls import path
from django.contrib import admin
from django.shortcuts import redirect, render
from .models import Customers, Fee
import csv
from django.http import HttpResponse
# Register your models here.


class CsvImportForm(forms.Form):
    csv_file = forms.FileField()


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


class FeeAdmin(admin.ModelAdmin, ExportCsvMixin):
    list_display = ["customer", "fee", "remaining_fee",
                    "month", 'given_on_date']
    list_filter = ['month']
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


class CustomerAdmin(admin.ModelAdmin, ExportCsvMixin):
    list_display = ["name", "phone", "cnic", 'user']
    # list_filter = ['month']
    actions = ["export_as_csv"]


admin.site.register(Fee, FeeAdmin)
admin.site.register(Customers, CustomerAdmin)
