import typing
from itertools import groupby
import strawberry
import boto3
from boto3.dynamodb.conditions import Key


dynamodb = boto3.resource("dynamodb")


@strawberry.type
class Broker:
    id: str
    name: str
    website: str

    @staticmethod
    def from_row(row: typing.Dict[str, typing.Any]):
        return Broker(**row)


@strawberry.type
class Deposit:
    money__currency: float
    total: str

    @staticmethod
    def from_row(row: typing.Dict[str, typing.Any]):
        return Deposit(**row)


@strawberry.type
class Account:
    id: str
    name: str
    details: str
    leverage: float
    account_type: str
    broker_id: str
    broker: Broker
    deposits: typing.List[Deposit]

    @staticmethod
    def from_row(row: typing.Dict[str, typing.Any]):
        return Account(**row)

    @strawberry.field
    def broker(self) -> Broker:
        table = dynamodb.Table("broker")
        broker = table.query(KeyConditionExpression=Key("id").eq(self.broker_id))[
            "Items"
        ]
        if not broker:
            raise Exception("broker not found")
        broker = broker[0]
        return Broker.from_row(broker)

    def get_total_deposits(self, data):
        sorted_data = sorted(data, key=lambda x: x["currency"])
        result = [
            Deposit.from_row(
                {
                    "money__currency": key,
                    "total": sum([data["amount"] for data in list(value)]),
                }
            )
            for key, value in groupby(sorted_data, lambda x: x["currency"])
        ]
        return result

    @strawberry.field
    def deposits(self) -> typing.List[Deposit]:
        table = dynamodb.Table("deposit")
        deposits = table.scan(FilterExpression=Key("account_id").eq(self.id))["Items"]
        return self.get_total_deposits(deposits)
