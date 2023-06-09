import os
import json
import boto3



def lambda_handler(event, context):
    """
    Main function of the lambda to perform a get operation for a subscriber in the subscribers table of the database.

    Args:
        event (dict): Event that contains the subscriber's data.
        context (object): Lambda context object.

    Returns:
        dict: Lambda response.
    """
    action = 'get'
    body = event['queryStringParameters'] if event['queryStringParameters'] is not None else None
    telefono_celular = body['telefono_celular'] if isinstance(body, dict) and 'telefono_celular' in body else None
    payload = {
        "body" : {
            'telefono_celular' : telefono_celular
        },
        'action':action
    }
    #create the lambda client
    client_lambda = boto3.client('lambda')

    # Invoke and wait the query lambda
    response = client_lambda.invoke(
        FunctionName=os.environ['LAMBDA_QUERIES_ARN'],
        InvocationType='RequestResponse',
        Payload=json.dumps(payload),
    )
    response = json.loads(response['Payload'].read().decode('utf-8'))

    return {
        'statusCode': response['statusCode'],
        'headers': {
            'Access-Control-Allow-Headers': '*',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'OPTIONS,GET'
        },
        'body': json.dumps(response['response'])
    }