from aws_cdk import (
    Arn,
    Stack,
    aws_apigateway
)
from constructs import Construct

class CdkApiStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, s3_bucket, dynamo_table, fargate_service, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        api_gateway = aws_apigateway.RestApi(self, "API-GATEWAY")
        s3_rest_api_integration = aws_apigateway.HttpIntegration(
            url= s3_bucket.url_for_object("index.html")
        )
        
        fargate_rest_api_integration = aws_apigateway.HttpIntegration(
            url="http://" + fargate_service.load_balancer.load_balancer_dns_name
        )
        api_gateway.root.resource_for_path("hello-s3").add_method("GET", s3_rest_api_integration)
        api_gateway.root.resource_for_path("hello-fargate").add_method("GET", fargate_rest_api_integration)
