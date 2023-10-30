import strawberry
import typing


@strawberry.type
class Asset:
    id: str
    name: str
    presition: int
    lot: int
    swap_coeficient: str
    long_swap_coeficient: float
    short_swap_coeficient: float


@strawberry.type
class SubPosition:
    id: str
    open_date: str
    close_date: str
    price: float
    volume: float
    is_leveraged: bool
    order_type: str
    direction: str
    description: str


@strawberry.type
class Position:
    id: str
    reference: SubPosition | None
    open_date: str
    close_date: str
    price: float
    volume: float
    is_leveraged: bool
    order_type: str
    direction: str
    asset: Asset
    description: str

    @staticmethod
    def from_row(row: typing.Dict[str, typing.Any]):
        return Position(**row)

    @strawberry.field
    def related_asset(self) -> typing.List[Asset]:
        return [
            Asset(
                id="",
                name="asset test",
                presition=1,
                lot=1,
                swap_coeficient="1111100",
                long_swap_coeficient=1,
                short_swap_coeficient=1,
            ),
        ]
    
    @strawberry.field
    def related_reference(self) -> typing.List[SubPosition]:
        return [
            SubPosition(
                id="",
                open_date="2020-01-01",
                close_date="2020-01-01",
                price=1,
                volume=1,
                is_leveraged=True,
                order_type="Long",
                direction="In",
                description="test",
            ),
        ]
