import strawberry
import typing


@strawberry.type
class Account:
    id: str
    name: str
    details: str
    leverage: float
    account_type: str


@strawberry.type
class Asset:
    id: str
    name: str
    presition: int
    lot: int
    swap_coeficient: str
    long_swap_coeficient: float
    short_swap_coeficient: float
    account: Account

    @staticmethod
    def from_row(row: typing.Dict[str, typing.Any]):
        return Asset(**row)

    @strawberry.field
    def related_account(self) -> typing.List[Account]:
        return [
            Account(
                id="1",
                name="account 1",
                details="test",
                leverage=1,
                account_type="test",
            ),
        ]

