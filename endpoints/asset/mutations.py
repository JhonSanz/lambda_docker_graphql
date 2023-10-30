import uuid
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
            "long_swap_coeficient": long_swap_coeficient,
            "short_swap_coeficient": short_swap_coeficient,
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
        table.delete_item(
            Key={"id": id},
        )
        asset = asset[0]
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
        if name:
            to_update[":name"] = name
        if presition:
            to_update[":presition"] = presition
        if lot:
            to_update[":lot"] = lot
        if swap_coeficient:
            to_update[":swap_coeficient"] = swap_coeficient
        if long_swap_coeficient:
            to_update[":long_swap_coeficient"] = long_swap_coeficient
        if short_swap_coeficient:
            to_update[":short_swap_coeficient"] = short_swap_coeficient
        if account_id:
            to_update[":account_id"] = account_id
        response = None
        try:
            response = table.update_item(
                Key={"id": id},
                UpdateExpression="SET name = :name, presition = :presition, lot = :lot, swap_coeficient = :swap_coeficient, long_swap_coeficient = :long_swap_coeficient, short_swap_coeficient = :short_swap_coeficient, account_id = :account_id",
                ExpressionAttributeValues=to_update,
                ReturnValues="UPDATED_NEW",
                ConditionExpression="attribute_exists(id)",
                ExpressionAttributeNames={},
            )
        except Exception as e:
            if "ConditionalCheckFailedException" in str(e):
                raise Exception("Asset does not exist")
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
