import strawberry
from comparison import ComparisonOperators


@strawberry.input
class MoneyQuery:
	currency: ComparisonOperators[str] | None = strawberry.UNSET