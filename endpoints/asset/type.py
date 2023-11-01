import strawberry
import typing
from boto3.dynamodb.conditions import Key
import boto3


dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("asset")


@strawberry.type
class Account:
    id: str
    name: str
    details: str
    leverage: float
    account_type: str

    def from_row(row: typing.Dict[str, typing.Any]):
        return Account(**row)


@strawberry.type
class Asset:
    id: str
    name: str
    presition: int
    lot: int
    swap_coeficient: str
    long_swap_coeficient: float
    short_swap_coeficient: float
    account_id: str
    account: Account

    @staticmethod
    def from_row(row: typing.Dict[str, typing.Any]):
        return Asset(**row)

    @strawberry.field
    def account(self) -> Account:
        table = dynamodb.Table("account")
        account = table.query(KeyConditionExpression=Key("id").eq(self.account_id))[
            "Items"
        ]
        if not account:
            raise Exception("account not found")
        account = account[0]
        return Account.from_row(account)
