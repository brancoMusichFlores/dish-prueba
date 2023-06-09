import os
import json
import boto3
import re



def lambda_handler(event, context):
    """
    Main function of the lambda to perform a delete operation for a subscriber in the subscribers table of the database.

    Args:
        event (dict): Event that contains the subscriber's data.
        context (object): Lambda context object.

    Returns:
        dict: Lambda response.
    """
    body = json.loads(event['body'])
    action = 'delete'
    # Extract the phone number in the body
    telefono_celular = body['telefono_celular'] if 'telefono_celular' in body else ' '
    # Validations for delete information
    if not re.match(r'^\d{10}$', telefono_celular):
        return {
            'statusCode': 400,
            'body': 'El teléfono celular debe ser una cadena de 10 dígitos.'
        }
    payload = {
        'body' : {
            'telefono_celular':telefono_celular
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
            'Access-Control-Allow-Methods': 'OPTIONS,DELETE'
        },
        'body': json.dumps(response['response'])
    }