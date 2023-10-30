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
class Deposit:
    id: str
    quantity: float
    date_deposit: str
    account: Account
    money_id: str
    currency: str
    description: str

    @staticmethod
    def from_row(row: typing.Dict[str, typing.Any]):
        return Deposit(**row)

    # @strawberry.field
    # def related_account(self) -> typing.List[Account]:
    #     return [
    #         Account(
    #             id="1",
    #             name="test",
    #             details="test",
    #             leverage=1,
    #             account_type="test",
    #         ),
    #     ]
