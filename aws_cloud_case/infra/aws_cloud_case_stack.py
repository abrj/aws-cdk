from aws_cdk import (
    Stack,
    aws_dynamodb,
    aws_s3,
    aws_ec2,
    aws_ecs,
    aws_ecs_patterns,
    CfnOutput
)
from constructs import Construct

class AwsCloudCaseStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # The code that defines your stack goes here

        # example resource
        # queue = sqs.Queue(
        #     self, "AwsCloudCaseQueue",
        #     visibility_timeout=Duration.seconds(300),
        # )
        # Dynamo Table
        db_table_name = "demo-table"
        demo_table = aws_dynamodb.Table(
            self, db_table_name,
            partition_key=aws_dynamodb.Attribute(
                name="id",
                type=aws_dynamodb.AttributeType.STRING
            )
        )
        # S3 bucket
        s3_bucket_name = "s3bucket"
        s3 = aws_s3.Bucket(self, s3_bucket_name)

       # VPC and Fargate Cluster
        # NOTE: Limit AZs to avoid reaching resource quotas
        # vpc = aws_ec2.Vpc(
        #     self, "MyVpc",
        #     max_azs=1
        # )

        # cluster = aws_ecs.Cluster(
        #     self, 'aws_ec2Cluster',
        #     vpc=vpc
        # )

        # fargate_service = aws_ecs_patterns.NetworkLoadBalancedFargateService(
        #     self, "FargateService",
        #     cluster=cluster,
        #     task_image_options={
        #         'image': aws_ecs.ContainerImage.from_registry("nginx:latest")
        #     }
        # )

        # fargate_service.service.connections.security_groups[0].add_ingress_rule(
        #     peer = aws_ec2.Peer.ipv4(vpc.vpc_cidr_block),
        #     connection = aws_ec2.Port.tcp(80),
        #     description="Allow http inbound from VPC"
        # )

        # CfnOutput(
        #     self, "LoadBalancerDNS",
        #     value=fargate_service.load_balancer.load_balancer_dns_name
        # )

        vpc = aws_ec2.Vpc(self, "MyVpc", max_azs=3)     # default is all AZs in region

        cluster = aws_ecs.Cluster(self, "MyCluster", vpc=vpc)

        aws_ecs_patterns.ApplicationLoadBalancedFargateService(self, "MyFargateService",
            cluster=cluster,            # Required
            cpu=512,                    # Default is 256
            desired_count=1,            # Default is 1
            task_image_options=aws_ecs_patterns.ApplicationLoadBalancedTaskImageOptions(
                image=aws_ecs.ContainerImage.from_registry("nginx:latest")),
            memory_limit_mib=2048,      # Default is 512
            public_load_balancer=True)  # Default is False
          


