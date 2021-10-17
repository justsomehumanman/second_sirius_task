import graphene
from ..queries.queries import Query


class MutationPayLoad(graphene.ObjectType):
	ok = graphene.Boolean(required=True)
	errors = graphene.List(graphene.String, required=True)
	query = graphene.Field(Query, required=True)

	@staticmethod
	def check_errors(checkers, input=None, id=None):
		errors = []
		for checker in checkers:
			result = checker(input, id)
			if result is not None:
				errors.append(result)
		return errors

	def resolve_ok(self, info):
		return len(self.errors or []) == 0

	def resolve_errors(self, info):
		return self.errors or []

	def resolve_query(self, info):
		return {}
