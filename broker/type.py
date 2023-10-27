import strawberry
import typing


@strawberry.type
class Test:
    id: str
    msg: str


@strawberry.type
class Broker:
    id: str
    name: str
    website: str
    other: typing.List[Test]

    @staticmethod
    def from_row(row: typing.Dict[str, typing.Any]):
        return Broker(id=row["id"], name=row["name"], website=row["website"])

    @strawberry.field
    def other(self) -> typing.List[Test]:
        return [Test(id="1", msg="hello"), Test(id="2", msg="world")]
