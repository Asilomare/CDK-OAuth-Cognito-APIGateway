import json
from os import environ
import boto3
import datetime

# Custom JSON serializer to handle datetime objects
class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.isoformat()
        return super(CustomJSONEncoder, self).default(obj)

def lambda_handler(event, context):
    
    payload = event['queryStringParameters']
    
    client_id = environ['APP_CLIENT_ID']
    challenge_name = payload['challenge_name']
    session = payload['session']
    challenge_responses = json.loads(payload['challenge_responses'])
    
    # Initialize the Cognito client
    cognito_client = boto3.client('cognito-idp')

    # Respond to the auth challenge
    try:
        response = cognito_client.respond_to_auth_challenge(
            ClientId=client_id,
            ChallengeName=challenge_name,
            Session=session,
            ChallengeResponses=challenge_responses
        )
        
        # Properly format the response for API Gateway
        return {
            'statusCode': 200,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps(response, cls=CustomJSONEncoder)
        }

    except cognito_client.exceptions.InvalidParameterException as e:
        return {
            'statusCode': 400,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({'error': 'Invalid parameters'})
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({'error': str(e)})
        }
