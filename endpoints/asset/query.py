import strawberry
import boto3
from boto3.dynamodb.conditions import Key
from type import Asset
from utils import PaginationWindow, get_pagination_window
from db_query import AssetQuery
from filters import FilterManager


dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("asset")


@strawberry.type
class Query:
    @strawberry.field(description="Get a list of asset")
    def assets(
        self,
        order_by: str,
        limit: int,
        query: AssetQuery,
        offset: int = 0,
    ) -> PaginationWindow[Asset]:
        filters = FilterManager(query).generate()
        assets = table.scan(**filters)
        assets = assets["Items"]
        return get_pagination_window(
            dataset=assets,
            ItemType=Asset,
            order_by=order_by,
            limit=limit,
            offset=offset,
        )

    @strawberry.field(description="Get a asset record.")
    def asset(self, id: str) -> Asset:
        asset = table.query(KeyConditionExpression=Key("id").eq(id))["Items"]
        if not asset:
            raise Exception("asset not found")
        asset = asset[0]
        return Asset.from_row(asset)
