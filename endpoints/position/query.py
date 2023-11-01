import strawberry
import boto3
from boto3.dynamodb.conditions import Key
from type import Position
from utils import PaginationWindow, get_pagination_window
from db_query import PositionQuery
from filters import FilterManager


dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("position")


@strawberry.type
class Query:
    @strawberry.field(description="Get a list of position")
    def positions(
        self,
        order_by: str,
        limit: int,
        query: PositionQuery,
        offset: int = 0,
    ) -> PaginationWindow[Position]:
        filters = FilterManager(query).generate()
        positions = table.scan(**filters)
        positions = positions["Items"]
        return get_pagination_window(
            dataset=positions,
            ItemType=Position,
            order_by=order_by,
            limit=limit,
            offset=offset,
        )

    @strawberry.field(description="Get a position record.")
    def position(self, id: str) -> Position:
        position = table.query(KeyConditionExpression=Key("id").eq(id))["Items"]
        if not position:
            raise Exception("position not found")
        position = position[0]
        return Position.from_row(position)
