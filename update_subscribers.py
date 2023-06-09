import os
import json
import boto3
import re


def lambda_handler(event, context):
    """
    # Main function of the lambda to update a subscriber in the subscribers table of the database.

    Args:
        event (dict): Event that contains the subscriber's data.
        context (object): Lambda context object.

    Returns:
        dict: Lambda response.
    """
    body = json.loads(event['body'])
    action = 'update'
    # Extract data from the request body
    subscriber = body['suscriptor'] if 'suscriptor' in body else None
    if subscriber == None:
        return {
            'statusCode': 400,
            'body': 'La informacion del suscriptor es obligatoria.'
        }
    info_nombre = subscriber['info_nombre'] if 'info_nombre' in subscriber else None
    if info_nombre == None:
        return {
            'statusCode': 400,
            'body': 'La informacion de info_nombre es obligatoria.'
        }
    nombre = info_nombre['nombre'] if 'nombre' in info_nombre else None
    apellido_paterno = info_nombre['apellido_paterno'] if 'apellido_paterno' in info_nombre else ''
    apellido_materno = info_nombre['apellido_materno'] if 'apellido_materno' in info_nombre else ''
    edad = subscriber['edad'] if 'edad' in subscriber else None
    telefono_celular = subscriber['telefono_celular'] if 'telefono_celular' in subscriber else None
    # Validations for update
    if nombre == None or telefono_celular == None:
        return {
            'statusCode': 400,
            'body': 'El nombre y el teléfono celular son obligatorios.'
        }
    if not isinstance(edad, int) or edad < 0:
        return {
            'statusCode': 400,
            'body': 'La edad debe ser un número entero positivo.'
        }
    if not re.match(r'^\d{10}$', telefono_celular):
        return {
            'statusCode': 400,
            'body': 'El teléfono celular debe ser una cadena de 10 dígitos.'
        }
    payload = {
        'body' : {
            'info_nombre':{
                'nombre':nombre,
                'apellido_materno':apellido_paterno,
                'apellido_paterno':apellido_materno
            },
            'edad':edad,
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
            'Access-Control-Allow-Methods': 'OPTIONS,PUT'
        },
        'body': json.dumps(response['response'])
    }
