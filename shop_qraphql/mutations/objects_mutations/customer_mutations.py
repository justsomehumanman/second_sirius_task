import graphene

from ...objects.objects_types import *
from ..mutation_pay_load import MutationPayLoad


class CustomerInput(graphene.InputObjectType):
    name = graphene.String()
    mail = graphene.String()


class CreateCustomer(MutationPayLoad, graphene.Mutation):
    class Arguments:
        input = CustomerInput(required=True)

    customer = graphene.Field(CustomerType)

    @staticmethod
    def mutate(root, info, input):
        customer = Customer(**input)
        customer.save()
        return CreateCustomer(customer=customer)


class UpdateCustomer(MutationPayLoad, graphene.Mutation):
    class Arguments:
        input = CustomerInput(required=True)
        id = graphene.Int(required=True)

    customer = graphene.Field(CustomerType)

    @staticmethod
    def mutate(root, info, id, input):
        customer = Customer.objects.get(pk=id)
        customer.name = input.name
        customer.mail = input.mail
        return UpdateCustomer(customer=customer)
    
    
class DeleteCustomer(MutationPayLoad, graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)

    @staticmethod
    def mutate(root, info, id):
        customer = Customer.objects.get(pk=id)
        customer.delete()
        return DeleteCustomer()
