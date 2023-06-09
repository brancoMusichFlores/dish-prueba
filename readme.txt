### REQUISITOS
Se requiere una base de datos MySQL en rds con acceso publico y con un secreto para el usuario.
Nodejs instalado en el equipo.
AWS CLI este instalado y configurado.
Python este instalado en el equipo.
Tener instalado y funcionando docker.

instalar aws serverless
    npm install -g serverless

Inicializar el proyecto npm: 
    npm install serverless-plugin-include-dependencies
    npm install --save serverless-python-requirements

Hacer deploy a la arquitectura serverless:
    sls deploy

### NOTA IMPORTANTE DE EL ROLE DE LAS LAMBDAS
Asegúrate de que el role de las Lambdas tengan acceso a rds, 
acceso a secret manager y permiso de invocar otras lambdas.

Para destruir la arquitectura:
    sls remove

# Endpoints que se cerrarán el 10 de junio de 2023

POST - https://ragv78fu3m.execute-api.us-east-1.amazonaws.com/dev/subscribers
GET - https://ragv78fu3m.execute-api.us-east-1.amazonaws.com/dev/subscribers
GET - https://ragv78fu3m.execute-api.us-east-1.amazonaws.com/dev/subscribers/?telefono_celular=<telefono_celular>
PUT - https://ragv78fu3m.execute-api.us-east-1.amazonaws.com/dev/subscribers
DELETE - https://ragv78fu3m.execute-api.us-east-1.amazonaws.com/dev/subscribers

### EL proyecto cuenta con un archivo de colección de postman para probar los endpoints 
anteriormente mencionados
