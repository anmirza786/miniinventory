from calendar import month_name
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Subuser(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.OneToOneField(
        User, related_name='subuser', on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Area(models.Model):
    area_name = models.CharField(
        max_length=265, blank=False, null=False, verbose_name='Area Name')
    area_user = models.ForeignKey(Subuser,related_name='subname',null=False,blank=False, on_delete=models.CASCADE)

    def __str__(self):
        return self.area_name


class SubArea(models.Model):
    area = models.ForeignKey(Area, related_name='customerarea',
                             on_delete=models.CASCADE, verbose_name='Main area')
    subarea_name = models.CharField(
        max_length=256, blank=False, null=False, verbose_name='Sub-Area`s Name')

    def __str__(self):
        return self.subarea_name




class Customers(models.Model):
    customer_id = models.CharField(
        max_length=4, blank=False, null=False, verbose_name='Customer`s ID')
    name = models.CharField(max_length=1000, blank=False,
                            null=False, verbose_name='Customer`s Name')
    phone = models.CharField(max_length=13, blank=False,
                             null=False, verbose_name='Customer`s Phone Number')
    address = models.TextField(
        null=False, blank=False, verbose_name='Customer`s Address')
    customer_status = models.CharField(max_length=10, choices=(
        ('Active', 'active'), ('Disabled', 'disabled')), default='disabled', null=False)
    area = models.ForeignKey(Area, related_name='customer',
                             on_delete=models.CASCADE, verbose_name='Customer`s area')
    subarea = models.ForeignKey(SubArea, related_name='customer_sarea',
                                on_delete=models.CASCADE, verbose_name='Customer`s Sub-Area')
    customer_fee_assigned = models.DecimalField(max_digits=8, blank=False, null=False,
                                                decimal_places=2, verbose_name='Customer`s Assigned Fee')
    user = models.ForeignKey(User, related_name='user',
                             on_delete=models.CASCADE)
    assigned_to_subuser = models.ForeignKey(Subuser, related_name='customersubuser', on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Fee(models.Model):
    customer = models.ForeignKey(
        Customers, related_name='fee', on_delete=models.CASCADE)
    fee_paid = models.DecimalField(max_digits=8, blank=False, null=False,
                              decimal_places=2, verbose_name='Customer`s Paid Fee')
    fee_status = models.CharField(max_length=10, choices=(
        ('Paid', 'paid'), ('Not Paid', 'not_paid')), default='not_paid', null=False)
    debit = models.DecimalField(max_digits=8, blank=False, null=False,
                                decimal_places=2, verbose_name='Customer`s Debit Fee', default=0)
    credit = models.DecimalField(max_digits=8, blank=False, null=False,
                                 decimal_places=2, verbose_name='Customer`s Debit Fee', default=0)
    month = models.DateField(
        auto_now_add=False, verbose_name='Fee of the Month')
    taken_by = models.ForeignKey(User, related_name='fee',
                             on_delete=models.CASCADE)
    given_on_date = models.DateTimeField(
        auto_now_add=True, verbose_name='Fee`s Date')
    def __str__(self):
        return str(self.month)

class Shop(models.Model):
    # shop_logo = models.ImageField(
    #     upload_to='shops_logo/', null=True, blank=True, verbose_name='Shop`s Logo')
    shop_name = models.CharField(
        max_length=20000, blank=False, null=False, verbose_name='Shop Name')
    shop_contact = models.TextField(
        blank=False, null=False, verbose_name='Shop Contact Information')
    shop_details = models.TextField(
        blank=False, null=False, verbose_name='Shop Location/Adress')
    user = models.ForeignKey(
        User, related_name='shopholder', on_delete=models.CASCADE, unique=True)

    def __str__(self):
        return self.shop_name
