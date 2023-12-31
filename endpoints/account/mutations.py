import uuid
from decimal import Decimal
import boto3
from boto3.dynamodb.conditions import Key, Attr
import strawberry
from type import Account

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("account")


@strawberry.type
class Mutation:
    @strawberry.field
    def add_account(
        self,
        name: str,
        details: str,
        leverage: float,
        account_type: str,
        broker_id: str,
    ) -> Account:
        id = str(uuid.uuid1())
        data = {
            "id": id,
            "name": name,
            "details": details,
            "leverage": Decimal(leverage),
            "account_type": account_type,
            "broker_id": broker_id,
        }
        new_account = Account.from_row(data)
        table.put_item(Item=data)
        return new_account

    @strawberry.field
    def delete_account(self, id: str) -> Account:
        account = table.query(KeyConditionExpression=Key("id").eq(id))["Items"]
        if not account:
            raise Exception("account not found")
        table.delete_item(
            Key={"id": id},
        )
        account = account[0]
        return Account.from_row(account)

    @strawberry.field
    def update_account(
        self,
        id: str,
        name: str,
        details: str,
        leverage: float,
        account_type: str,
    ) -> Account:
        to_update = {}
        to_update[":name"] = name
        to_update[":details"] = details
        to_update[":leverage"] = Decimal(leverage)
        to_update[":account_type"] = account_type
        response = None
        try:
            response = table.update_item(
                Key={"id": id},
                UpdateExpression="SET #name_ = :name, details = :details, leverage = :leverage, account_type = :account_type",
                ExpressionAttributeValues=to_update,
                ReturnValues="UPDATED_NEW",
                ConditionExpression="attribute_exists(id)",
                ExpressionAttributeNames={
                    "#name_": "name"
                },
            )
        except Exception as e:
            if "ConditionalCheckFailedException" in str(e):
                raise Exception("Account does not exist")
            raise Exception(str(e))
        return Account.from_row(
            {
                "id": id,
                "name": response["Attributes"]["name"],
                "details": response["Attributes"]["details"],
                "leverage": response["Attributes"]["leverage"],
                "account_type": response["Attributes"]["account_type"],
            }
        )
