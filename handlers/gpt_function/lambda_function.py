import openai
import json
import boto3

def lambda_handler(event, context):
    payload = event['queryStringParameters']

    result = process_request(payload)

    response_data = {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json'
        },
        'body': json.dumps(result)
    }

    return response_data

def process_request(data):
    openai.api_key = data['key']
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": data['message']}
        ]
    )
    return completion.choices[0].message.content
