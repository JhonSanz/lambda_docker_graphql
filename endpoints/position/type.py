import strawberry
import typing
import boto3
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource("dynamodb")


@strawberry.type
class Asset:
    id: str
    name: str
    presition: int
    lot: int
    swap_coeficient: str
    long_swap_coeficient: float
    short_swap_coeficient: float

    @staticmethod
    def from_row(row: typing.Dict[str, typing.Any]):
        return Asset(**row)


@strawberry.type
class SubPosition:
    id: str
    reference_id: str
    open_date: str
    close_date: str
    price: float
    volume: float
    is_leveraged: bool
    order_type: str
    direction: str
    description: str

    @staticmethod
    def from_row(row: typing.Dict[str, typing.Any]):
        return SubPosition(**row)


@strawberry.type
class Position:
    id: str
    reference_id: str
    subpositions: SubPosition
    open_date: str
    close_date: str
    price: float
    volume: float
    is_leveraged: bool
    order_type: str
    direction: str
    asset_id: str
    asset: Asset
    description: str

    @staticmethod
    def from_row(row: typing.Dict[str, typing.Any]):
        return Position(**row)

    @strawberry.field
    def asset(self) -> typing.List[Asset]:
        table = dynamodb.Table("asset")
        asset = table.query(KeyConditionExpression=Key("id").eq(self.asset_id))["Items"]
        if not asset:
            raise Exception("asset not found")
        asset = asset[0]
        return Asset.from_row(asset)

    @strawberry.field
    def subpositions(self) -> typing.List[SubPosition]:
        table = dynamodb.Table("positions")
        subpositions = table.scan(FilterExpression=Key("reference_id").eq(self.id))[
            "Items"
        ]
        return [SubPosition.from_row(x) for x in subpositions]
