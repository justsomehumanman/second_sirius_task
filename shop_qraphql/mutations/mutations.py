from .objects_mutations.seller_mutations import *
from .objects_mutations.bouquet_mutations import *
from .objects_mutations.customer_mutations import *
from .objects_mutations.purchase_mutations import *


class Mutation(graphene.ObjectType):
    create_seller = CreateSeller.Field()
    update_seller = UpdateSeller.Field()
    delete_seller = DeleteSeller.Field()

    create_bouquet = CreateBouquet.Field()
    update_bouquet = UpdateBouquet.Field()
    delete_bouquet = DeleteBouquet.Field()

    create_customer = CreateCustomer.Field()
    update_customer = UpdateCustomer.Field()
    delete_customer = DeleteCustomer.Field()

    purchase_bouquet = PurchaseBouquet.Field()
