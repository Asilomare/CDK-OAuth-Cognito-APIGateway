from constructs import Construct
from aws_cdk import (
    App, Stack, Duration,
    aws_cognito as cognito,
    aws_lambda as _lambda
)

class cognitoStack(Stack):

    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)
        
        self.pool = cognito.UserPool(self, "Pool"
        
            # For MFA:
            #mfa=cognito.Mfa.REQUIRED,
            #mfa_message="Your signup code for {APP_NAME}: {####}",
            
            
            # For custom auth/onboarding workflows:
            # https://docs.aws.amazon.com/cognito/latest/developerguide/cognito-user-identity-pools-working-with-aws-lambda-triggers.html
            # auth_challenge_fn : aws_lambda.Function
            
            #lambda_triggers=cognito.UserPoolTriggers(
            #    create_auth_challenge=auth_challenge_fn
            #)
            
            
            # For costum password requirements:
            
            #password_policy=cognito.PasswordPolicy(
            #    min_length=12,
            #    require_lowercase=True,
            #    require_uppercase=True,
            #    require_digits=True,
            #    require_symbols=True,
            #    temp_password_validity=Duration.days(3)
            #)
        )
        
        self.client = self.pool.add_client("poolclient",
            auth_flows=cognito.AuthFlow(user_password=True),
        )