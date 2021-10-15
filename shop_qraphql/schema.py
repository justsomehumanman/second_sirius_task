import graphene
from graphene_django import DjangoObjectType
from .models import *


class SellerType(DjangoObjectType):
    class Meta:
        model = Seller


class SellerInput(graphene.InputObjectType):
    id = graphene.ID()
    shop_name = graphene.String()
    link_on_photo = graphene.String()
    sold_bouquets_counter = graphene.Int()


class Query(graphene.ObjectType):
    seller = graphene.Field(SellerType, id=graphene.Int())

    sellers = graphene.List(SellerType)

    @staticmethod
    def resolve_seller(self, info, **kwargs):
        id = kwargs.get('id')

        if id is not None:
            return Seller.objects.get(pk=id)

        return None

    @staticmethod
    def resolve_sellers(self, info, **kwargs):
        return Seller.objects.all()


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
