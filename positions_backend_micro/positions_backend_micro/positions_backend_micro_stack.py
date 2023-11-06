from constructs import Construct
from aws_cdk import (
    Duration,
    Stack,
    aws_lambda as lambda_,
    aws_iam as iam,
    aws_dynamodb as dynamodb,
    aws_cognito as cognito,
)
import aws_cdk.aws_apigatewayv2_alpha as apigwv2
from aws_cdk.aws_apigatewayv2_integrations_alpha import HttpLambdaIntegration
from aws_cdk.aws_apigatewayv2_authorizers_alpha import HttpUserPoolAuthorizer
from aws_cdk import RemovalPolicy


class PositionsBackendMicroStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        user_pool = cognito.UserPool(
            self,
            id="positions-backend-pool",
            user_pool_name="positions-backend-pool",
            removal_policy=RemovalPolicy.DESTROY,
            self_sign_up_enabled=False,
            sign_in_aliases={"email": True},
            auto_verify={"email": True},
            password_policy=cognito.PasswordPolicy(
                min_length=6,
                require_digits=True,
                require_lowercase=True,
                require_symbols=True,
                require_uppercase=True,
            ),
            account_recovery=cognito.AccountRecovery.EMAIL_ONLY,
            email=cognito.UserPoolEmail.with_cognito("support@myawesomeapp.com"),
            mfa=None,
            enable_sms_role=False,
        )

        user_pool.add_domain(
            "positions-backend-domain",
            cognito_domain=cognito.CognitoDomainOptions(domain_prefix="positions-backend-domain"),
        )

        user_pool_client = cognito.UserPoolClient(
            self,
            id="positions-backend-client",
            user_pool=user_pool,
            user_pool_client_name="positions-backend-client",
            disable_o_auth=False,
            o_auth=cognito.OAuthSettings(
                flows=cognito.OAuthFlows(authorization_code_grant=True),
                scopes=[cognito.OAuthScope.OPENID],
                callback_urls=["https://example.com/"],
                logout_urls=["https://example.com/"],
            ),
        )

        authorizer = HttpUserPoolAuthorizer(
            "positions-backend-authorizer",
            pool=user_pool,
            user_pool_clients=[user_pool_client],
        )

        http_api = apigwv2.HttpApi(
            self,
            "positions-backend-micro",
            cors_preflight=apigwv2.CorsPreflightOptions(
                allow_headers=["Authorization"],
                allow_methods=[apigwv2.CorsHttpMethod.ANY],
                allow_origins=["*"],
                max_age=Duration.days(10),
            ),
        )

        for endpoint in ["account", "asset", "broker", "deposit", "money", "position"]:
            lambda_function = lambda_.Function(
                self,
                f"{endpoint}EndpointLambda",
                handler="lambda_function.lambda_handler",
                runtime=lambda_.Runtime.PYTHON_3_11,
                code=lambda_.Code.from_asset(f"endpoints/{endpoint}.zip"),
                description=f"handles {endpoint} endpoint.",
                function_name=f"{endpoint}EndpointLambda",
            )
            lambda_function.add_to_role_policy(
                iam.PolicyStatement(
                    effect=iam.Effect.ALLOW,
                    actions=["dynamodb:*"],
                    resources=["*"],
                )
            )

            books_integration = HttpLambdaIntegration(
                f"{endpoint}Integration", lambda_function
            )
            http_api.add_routes(
                path=f"/{endpoint}",
                methods=[apigwv2.HttpMethod.ANY],
                integration=books_integration,
                authorizer=authorizer,
            )

            dynamodb.Table(
                self,
                id=f"{endpoint}_dynamodbTable",
                table_name=endpoint,
                partition_key=dynamodb.Attribute(
                    name="id", type=dynamodb.AttributeType.STRING
                ),
                billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST,
            )
