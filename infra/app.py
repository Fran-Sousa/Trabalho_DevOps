"""Infra com AWS CDK."""

import os

from aws_cdk import App, Environment, LegacyStackSynthesizer
from stack import ToDoStack

app = App()
image_tag = app.node.try_get_context("imageTag") or "latest"
env = Environment(
    account=os.environ.get("CDK_DEFAULT_ACCOUNT"),  # Uso do OIDC
    #region=os.environ.get("CDK_DEFAULT_REGION"),
    region="us-east-1"
)

ToDoStack(
    app,
    "ToDoStack",  # O mesmo configurado em github secrets CDK_STACK_NAME
    image_tag=image_tag,
    env=env,
    synthesizer=LegacyStackSynthesizer(),
)

app.synth()
