import uuid
from decimal import Decimal
import boto3
from boto3.dynamodb.conditions import Key, Attr
import strawberry
from type import Asset

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("asset")


@strawberry.type
class Mutation:
    @strawberry.field
    def add_asset(
        self,
        name: str,
        presition: int,
        lot: int,
        swap_coeficient: str,
        long_swap_coeficient: float,
        short_swap_coeficient: float,
        account_id: str,
    ) -> Asset:
        id = str(uuid.uuid1())
        data = {
            "id": id,
            "name": name,
            "presition": presition,
            "lot": lot,
            "swap_coeficient": swap_coeficient,
            "long_swap_coeficient": Decimal(long_swap_coeficient),
            "short_swap_coeficient": Decimal(short_swap_coeficient),
            "account_id": account_id,
        }
        new_asset = Asset.from_row(data)
        table.put_item(Item=data)
        return new_asset

    @strawberry.field
    def delete_asset(self, id: str) -> Asset:
        asset = table.query(KeyConditionExpression=Key("id").eq(id))["Items"]
        if not asset:
            raise Exception("asset not found")
        table.delete_item(Key={"id": id})
        asset = asset[0]

        positions_table = dynamodb.Table("position")
        positions = positions_table.scan(FilterExpression=Key("asset_id").eq(id))["Items"]
        with positions_table.batch_writer() as batch:
            for item in positions:
                batch.delete_item(Key={"id": item["id"]})
        return Asset.from_row(asset)

    @strawberry.field
    def update_asset(
        self,
        id: str,
        name: str,
        presition: int,
        lot: int,
        swap_coeficient: str,
        long_swap_coeficient: float,
        short_swap_coeficient: float,
        account_id: str,
    ) -> Asset:
        to_update = {}
        to_update[":name"] = name
        to_update[":presition"] = presition
        to_update[":lot"] = lot
        to_update[":swap_coeficient"] = swap_coeficient
        to_update[":long_swap_coeficient"] = Decimal(long_swap_coeficient)
        to_update[":short_swap_coeficient"] = Decimal(short_swap_coeficient)
        to_update[":account_id"] = account_id
        response = None
        try:
            response = table.update_item(
                Key={"id": id},
                UpdateExpression="SET #name_ = :name, presition = :presition, lot = :lot, swap_coeficient = :swap_coeficient, long_swap_coeficient = :long_swap_coeficient, short_swap_coeficient = :short_swap_coeficient, account_id = :account_id",
                ExpressionAttributeValues=to_update,
                ReturnValues="UPDATED_NEW",
                ConditionExpression="attribute_exists(id)",
                ExpressionAttributeNames={"#name_": "name"},
            )
        except Exception as e:
            if "ConditionalCheckFailedException" in str(e):
                raise Exception("Asset does not exist")
            raise Exception(str(e))
        return Asset.from_row(
            {
                "id": id,
                "name": response["Attributes"]["name"],
                "presition": response["Attributes"]["presition"],
                "lot": response["Attributes"]["lot"],
                "swap_coeficient": response["Attributes"]["swap_coeficient"],
                "long_swap_coeficient": response["Attributes"]["long_swap_coeficient"],
                "short_swap_coeficient": response["Attributes"][
                    "short_swap_coeficient"
                ],
                "account_id": response["Attributes"]["account_id"],
            }
        )
