import graphene

from ...objects.objects_types import *
from ..mutation_pay_load import MutationPayLoad


class PurchaseBouquet(MutationPayLoad, graphene.Mutation):
    class Arguments:
        bouquet_id = graphene.Int()
        customer_id = graphene.Int()

    purchase = graphene.Field(PurchaseType)

    @staticmethod
    def mutate(root, info, bouquet_id, customer_id):
        purchase = Purchase()
        purchase.bouquet = Bouquet.objects.get(pk=bouquet_id)
        purchase.customer = Customer.objects.get(pk=customer_id)
        purchase.cost = purchase.bouquet.price
        purchase.service_income = Purchase.count_service_income(purchase.cost)
        purchase.save()
        return PurchaseBouquet(purchase=purchase)
