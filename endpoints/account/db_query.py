import strawberry
from comparison import ComparisonOperators


@strawberry.input
class AccountQuery:
	name: ComparisonOperators[str] | None = strawberry.UNSET
	details: ComparisonOperators[str] | None = strawberry.UNSET
	leverage: ComparisonOperators[str] | None = strawberry.UNSET
	account_type: ComparisonOperators[str] | None = strawberry.UNSET
	broker_id: ComparisonOperators[str] | None = strawberry.UNSET
