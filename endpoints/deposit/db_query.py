import strawberry
from comparison import ComparisonOperators


@strawberry.input
class DepositQuery:
	quantity: ComparisonOperators[str] | None = strawberry.UNSET
	date_deposit: ComparisonOperators[str] | None = strawberry.UNSET
	account_id: ComparisonOperators[str] | None = strawberry.UNSET
	currency: ComparisonOperators[str] | None = strawberry.UNSET
