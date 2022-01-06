from aws_cdk import (
    Stack,
    aws_ecs,
    aws_ec2,
    CfnOutput
)
from constructs import Construct

class CdkNetworkStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        VPC_NAME = "CDK-VPC"
        ECS_CLUSTER_NAME = "ECS-CLUSTER"
        # VPN
        self.vpc = aws_ec2.Vpc(self, VPC_NAME, max_azs=3)     # default is all AZs in region

        # ECS cluster
        self.cluster = aws_ecs.Cluster(self, ECS_CLUSTER_NAME, vpc=self.vpc)