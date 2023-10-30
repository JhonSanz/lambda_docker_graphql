import strawberry
from comparison import ComparisonOperators


@strawberry.input
class AssetQuery:
    name: ComparisonOperators[str] | None = strawberry.UNSET
    account_id: ComparisonOperators[str] | None = strawberry.UNSET
