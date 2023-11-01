import strawberry
import boto3
from boto3.dynamodb.conditions import Key
from type import Deposit
from utils import PaginationWindow, get_pagination_window
from db_query import DepositQuery
from filters import FilterManager


dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("deposit")


@strawberry.type
class Query:
    @strawberry.field(description="Get a list of deposit")
    def deposits(
        self,
        order_by: str,
        limit: int,
        query: DepositQuery,
        offset: int = 0,
    ) -> PaginationWindow[Deposit]:
        filters = FilterManager(query).generate()
        deposits = table.scan(**filters)
        deposits = deposits["Items"]
        return get_pagination_window(
            dataset=deposits,
            ItemType=Deposit,
            order_by=order_by,
            limit=limit,
            offset=offset,
        )

    @strawberry.field(description="Get a deposit record.")
    def deposit(self, id: str) -> Deposit:
        deposit = table.query(KeyConditionExpression=Key("id").eq(id))["Items"]
        if not deposit:
            raise Exception("deposit not found")
        deposit = deposit[0]
        return Deposit.from_row(deposit)
