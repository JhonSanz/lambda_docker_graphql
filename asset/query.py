import strawberry
import boto3
from boto3.dynamodb.conditions import Key
from type import Asset
from utils import PaginationWindow, get_pagination_window


dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('asset')

@strawberry.type
class Query:
	@strawberry.field(description='Get a list of asset')
	def assets(
		self,
		order_by: str,
		limit: int,
		offset: int = 0,
		name: str | None = None,
	) -> PaginationWindow[Asset]:
		response = table.scan()
		assets = response['Items']

		while 'LastEvaluatedKey' in response:
			response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
			assets.extend(response['Items'])

		filters = {}
		if name:
			filters['name'] = name
		return get_pagination_window(
			dataset=assets,
			ItemType=Asset,
			order_by=order_by,
			limit=limit,
			offset=offset,
			filters=filters,
		)

	@strawberry.field(description='Get a asset record.')
	def asset(self, id: str) -> Asset:
		asset = table.query(
			KeyConditionExpression=Key('id').eq(id)
		)['Items']
		if not asset:
			raise Exception('asset not found')
		asset = asset[0]
		return Asset.from_row(asset)
