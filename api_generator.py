from account.type import Account

class Creator:
    def __init__(self, strawberry_type, path_to_save):
        self.strawberry_type = strawberry_type
        self.path_to_save = path_to_save

    def check_file_exists(self, path: str) -> bool:
        """ Checks if a file exists """
        try:
            with open(f"{path}", "r") as f:
                return True
        except FileNotFoundError:
            return False
    
    def create_query(self):
        name = self.strawberry_type.__strawberry_definition__.name.lower()
        if (self.check_file_exists(self.path_to_save + "/query.py")):
            print(f"File already exists in {self.path_to_save}/query.py")
            return
        with open(self.path_to_save + "/query.py", "w") as f:
            f.write(
                "import strawberry\n"
                "import boto3\n"
                "from boto3.dynamodb.conditions import Key\n"
                f"from .type import {name.capitalize()}\n"
                f"from .utils import PaginationWindow, get_pagination_window\n"
                "\n""\n"
                "dynamodb = boto3.resource('dynamodb')\n"
                f"table = dynamodb.Table('{name}')\n\n"
                "@strawberry.type\n"
                "class Query:\n"
                f"\t@strawberry.field(description='Get a list of {name}')\n"
                f"\tdef {name}s(\n"
                "\t\tself,\n"
                "\t\torder_by: str,\n"
                "\t\tlimit: int,\n"
                "\t\toffset: int = 0,\n"
                "\t\tname: str | None = None,\n"
                f"\t) -> PaginationWindow[{name.capitalize()}]:\n"
                "\t\tresponse = table.scan()\n"
                f"\t\t{name}s = response['Items']\n\n"
                "\t\twhile 'LastEvaluatedKey' in response:\n"
                "\t\t\tresponse = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])\n"
                f"\t\t\t{name}s.extend(response['Items'])\n\n"
                "\t\tfilters = {}\n"
                "\t\tif name:\n"
                "\t\t\tfilters['name'] = name\n"
                "\t\treturn get_pagination_window(\n"
                f"\t\t\tdataset={name}s,\n"
                f"\t\t\tItemType={name.capitalize()},\n"
                "\t\t\torder_by=order_by,\n"
                "\t\t\tlimit=limit,\n"
                "\t\t\toffset=offset,\n"
                "\t\t\tfilters=filters,\n"
                "\t\t)\n\n"
                "\t@strawberry.field(description='Get a broker record.')\n"
                f"\tdef {name}(self, id: str) -> {name.capitalize()}:\n"
                f"\t\t{name} = table.query(\n"
                "\t\t\tKeyConditionExpression=Key('id').eq(id)\n"
                "\t\t)['Items']\n"
                f"\t\tif not {name}:\n"
                f"\t\t\traise Exception('{name} not found')\n"
                f"\t\t{name} = {name}[0]\n"
                f"\t\treturn {name.capitalize()}.from_row({name})\n"
            )
    
    def create_mutations(self):
        name = self.strawberry_type.__strawberry_definition__.name.lower()

        if (self.check_file_exists(self.path_to_save + "/mutations.py")):
            print(f"File already exists in {self.path_to_save}/mutations.py")
            return

        all_fields = [
            {"field": field, "data": str(f_type).split("'")[1]}
            for field, f_type in self.strawberry_type.__dict__["__annotations__"].items()
            if f_type in [str, float, int, bool]
        ]
        filtered_id = list(filter(lambda x: x['field'] != "id", all_fields))

        add = ", ".join(
            [
                f"{item['field']}: {item['data']}" for item in
                filtered_id
            ]
        )
        add_data = ",\n".join(
            [
                f"\t\t\t\t'{item['field']}': {item['field']}"
                for item in all_fields
            ]
        )
        updating_fileds = "\n".join(
            [
                f"\t\tif {item['field']}: to_update[':{item['field']}'] = {item['field']}"
                for item in filtered_id
            ]
        )
        updating_dynamo_expression = "SET #broker_name = :name, website = :website"
        updating_dynamo_expression = "SET " + ", ".join([
            f"{item['field']} = :{item['field']}"
            for item in filtered_id
        ])
        updating_response = "'id': id,\n" + ",\n".join(
            [
                f"\t\t\t'{item['field']}': response['Attributes']['{item['field']}']"
                for item in filtered_id
            ]
        )

        with open(self.path_to_save + "/mutations.py", "w") as f:
            f.write(
                "import uuid\n"
                "import boto3\n"
                "from boto3.dynamodb.conditions import Key, Attr\n"
                "import strawberry\n"
                f"from .type import {name.capitalize()}\n\n"
                "dynamodb = boto3.resource('dynamodb')\n"
                f"table = dynamodb.Table('{name}')\n\n"
                "@strawberry.type\n"
                "class Mutation:\n"
                "\t@strawberry.field\n"
                f"\tdef add_{name}(self, {add}) -> {name.capitalize()}:\n"
                "\t\tid = str(uuid.uuid1())\n"
                f"\t\tnew_{name} = {name.capitalize()}.from_row({{ \n"
                f"{add_data}\n"
                f"\t\t}})\n"
                "\t\ttable.put_item(\n"
                "\t\t\tItem={\n"
                f"{add_data}\n"
                "\t\t\t}\n"
                "\t\t)\n"
                f"\t\treturn new_{name}\n\n"
                "\t@strawberry.field\n"
                f"\tdef delete_{name}(self, id: str) -> {name.capitalize()}:\n"
                f"\t\t{name} = table.query(\n"
                "\t\t\tKeyConditionExpression=Key('id').eq(id)\n"
                "\t\t)['Items']\n"
                f"\t\tif not {name}:\n"
                f"\t\t\traise Exception('{name} not found')\n"
                "\t\ttable.delete_item(\n"
                "\t\t\tKey={'id': id},\n"
                "\t\t)\n"
                f"\t\t{name} = {name}[0]\n"
                f"\t\treturn {name.capitalize()}.from_row({name})\n\n"
                "\t@strawberry.field\n"
                f"\tdef update_{name}(self, id: str, {add}) -> {name.capitalize()}:\n"
                "\t\tto_update = {}\n"
                f"{updating_fileds}\n"
                "\t\tresponse = None\n"
                "\t\ttry:\n"
                "\t\t\tresponse = table.update_item(\n"
                "\t\t\t\tKey={'id': id},\n"
                f"\t\t\t\tUpdateExpression='{updating_dynamo_expression}',\n"
                "\t\t\t\tExpressionAttributeValues=to_update,\n"
                "\t\t\t\tReturnValues='UPDATED_NEW',\n"
                "\t\t\t\tConditionExpression='attribute_exists(id)',\n"
                "\t\t\t\tExpressionAttributeNames={}\n"
                "\t\t\t)\n"
                "\t\texcept Exception as e:\n"
                "\t\t\tif 'ConditionalCheckFailedException' in str(e):\n"
                f"\t\t\t\traise Exception('{name.capitalize()} does not exist')\n"
                f"\t\treturn {name.capitalize()}.from_row({{\n"
                f"\t\t\t{updating_response}\n"
                "\t\t})"
            )

    def create_lambda(self):
        name = self.strawberry_type.__strawberry_definition__.name.lower()

        if (self.check_file_exists(self.path_to_save + "/lambda_function.py")):
            print(f"File already exists in {self.path_to_save}/lambda_function.py")
            return

        with open(self.path_to_save + "/lambda_function.py", "w") as f:
            f.write(
                "import json\n"
                "import strawberry\n"
                f"from {name}.query import Query\n"
                f"from {name}.mutations import Mutation\n\n"
                "def handler(event, context):\n"
                "\tbody = json.loads(event['body'])\n"
                "\tif not body.get('query'):\n"
                "\t\treturn {\n"
                "\t\t\t'statusCode': 400,\n"
                "\t\t\t'body': 'Bad body bro'\n"
                "\t\t}\n"
                "\tschema = strawberry.Schema(query=Query, mutation=Mutation)\n"
                "\tresult = schema.execute_sync(body['query'])\n"
                "\treturn {\n"
                "\t\t'statusCode': 200,\n"
                "\t\t'body': json.dumps(\n"
                "\t\t\t{\n"
                "\t\t\t\t'data': result.data,\n"
                "\t\t\t\t'errors': [\n"
                "\t\t\t\t\t{\n"
                "\t\t\t\t\t\t'msg': err.message,\n"
                "\t\t\t\t\t\t'location': [\n"
                "\t\t\t\t\t\t\t{'line': loc.line, 'column': loc.column}\n"
                "\t\t\t\t\t\t\tfor loc in err.locations\n"
                "\t\t\t\t\t\t]\n"
                "\t\t\t\t\t}\n"
                "\t\t\t\t\tfor err in result.errors\n"
                "\t\t\t\t] if result.errors else []\n"
                "\t\t\t}\n"
                "\t\t)\n"
                "\t}\n"
            )

    def run(self):
        self.create_query()
        self.create_mutations()
        self.create_lambda()

Creator(Account, "account").run()
