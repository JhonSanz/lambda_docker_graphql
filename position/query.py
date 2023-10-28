import strawberry
import boto3
from boto3.dynamodb.conditions import Key
from .type import Position
from .utils import PaginationWindow, get_pagination_window


dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('position')

@strawberry.type
class Query:
	@strawberry.field(description='Get a list of position')
	def positions(
		self,
		order_by: str,
		limit: int,
		offset: int = 0,
		name: str | None = None,
	) -> PaginationWindow[Position]:
		response = table.scan()
		positions = response['Items']

		while 'LastEvaluatedKey' in response:
			response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
			positions.extend(response['Items'])

		filters = {}
		if name:
			filters['name'] = name
		return get_pagination_window(
			dataset=positions,
			ItemType=Position,
			order_by=order_by,
			limit=limit,
			offset=offset,
			filters=filters,
		)

	@strawberry.field(description='Get a position record.')
	def position(self, id: str) -> Position:
		position = table.query(
			KeyConditionExpression=Key('id').eq(id)
		)['Items']
		if not position:
			raise Exception('position not found')
		position = position[0]
		return Position.from_row(position)
