from graphene_django.types import DjangoObjectType
from ..models import *


class BouquetType(DjangoObjectType):
    class Meta:
        model = Bouquet


class PurchaseType(DjangoObjectType):
    class Meta:
        model = Purchase


class CustomerType(DjangoObjectType):
    class Meta:
        model = Customer


class SellerType(DjangoObjectType):
    class Meta:
        model = Seller
