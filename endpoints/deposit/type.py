import strawberry
import typing


@strawberry.type
class Deposit:
    id: str
    quantity: float
    date_deposit: str
    account_id: str
    money_id: str
    currency: str
    description: str

    @staticmethod
    def from_row(row: typing.Dict[str, typing.Any]):
        return Deposit(**row)
