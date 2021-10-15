import graphene
from graphene_django.types import ObjectType
from .mutations.mutations import Mutation
from .queries.queries import Query

Query: ObjectType
schema = graphene.Schema(query=Query, mutation=Mutation)
