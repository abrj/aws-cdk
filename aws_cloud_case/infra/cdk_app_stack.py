from aws_cdk import (
    Stack,
    aws_ecs_patterns,
    aws_ecs,
    CfnOutput,
    aws_dynamodb,
    aws_s3,
    aws_s3_deployment,
    aws_iam
)
from constructs import Construct

class CdkAppStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, cluster, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)


        # Dynamo Table
        db_table_name = "dynamo-demo-table"
        self.demo_table = aws_dynamodb.Table(
            self, db_table_name,
            partition_key=aws_dynamodb.Attribute(
                name="id",
                type=aws_dynamodb.AttributeType.STRING
            )
        )
        # S3 bucket
        s3_bucket_name = "s3-demo-bucket"
        self.s3bucket = aws_s3.Bucket(
            self, 
            s3_bucket_name,
            public_read_access=True)

        # Add html file to S3 bucket
        bucket_deployment = aws_s3_deployment.BucketDeployment(
                self,
                'S3StaticDeploymentHtml',
                sources=[aws_s3_deployment.Source.asset('aws_cloud_case/app/s3-static-website')],
                destination_bucket=self.s3bucket
            )
        # Fargate + LoadBalancer
        self.fargate_service = aws_ecs_patterns.ApplicationLoadBalancedFargateService(self, "LoadBalancedFargateService",
            cluster=cluster,            # Required
            cpu=512,                    # Default is 256
            desired_count=2,            # Default is 1
            task_image_options={
                    "image": aws_ecs.ContainerImage.from_registry("nginxdemos/hello")
                },
            memory_limit_mib=2048,      # Default is 512
            public_load_balancer=True   # Default is False,
        )  

        # Output 
        CfnOutput(
            self, "FargateServiceName",
            value=self.fargate_service.service.service_name
        )
        
        CfnOutput(
            self, "LoadBalancerFullName",
            value=self.fargate_service.load_balancer.load_balancer_full_name
        )

        CfnOutput(
            self, "LoadBalancerName",
            value=self.fargate_service.load_balancer.load_balancer_name
        )   

