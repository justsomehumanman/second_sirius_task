import graphene
from graphene_django.types import DjangoObjectType, ObjectType
from .models import *


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


class Query(graphene.ObjectType):
    purchase = graphene.Field(PurchaseType, id=graphene.Int())
    bouquet = graphene.Field(BouquetType, id=graphene.Int())
    customer = graphene.Field(CustomerType, id=graphene.Int())
    seller = graphene.Field(SellerType, id=graphene.Int())

    purchases = graphene.List(PurchaseType, id=graphene.Int())
    bouquets = graphene.List(BouquetType)
    sellers = graphene.List(SellerType)

    @staticmethod
    def resolve_purchase(self, info, **kwargs):
        id = kwargs.get('id')

        if id is not None:
            return Purchase.objects.get(pk=id)

        return None

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


class BouquetInput(graphene.InputObjectType):
    id = graphene.ID()
    name = graphene.String()
    price = graphene.Int()
    link_on_photo = graphene.String()
    seller_id = graphene.Int()


class SellerInput(graphene.InputObjectType):
    id = graphene.ID()
    shop_name = graphene.String()
    link_on_photo = graphene.String()
    sold_bouquets_counter = graphene.Int()


class PurchaseInput(graphene.InputObjectType):
    id = graphene.ID()
    bouquet_id = graphene.Int()
    customer_id = graphene.Int()
    cost = graphene.Int()
    service_income = graphene.Int()


class CustomerInput(graphene.InputObjectType):
    name = graphene.String()
    mail = graphene.String()


class CreateSeller(graphene.Mutation):
    class Arguments:
        input = SellerInput(required=True)

    ok = graphene.Boolean()
    seller = graphene.Field(SellerType)

    @staticmethod
    def mutate(root, info, input=None):
        ok = True
        seller_instance = Seller(shop_name=input.shop_name,
                                 link_on_photo=input.link_on_photo,
                                 created_date=datetime.datetime.today())
        seller_instance.save()
        return CreateSeller(ok=ok, seller=seller_instance)


class UpdateSeller(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        input = SellerInput(required=True)

    ok = graphene.Boolean()
    seller = graphene.Field(SellerType)

    @staticmethod
    def mutate(root, info, id, input=None):
        ok = False
        seller_instance = Seller.objects.get(pk=id)
        if seller_instance:
            ok = True
            seller_instance.shop_name = input.name
            seller_instance.link_on_photo = input.link_on_photo
            seller_instance.sold_bouquets_counter = input.sold_bouquets_counter
            seller_instance.save()
            return UpdateSeller(ok=ok, seller=seller_instance)
        return UpdateSeller(ok=ok, seller=None)


class DeleteSeller(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)

    ok = graphene.Boolean()

    @staticmethod
    def mutate(root, info, id):
        ok = False
        seller = Seller.objects.get(pk=id)
        if seller:
            ok = True
            seller.delete()
            return DeleteSeller(ok=ok)
        return DeleteSeller(ok=ok)


class Mutation(graphene.ObjectType):
    create_seller = CreateSeller.Field()
    update_seller = UpdateSeller.Field()
    delete_seller = DeleteSeller.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
