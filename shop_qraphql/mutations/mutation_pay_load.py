import graphene
from ..queries.queries import Query


class MutationPayLoad(graphene.ObjectType):
	ok = graphene.Boolean(required=True)
	errors = graphene.List(graphene.String, required=True)
	query = graphene.Field(Query, required=True)

	def resolve_ok(self, info):
		return len(self.errors or []) == 0

	def resolve_errors(self, info):
		return self.errors or []

	def resolve_query(self, info):
		return {}
