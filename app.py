#!/usr/bin/env python3
import os

import aws_cdk as cdk

# from aws_cloud_case.infra.aws_cloud_case_stack import AwsCloudCaseStack
from aws_cloud_case.infra.cdk_network_stack import CdkNetworkStack
from aws_cloud_case.infra.cdk_app_stack import CdkAppStack
from aws_cloud_case.infra.cdk_api_stack import CdkApiStack

app = cdk.App()

# NetworkStack: Vpc, ECS Cluster
ecs_cluster = CdkNetworkStack(app, "CDK-NETWORK-STACK")
# ApplicationStack: S3, DynamoTable, Fargate + loadbalancer
app_stack = CdkAppStack(app, "CDK-APP-STACK", cluster=ecs_cluster.cluster)
# Http: API Gateway 
http_stack = CdkApiStack(app, 
    "CDK-API-STACK", 
    s3_bucket=app_stack.s3bucket, 
    dynamo_table=app_stack.demo_table, 
    fargate_service=app_stack.fargate_service
)

app.synth()
