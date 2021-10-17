import graphene.types
from ...objects.objects_types import *
from ..mutation_pay_load import MutationPayLoad
from ...form_checks import is_link


class BouquetInput(graphene.InputObjectType):
    name = graphene.String()
    price = graphene.Float()
    link_on_photo = graphene.String()
    seller_id = graphene.Int()


def check_link_on_photo(input, id):
    if not is_link(input.link_on_photo):
        return "Field 'link_on_photo' expected for link, but received '{}'.".format(input.link_on_photo)
    return None


def check_id(input, id):
    if Bouquet.objects.get(pk=id) is None:
        return "Bouquet with id '{}' is not exist.".format(id)
    return None


def check_seller_id(input, id):
    if Seller.objects.get(pk=input.seller_id) is None:
        return "Seller with id '{}' is not exist.".format(id)
    return None


class CreateBouquet(MutationPayLoad, graphene.Mutation):
    class Arguments:
        input = BouquetInput(required=True)

    bouquet = graphene.Field(BouquetType)
    bouquet_id = graphene.Int()

    @staticmethod
    def mutate(root, info, input):
        checkers = [check_seller_id, check_link_on_photo]
        errors = MutationPayLoad.check_errors(checkers, input=input)
        if not errors:
            bouquet = Bouquet(**input)
            bouquet.save()
            return CreateBouquet(bouquet=bouquet, bouquet_id=bouquet.id, errors=errors)
        return CreateBouquet(errors=errors)


class UpdateBouquet(MutationPayLoad, graphene.Mutation):
    class Arguments:
        input = BouquetInput(required=True)
        id = graphene.Int(required=True)

    bouquet = graphene.Field(BouquetType)
    bouquet_id = graphene.Int()

    @staticmethod
    def mutate(root, info, id, input):
        checkers = [check_seller_id, check_link_on_photo, check_id]
        errors = MutationPayLoad.check_errors(checkers, input=input, id=id)
        if not errors:
            bouquet = Bouquet.objects.get(pk=id)
            bouquet.name = input.name
            bouquet.seller = Seller.objects.get(pk=input.seller_id)
            bouquet.price = input.price
            bouquet.link_on_photo = input.link_on_photo
            bouquet.save()
            return CreateBouquet(bouquet=bouquet, bouquet_id=bouquet.id, errors=errors)
        return UpdateBouquet(errors=errors)


class DeleteBouquet(MutationPayLoad, graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)

    @staticmethod
    def mutate(root, info, id):
        checkers = [check_id]
        errors = MutationPayLoad.check_errors(checkers, id=id)
        if not errors:
            bouquet = Bouquet.objects.get(pk=id)
            bouquet.delete()
        return DeleteBouquet(errors=errors)
