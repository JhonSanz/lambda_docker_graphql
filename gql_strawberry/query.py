import typing
import strawberry
import boto3
from boto3.dynamodb.conditions import Key, Attr
from .type import Broker
from .data import brokers


dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table("broker")

Item = typing.TypeVar("Item")

@strawberry.type
class PaginationWindow(typing.Generic[Item]):
    items: typing.List[Item] = strawberry.field(
        description="The list of items in this pagination window."
    )

    total_items_count: int = strawberry.field(
        description="Total number of items in the filtered dataset."
    )

def matches(item, filters):
    """
    Test whether the item matches the given filters.
    This demo only supports filtering by string fields.
    """
    for attr_name, val in filters.items():
        if val not in item[attr_name]:
            return False
    return True

def get_pagination_window(
    dataset: typing.List[Broker],
    ItemType: type,
    order_by: str,
    limit: int,
    offset: int = 0,
    filters: dict[str, str] = {},
) -> PaginationWindow:
    """
    Get one pagination window on the given dataset for the given limit
    and offset, ordered by the given attribute and filtered using the
    given filters
    """
    if limit <= 0 or limit > 100:
        raise Exception(f"limit ({limit}) must be between 0-100")
    if filters:
        dataset = list(filter(lambda x: matches(x, filters), dataset))

    dataset.sort(key=lambda x: x[order_by])
    if offset != 0 and not 0 <= offset < len(dataset):
        raise Exception(f"offset ({offset}) is out of range " f"(0-{len(dataset) - 1})")

    total_items_count = len(dataset)
    items = dataset[offset : offset + limit]
    items = [ItemType.from_row(x) for x in items]
    return PaginationWindow(items=items, total_items_count=total_items_count)


@strawberry.type
class Query:
    @strawberry.field(description="Get a list of brokers.")
    def brokers(
        self,
        order_by: str,
        limit: int,
        offset: int = 0,
        name: str | None = None,
    ) -> PaginationWindow[Broker]:
        filters = {}

        if name:
            filters["name"] = name

        return get_pagination_window(
            dataset=brokers,
            ItemType=Broker,
            order_by=order_by,
            limit=limit,
            offset=offset,
            filters=filters,
        )
    
    @strawberry.field(description="Get a broker record.")
    def broker(self, id: str) -> Broker:
        broker = table.query(
            KeyConditionExpression=Key('id').eq(id)
        )["Items"]
        if not broker:
            raise Exception("broker not found")
        broker = broker[0]
        return Broker.from_row(broker)
