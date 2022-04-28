from calendar import month_name
from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Customers(models.Model):
    name = models.CharField(max_length=1000, blank=False,
                            null=False, verbose_name='Customer`s Name')
    phone = models.CharField(max_length=13, blank=False,
                             null=False, verbose_name='Customer`s Phone Number')
    cnic = models.CharField(max_length=15, blank=False,
                            null=False, verbose_name='Customer`s CNIC')
    user = models.ForeignKey(User, related_name='user', on_delete=models.CASCADE)
    def __str__(self):
        return self.name


class Fee(models.Model):
    customer = models.ForeignKey(
        Customers, related_name='fee', on_delete=models.CASCADE)
    fee = models.DecimalField(max_digits=8, blank=False, null=False,
                              decimal_places=2, verbose_name='Customer`s Paid Fee')
    remaining_fee = models.DecimalField(max_digits=8, blank=False, null=False,
                                        decimal_places=2, verbose_name='Customer`s Remaining Fee', default=0)
    month = models.DateField(
        auto_now_add=False, verbose_name='Fee of the Month')
    given_on_date = models.DateTimeField(
        auto_now_add=True, verbose_name='Fee`s Date')

