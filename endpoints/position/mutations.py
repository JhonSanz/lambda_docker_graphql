import uuid
from decimal import Decimal
import boto3
from boto3.dynamodb.conditions import Key, Attr
import strawberry
from type import Position

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("position")


@strawberry.type
class Mutation:
    @strawberry.field
    def add_position(
        self,
        reference_id: str,
        open_date: str,
        close_date: str,
        price: float,
        volume: float,
        is_leveraged: bool,
        order_type: str,
        direction: str,
        asset_id: str,
        description: str,
    ) -> Position:
        id = str(uuid.uuid1())
        data = {
            "id": id,
            "reference_id": reference_id,
            "open_date": open_date,
            "close_date": close_date,
            "price": Decimal(price),
            "volume": Decimal(volume),
            "is_leveraged": is_leveraged,
            "order_type": order_type,
            "direction": direction,
            "asset_id": asset_id,
            "description": description,
        }
        new_position = Position.from_row(data)
        table.put_item(Item=data)
        return new_position

    @strawberry.field
    def delete_position(self, id: str) -> Position:
        position = table.query(KeyConditionExpression=Key("id").eq(id))["Items"]
        if not position:
            raise Exception("position not found")
        table.delete_item(
            Key={"id": id},
        )
        position = position[0]
        return Position.from_row(position)

    @strawberry.field
    def update_position(
        self,
        id: str,
        reference_id: str,
        open_date: str,
        close_date: str,
        price: float,
        volume: float,
        is_leveraged: bool,
        order_type: str,
        direction: str,
        asset_id: str,
        description: str,
    ) -> Position:
        to_update = {}
        to_update[":reference_id"] = reference_id
        to_update[":open_date"] = open_date
        to_update[":close_date"] = close_date
        to_update[":price"] = price
        to_update[":volume"] = volume
        to_update[":is_leveraged"] = is_leveraged
        to_update[":order_type"] = order_type
        to_update[":direction"] = direction
        to_update[":asset_id"] = asset_id
        to_update[":description"] = description
        response = None
        try:
            response = table.update_item(
                Key={"id": id},
                UpdateExpression="SET reference_id = :reference_id, open_date = :open_date, close_date = :close_date, price = :price, volume = :volume, is_leveraged = :is_leveraged, order_type = :order_type, direction = :direction, asset_id = :asset_id, description = :description",
                ExpressionAttributeValues=to_update,
                ReturnValues="UPDATED_NEW",
                ConditionExpression="attribute_exists(id)",
            )
        except Exception as e:
            if "ConditionalCheckFailedException" in str(e):
                raise Exception("Position does not exist")
            raise Exception(str(e))
        return Position.from_row(
            {
                "id": id,
                "reference_id": response["Attributes"]["reference_id"],
                "open_date": response["Attributes"]["open_date"],
                "close_date": response["Attributes"]["close_date"],
                "price": response["Attributes"]["price"],
                "volume": response["Attributes"]["volume"],
                "is_leveraged": response["Attributes"]["is_leveraged"],
                "order_type": response["Attributes"]["order_type"],
                "direction": response["Attributes"]["direction"],
                "asset_id": response["Attributes"]["asset_id"],
                "description": response["Attributes"]["description"],
            }
        )
