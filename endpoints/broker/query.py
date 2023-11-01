import strawberry
import boto3
from boto3.dynamodb.conditions import Key
from type import Broker
from utils import PaginationWindow, get_pagination_window
from db_query import BrokerQuery
from filters import FilterManager


dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("broker")


@strawberry.type
class Query:
    @strawberry.field(description="Get a list of broker")
    def brokers(
        self,
        order_by: str,
        limit: int,
        query: BrokerQuery,
        offset: int = 0,
    ) -> PaginationWindow[Broker]:
        filters = FilterManager(query).generate()
        brokers = table.scan(**filters)
        brokers = brokers["Items"]
        return get_pagination_window(
            dataset=brokers,
            ItemType=Broker,
            order_by=order_by,
            limit=limit,
            offset=offset,
        )

    @strawberry.field(description="Get a broker record.")
    def broker(self, id: str) -> Broker:
        broker = table.query(KeyConditionExpression=Key("id").eq(id))["Items"]
        if not broker:
            raise Exception("broker not found")
        broker = broker[0]
        return Broker.from_row(broker)
