from django.db import models
from .form_checks import is_link


class Customer(models.Model):
    name = models.CharField(max_length=200, default='')
    mail = models.CharField(max_length=200, default='')

    def __str__(self):
        return self.name


class Seller(models.Model):
    shop_name = models.CharField(max_length=200, default='')
    link_on_photo = models.CharField(max_length=200, default='')
    created_date = models.DateField()
    sold_bouquets_counter = models.IntegerField(default=0)

    def __str__(self):
        return self.shop_name


class Bouquet(models.Model):
    name = models.CharField(max_length=200, default='')
    price = models.FloatField(default=0)
    link_on_photo = models.CharField(max_length=200, default='')
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE, related_name='bouquets', default=None)

    def __str__(self):
        return self.name


class Purchase(models.Model):
    bouquet = models.ForeignKey(Bouquet, on_delete=models.DO_NOTHING, related_name='purchase', default=None)
    customer = models.ForeignKey(Customer, on_delete=models.DO_NOTHING, related_name='purchases', default=None)
    cost = models.FloatField(default=0)
    service_income = models.FloatField(default=0)

    def __str__(self):
        return self.id

    @staticmethod
    def count_service_income(x):
        return round(x * 0.3, 2)
