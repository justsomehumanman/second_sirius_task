import graphene

from ...objects.objects_types import *
from ..mutation_pay_load import MutationPayLoad


class PurchaseInput(graphene.InputObjectType):
    bouquet_id = graphene.Int()
    customer_id = graphene.Int()


def check_bouquet_id(input, id):
    if not Bouquet.objects.filter(pk=input.bouquet_id):
        return "Bouquet with id '{}' is not exist.".format(id)
    return None


def check_customer_id(input, id):
    if not Customer.objects.filter(pk=input.customer_id):
        return "Customer with id '{}' is not exist.".format(id)
    return None


class PurchaseBouquet(MutationPayLoad, graphene.Mutation):
    class Arguments:
        input = PurchaseInput(required=True)

    purchase = graphene.Field(PurchaseType)

    @staticmethod
    def mutate(root, info, input):
        checkers = [check_customer_id, check_bouquet_id]
        errors = MutationPayLoad.check_errors(checkers, input=input)
        if not errors:
            purchase = Purchase()
            purchase.bouquet = Bouquet.objects.get(pk=input.bouquet_id)
            purchase.customer = Customer.objects.get(pk=input.customer_id)
            purchase.cost = purchase.bouquet.price
            purchase.service_income = Purchase.count_service_income(purchase.cost)
            purchase.save()
            return PurchaseBouquet(purchase=purchase, errors=errors)
        return PurchaseBouquet(errors=errors)
