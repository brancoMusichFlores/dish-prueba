import os
import json
import mysql.connector
import boto3


def get_secret(secret_arn):
    """
    Get a secret of secret manager.

    Args:
        secret_arn (str): secret's arn.

    Returns:
        dict: A dict with the secret's value.
    """

    client = boto3.client('secretsmanager')
    response = client.get_secret_value(SecretId=secret_arn)
    if 'SecretString' in response:
        secret = json.loads(response['SecretString'])
        return secret
    else:
        # Handle binary secrets if necessary
        secret = response['SecretBinary']
        return secret


def lambda_handler(event, context):
    """
    Main function of the lambda to perform subscriber-related operations in 
    the subscribers table of the database.

    Args:
        event (dict): Event that contains the subscriber's data.
        context (object): Lambda context object.

    Returns:
        dict: Lambda response.
    """
    secret_arn = os.environ['SECRET_ARN']
    action = event['action']
    subscriber = event['body']

    if action.lower() == 'get':
        telefono_celular = subscriber['telefono_celular']

    elif action.lower() == 'create' or action.lower() == 'update':
        info_nombre = subscriber['info_nombre']
        nombre = info_nombre['nombre'] 
        apellido_paterno = info_nombre['apellido_paterno'] 
        apellido_materno = info_nombre['apellido_materno']
        edad = subscriber['edad'] 
        telefono_celular = subscriber['telefono_celular'] 
        
    elif action.lower() == 'delete':
        telefono_celular = subscriber['telefono_celular'] 

    try:
        # Retrieve the password from the secret
        secret = get_secret(secret_arn)
        conn = mysql.connector.connect(
            host=os.environ['DB_HOST'],
            user=secret['username'],
            password=secret['password'],
            database=os.environ['DB_DATABASE']
        )
        cursor = conn.cursor()
        if action.lower() == 'get':
            # Execute the SQL query to retrieve all subscriber records
            if telefono_celular == None:
                sql = "SELECT * FROM subscribers"
                cursor.execute(sql)
            else:
                sql = "SELECT * FROM subscribers WHERE telefono_celular = %s"
                values = (telefono_celular,)
                cursor.execute(sql, values)
            # Fetch all rows from the result set
            rows = cursor.fetchall()
            # Format the result as a list of dictionaries
            subscribers = []
            for row in rows:
                subscriber = {
                    "info_nombre":{
                        'nombre': row[1],
                        'apellido_materno': row[2],
                        'apellido_paterno': row[3],
                    },
                    'edad': row[4],
                    'telefono_celular': row[0]
                }
                subscribers.append(subscriber)
            
            response = {
            'statusCode': 200,
            'response': subscribers
            }

        elif action.lower() == 'create':
            #Execute the SQL query to check if the record already exists
            sql = "SELECT COUNT(*) FROM subscribers WHERE telefono_celular = %s"
            values = (telefono_celular,)
            cursor.execute(sql, values)
            # Obtener el resultado de la consulta
            cantidad_subscriptores = cursor.fetchone()[0]
            if cantidad_subscriptores != 0:
                # Close the database connection
                cursor.close()
                conn.close()
                return {
                    'statusCode': 400,
                    'response': 'Ya existe un suscriptor con ese telefono celular.'
                }
            # Execute the SQL query to insert the record
            sql = "INSERT INTO subscribers (nombre, apellido_materno, apellido_paterno, edad, telefono_celular) VALUES (%s, %s, %s, %s, %s)"
            values = (nombre, apellido_materno,
                    apellido_paterno, edad, telefono_celular)
            cursor.execute(sql, values)
            # Confirm the changes in the database
            conn.commit()
            response = {
                'statusCode': 200,
                'response': 'Registro creado exitosamente.'
            }
    
        elif action.lower() == 'update':
            #Execute the SQL query to check if the record already exists
            sql = "SELECT COUNT(*) FROM subscribers WHERE telefono_celular = %s"
            values = (telefono_celular,)
            cursor.execute(sql, values)
            # Obtener el resultado de la consulta
            cantidad_subscriptores = cursor.fetchone()[0]
            if cantidad_subscriptores < 1:
                # Close the database connection
                cursor.close()
                conn.close()
                return {
                    'statusCode': 400,
                    'response': 'No existe un suscriptor con ese telefono celular.'
                }
            # Execute the SQL query to update the record
            sql = "UPDATE subscribers SET nombre = %s, apellido_materno = %s, apellido_paterno = %s, edad = %s WHERE telefono_celular = %s"
            values = (nombre, apellido_materno,
                    apellido_paterno, edad, telefono_celular)
            cursor.execute(sql, values)

            # Confirm the changes in the database
            conn.commit()
            response ={
            'statusCode': 200,
            'response': 'Registro actualizado exitosamente.'
            }

        elif action.lower() == 'delete':
            #Execute the SQL query to check if the record already exists
            sql = "SELECT COUNT(*) FROM subscribers WHERE telefono_celular = %s"
            values = (telefono_celular,)
            cursor.execute(sql, values)
            # Obtener el resultado de la consulta
            cantidad_subscriptores = cursor.fetchone()[0]
            if cantidad_subscriptores < 1:
                # Close the database connection
                cursor.close()
                conn.close()
                return {
                    'statusCode': 400,
                    'response': 'No existe un suscriptor con ese telefono celular.'
                }
            # Execute the SQL query to delete the record
            sql = "DELETE FROM subscribers WHERE telefono_celular = %s"
            values = (telefono_celular,)
            cursor.execute(sql, values)

            # Confirm the changes in the database
            conn.commit()
            response = {
            'statusCode': 200,
            'response': 'Registro eliminado exitosamente.'
            }

        # Close the database connection
        cursor.close()
        conn.close()

        return response
    
    except Exception as e:
        # Close the database connection
        cursor.close()
        conn.close()
        return {
            'statusCode': 500,
            'response': str(e)
        }