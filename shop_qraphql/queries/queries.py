import graphene
from ..objects.objects_types import *


class Query(graphene.ObjectType):
    bouquet = graphene.Field(BouquetType, id=graphene.Int())
    customer = graphene.Field(CustomerType, id=graphene.Int())
    seller = graphene.Field(SellerType, id=graphene.Int())

    purchases = graphene.List(PurchaseType, id=graphene.Int())
    bouquets = graphene.List(BouquetType)
    sellers = graphene.List(SellerType)

    @staticmethod
    def resolve_bouquet(self, info, **kwargs):
        id = kwargs.get('id')

        if id is not None:
            return Bouquet.objects.get(pk=id)

        return None

    @staticmethod
    def resolve_seller(self, info, **kwargs):
        id = kwargs.get('id')

        if id is not None:
            return Seller.objects.get(pk=id)

        return None

    @staticmethod
    def resolve_customer(self, info, **kwargs):
        id = kwargs.get('id')

        if id is not None:
            return Customer.objects.get(pk=id)

        return None

    @staticmethod
    def resolve_sellers(self, info, **kwargs):
        return Seller.objects.all()

    @staticmethod
    def resolve_bouquets(self, info, **kwargs):
        return Bouquet.objects.all()

    @staticmethod
    def resolve_purchases(self, info, **kwargs):
        id = kwargs.get('id')
        if id is not None:
            return Purchase.objects.filter(customer=id)

        return None

