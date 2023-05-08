from constructs import Construct
from aws_cdk import (
    App, Stack, Duration,
    aws_lambda as _lambda,
    aws_apigateway as apigw
)

class apiStack(Stack):

    def __init__(self, scope: Construct, id: str, cognitoStack, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        gpt_handler = _lambda.DockerImageFunction(self, "gpt-handler",
            code=_lambda.DockerImageCode.from_image_asset(
                directory="handlers/gpt_function/"
            ),
            timeout=Duration.seconds(20)
        )
        
        signup_handler = _lambda.DockerImageFunction(self, "signup-handler",
            code=_lambda.DockerImageCode.from_image_asset(
                directory="handlers/signup_function/"
            ),
            timeout=Duration.seconds(10),
            environment={
                'USER_POOL_ID': cognitoStack.pool.user_pool_id
            }
        )
        cognitoStack.pool.grant(signup_handler, 'cognito-idp:AdminCreateUser')
        
        auth_handler = _lambda.DockerImageFunction(self, "auth-handler",
            code=_lambda.DockerImageCode.from_image_asset(
                directory="handlers/auth_function/"
            ),
            timeout=Duration.seconds(10),
            environment={
                'APP_CLIENT_ID': cognitoStack.client.user_pool_client_id
            }
        )
        
        # acm_certificate_for_example_com: AWS Certificate Manager.Certificate
        api = apigw.LambdaRestApi(
            self, 'api',
            
            #domain_name=apigateway.DomainNameOptions(
            #    domain_name="example.com",
            #    certificate=acm_certificate_for_example_com
            #)
        )
        
        
        gpt_endpoint = api.root.add_resource('gpt')
        gpt_endpoint.add_method('POST', apigw.LambdaIntegration(gpt_handler))
        
        signup_endpoint = api.root.add_resource('signup')
        signup_endpoint.add_method('POST', apigw.LambdaIntegration(signup_handler))
        
        auth_endpoint = api.root.add_resource('login')
        auth_endpoint.add_method('POST', apigw.LambdaIntegration(auth_handler))