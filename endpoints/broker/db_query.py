import strawberry
from comparison import ComparisonOperators


@strawberry.input
class BrokerQuery:
	name: ComparisonOperators[str] | None = strawberry.UNSET
