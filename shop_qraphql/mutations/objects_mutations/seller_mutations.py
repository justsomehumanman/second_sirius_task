import datetime

import graphene.types

from ...objects.objects_types import *
from ..mutation_pay_load import MutationPayLoad


class SellerInput(graphene.InputObjectType):
    shop_name = graphene.String()
    link_on_photo = graphene.String()


class CreateSeller(MutationPayLoad, graphene.Mutation):
    class Arguments:
        input = SellerInput(required=True)

    seller = graphene.Field(SellerType)

    @staticmethod
    def mutate(root, info, input):
        seller = Seller(**input)
        seller.created_date = datetime.date.today()
        seller.save()
        return CreateSeller(seller=seller)


class UpdateSeller(MutationPayLoad, graphene.Mutation):
    class Arguments:
        input = SellerInput(required=True)
        id = graphene.Int(required=True)

    seller = graphene.Field(SellerType)

    @staticmethod
    def mutate(root, info, id, input):
        seller = Seller.objects.get(pk=id)
        seller.shop_name = input.name
        seller.link_on_photo = input.link_on_photo
        seller.save()
        return UpdateSeller(seller=seller)


class DeleteSeller(MutationPayLoad, graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)

    @staticmethod
    def mutate(root, info, id):
        seller = Seller.objects.get(pk=id)
        seller.delete()
        return DeleteSeller()
