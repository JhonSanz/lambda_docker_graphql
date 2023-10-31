import strawberry
from comparison import ComparisonOperators


@strawberry.input
class AccountQuery:
	name: ComparisonOperators[str] | None = strawberry.UNSET
	broker_id: ComparisonOperators[str] | None = strawberry.UNSET
