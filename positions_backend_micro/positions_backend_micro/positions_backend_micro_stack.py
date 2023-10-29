from constructs import Construct
from aws_cdk import (
    Duration,
    Stack,
    aws_lambda as lambda_,
    aws_iam as iam,
    aws_apigateway as _apigw,
)


class PositionsBackendMicroStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        name = "broker"

        lambda_function = lambda_.Function(
            self, f"{name}EndpointLambda",
            handler="lambda_function.lambda_handler",
            runtime=lambda_.Runtime.PYTHON_3_11,
            code=lambda_.Code.from_asset(f"{name}.zip"),
        )
        lambda_function.add_to_role_policy(iam.PolicyStatement(
            effect=iam.Effect.ALLOW,
            actions=["dynamodb:*"],
            resources=['*'],
        ))

        # aws_apigatewayv2_alpha.HttpApi() # TODO: TRY WITH REST API