import strawberry
import typing

@strawberry.type
class Broker:
    id: str
    name: str
    website: str

    @staticmethod
    def from_row(row: typing.Dict[str, typing.Any]):
        return Broker(id=row["id"], name=row["name"], website=row["website"])
