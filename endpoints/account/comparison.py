import strawberry
from typing import Generic, TypeVar


T = TypeVar("T")

@strawberry.input
class ComparisonOperators(Generic[T]):
    exact: T | None = strawberry.UNSET
    contains: T | None = strawberry.UNSET
    gt: T | None = strawberry.UNSET
    gte: T | None = strawberry.UNSET
    lt: T | None = strawberry.UNSET
    lte: T | None = strawberry.UNSET
