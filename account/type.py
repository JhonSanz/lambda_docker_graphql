import strawberry
import typing

@strawberry.type
class Broker:
    id: str
    name: str
    website: str


@strawberry.type
class Account:
    id: str
    name: str
    details: str
    leverage: float
    account_type: str
    broker: Broker

    @staticmethod
    def from_row(row: typing.Dict[str, typing.Any]):
        return Account(**row)

    @strawberry.field
    def related_broker(self) -> typing.List[Broker]:
        return [
            Broker(id="1", name="hello", website="test.com"),
            Broker(id="2", name="world", website="test.com")
        ]
