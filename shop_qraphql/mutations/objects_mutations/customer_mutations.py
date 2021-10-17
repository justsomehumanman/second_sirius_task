import graphene

from ...objects.objects_types import *
from ..mutation_pay_load import MutationPayLoad
from ...form_checks import is_mail


class CustomerInput(graphene.InputObjectType):
    name = graphene.String()
    mail = graphene.String()


def check_mail(input, id):
    if not is_mail(input.mail):
        return "Field 'mail' expected for mail address, but '{}' is not valid mail address.".format(input.mail)
    return None


def check_id(input, id):
    if not Customer.objects.filter(pk=id):
        return "Customer with id '{}' is not exist.".format(id)
    return None


class CreateCustomer(MutationPayLoad, graphene.Mutation):
    class Arguments:
        input = CustomerInput(required=True)

    customer = graphene.Field(CustomerType)
    customer_id = graphene.Int()

    @staticmethod
    def mutate(root, info, input):
        checkers = [check_mail]
        errors = MutationPayLoad.check_errors(checkers, input=input)
        if not errors:
            customer = Customer(**input)
            customer.save()
            return CreateCustomer(customer=customer, customer_id=customer.id, errors=errors)
        return CreateCustomer(errors=errors)


class UpdateCustomer(MutationPayLoad, graphene.Mutation):
    class Arguments:
        input = CustomerInput(required=True)
        id = graphene.Int(required=True)

    customer = graphene.Field(CustomerType)
    customer_id = graphene.Int()

    @staticmethod
    def mutate(root, info, id, input):
        checkers = [check_mail, check_id]
        errors = MutationPayLoad.check_errors(checkers, input=input, id=id)
        if not errors:
            customer = Customer.objects.get(pk=id)
            customer.name = input.name
            customer.mail = input.mail
            customer.save()
            return UpdateCustomer(customer=customer, customer_id=customer.id)
        return UpdateCustomer(errors=errors)

    
class DeleteCustomer(MutationPayLoad, graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)

    @staticmethod
    def mutate(root, info, id):
        checkers = [check_id]
        errors = MutationPayLoad.check_errors(checkers, id=id)
        if not errors:
            customer = Customer.objects.get(pk=id)
            customer.delete()
        return DeleteCustomer(errors=errors)
