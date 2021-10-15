import graphene.types
from ...objects.objects_types import *
from ..mutation_pay_load import MutationPayLoad


class BouquetInput(graphene.InputObjectType):
    name = graphene.String()
    price = graphene.Float()
    link_on_photo = graphene.String()
    seller_id = graphene.Int()


class CreateBouquet(MutationPayLoad, graphene.Mutation):
    class Arguments:
        input = BouquetInput(required=True)

    bouquet = graphene.Field(BouquetType)
    bouquet_id = graphene.Int()

    @staticmethod
    def mutate(root, info, input):
        bouquet = Bouquet(**input)
        bouquet.save()
        return CreateBouquet(bouquet=bouquet, bouquet_id=bouquet.id)


class UpdateBouquet(MutationPayLoad, graphene.Mutation):
    class Arguments:
        input = BouquetInput(required=True)
        id = graphene.Int(required=True)

    bouquet = graphene.Field(BouquetType)
    bouquet_id = graphene.Int()

    @staticmethod
    def mutate(root, info, id, input):
        bouquet = Bouquet.objects.get(pk=id)
        bouquet.name = input.name
        bouquet.seller = Seller.objects.get(pk=input.seller_id)
        bouquet.price = input.price
        bouquet.link_on_photo = input.link_on_photo
        bouquet.save()
        return UpdateBouquet(bouquet=bouquet, bouquet_id=bouquet.id)


class DeleteBouquet(MutationPayLoad, graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)

    @staticmethod
    def mutate(root, info, id):
        bouquet = Bouquet.objects.get(pk=id)
        bouquet.delete()
        return DeleteBouquet()
