import datetime

import graphene.types

from ...objects.objects_types import *
from ..mutation_pay_load import MutationPayLoad
from ...form_checks import is_link


class SellerInput(graphene.InputObjectType):
    shop_name = graphene.String()
    link_on_photo = graphene.String()


def check_link_on_photo(input, id):
    if not is_link(input.link_on_photo):
        return "Field 'link_on_photo' expected for link, but received '{}'.".format(input.link_on_photo)
    return None


def check_id(input, id):
    if not Seller.objects.filter(pk=id):
        return "Seller with id '{}' is not exist.".format(id)
    return None


class CreateSeller(MutationPayLoad, graphene.Mutation):
    class Arguments:
        input = SellerInput(required=True)

    seller = graphene.Field(SellerType)
    seller_id = graphene.Int()

    @staticmethod
    def mutate(root, info, input):
        checkers = [check_link_on_photo]
        errors = MutationPayLoad.check_errors(checkers, input=input)
        if not errors:
            seller = Seller(**input)
            seller.created_date = datetime.date.today()
            seller.save()
            return CreateSeller(seller=seller, seller_id=seller.id)
        return CreateSeller(error=errors)


class UpdateSeller(MutationPayLoad, graphene.Mutation):
    class Arguments:
        input = SellerInput(required=True)
        id = graphene.Int(required=True)

    seller = graphene.Field(SellerType)
    seller_id = graphene.Int()

    @staticmethod
    def mutate(root, info, id, input):
        checkers = [check_link_on_photo, check_id]
        errors = MutationPayLoad.check_errors(checkers, input=input, id=id)
        if not errors:
            seller = Seller.objects.get(pk=id)
            seller.shop_name = input.shop_name
            seller.link_on_photo = input.link_on_photo
            seller.save()
            return UpdateSeller(seller=seller, seller_id=seller.id, errors=errors)
        return UpdateSeller(errors=errors)


class DeleteSeller(MutationPayLoad, graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)

    @staticmethod
    def mutate(root, info, id):
        checkers = [check_id]
        errors = MutationPayLoad.check_errors(checkers, id=id)
        if not errors:
            seller = Seller.objects.get(pk=id)
            seller.delete()
        return DeleteSeller(errors=errors)
