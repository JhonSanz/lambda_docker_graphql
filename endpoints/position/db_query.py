import strawberry
from comparison import ComparisonOperators


@strawberry.input
class PositionQuery:
	reference_id: ComparisonOperators[str] | None = strawberry.UNSET
	open_date: ComparisonOperators[str] | None = strawberry.UNSET
	close_date: ComparisonOperators[str] | None = strawberry.UNSET
	price: ComparisonOperators[str] | None = strawberry.UNSET
	volume: ComparisonOperators[str] | None = strawberry.UNSET
	is_leveraged: ComparisonOperators[str] | None = strawberry.UNSET
	order_type: ComparisonOperators[str] | None = strawberry.UNSET
	direction: ComparisonOperators[str] | None = strawberry.UNSET
	asset_id: ComparisonOperators[str] | None = strawberry.UNSET
	description: ComparisonOperators[str] | None = strawberry.UNSET