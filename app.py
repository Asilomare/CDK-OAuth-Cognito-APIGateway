#!/usr/bin/env python3
import os

import aws_cdk as cdk

from stacks.api_stack import apiStack

from stacks.cognitoStack import cognitoStack

app = cdk.App()

cognito_stack = cognitoStack(app, 'cognitoStack')
api_Stack = apiStack(app, "apiStack", cognito_stack)

api_Stack.add_dependency(cognito_stack)

app.synth()
