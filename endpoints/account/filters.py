import strawberry
from boto3.dynamodb.conditions import Key, Attr


class FilterManager:
    def __init__(self, filters) -> None:
        self.filters = filters

    def filtering(self, field, condition, value):
        if condition == "exact":
            return Key(field).eq(value)
        if condition == "contains":
            return Attr(field).contains(value)

    def generate(self):
        result = {}
        for field, subdict in self.filters.__dict__.items():
            if type(subdict) is strawberry.UNSET:
                continue
            for condition, value in subdict.__dict__.items():
                if not result.get("KeyConditionExpression"):
                    result["KeyConditionExpression"] = self.filtering(
                        field, condition, value
                    )
                else:
                    result["KeyConditionExpression"] = result[
                        "KeyConditionExpression"
                    ] & self.filtering(field, condition, value)
        return result
