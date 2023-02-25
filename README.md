# Aula 25-02-2023

# FATEC

## Configuração ambiente AWS

## Deploy de função zip

### Criar nova função à partir de um zip

Para publição via CLI:

**Detalhe**
```shell
aws lambda create-function \
--function-name $NOME_FUNCAO \
--zip-file fileb://$ARQUIVO_ZIP.zip \
--runtime python3.9 \
--role $ARN_DA_ROLE_PARA_PUBLICACAO \
--handler $NOME_FUNCAO.$METODO_DEFINIDO_NO_ARQUIVO_PYTHON
```

**Exemplo 1**
```shell
aws lambda create-function \
--function-name meu-app-python \
--zip-file fileb://meu-app-python.zip \
--runtime python3.9 \
--role arn:aws:iam::251822626625:role/LabRole \
--handler meu-app-python.lambda_handler
```

**Exemplo 2**
```shell
aws lambda create-function \
--function-name novaFuncao \
--runtime python3.9 z
--handler me-do-arquivo.lambda_handler \
--role arn:aws:iam::302614027063:role/LabRole \
--zip-file fileb://lambda_function.zip
```
#dTaBFso3
**Exemplo 3**
```shell
aws lambda create-function \
--function-name function01 \
--zip-file fileb://lambda_function.zip \
--runtime python3.9 \
--role arn:aws:iam::251822626625:role/LabRole \
--handler lambda_function.lambda_handler --profile aws_academy --region us-east-1
```
### Resultado

```json
{
    "FunctionName": "function03",
    "FunctionArn": "arn:aws:lambda:us-east-1:251822626625:function:function03",
    "Runtime": "python3.9",
    "Role": "arn:aws:iam::251822626625:role/LabRole",
    "Handler": "lambda_function.lambda_handler",
    "CodeSize": 563,
    "Description": "",
    "Timeout": 3,
    "MemorySize": 128,
    "LastModified": "2023-02-25T15:45:39.455+0000",
    "CodeSha256": "gXgyb3wmShcyS3rm2nBZnRF0Myr0e4/KuAR3MA2on+M=",
    "Version": "$LATEST",
    "TracingConfig": {
        "Mode": "PassThrough"
    },
    "RevisionId": "f320acf6-3673-41e9-8a26-21f52542bbb6",
    "State": "Pending",
    "StateReason": "The function is being created.",
    "StateReasonCode": "Creating",
    "PackageType": "Zip"
}

```

### Atualizar função à partir de um arquivo zip.

**Atualizar função**
```shell
aws lambda udpdate-function \
--function-name meu-app-python \
--zip-file fileb://meu-app-python.zip \
--runtime python3.9 \
--role arn:aws:iam::251822626625:role/LabRole \
--handler index.handler
```

## Criação da tabela no DynamoDB


## Inserção de dados via linha de comando

## Linux
```shell
aws dynamodb put-item
--table-name temperatura
--item '{
 "idDispositivo": {
  "S": "9aa435ca-b535-11ed-afa1-0242ac120002"
 },
 "dataEvento": {
  "S": "25-02-2023"
 }
}'
```

ou exemplo passando profile e região como parâmetro
## Linux
```shell
aws dynamodb put-item
--table-name temperatura
--item '{
 "idDispositivo": {
  "S": "9aa435ca-b535-11ed-afa1-0242ac120002"
 },
 "dataEvento": {
  "S": "25-02-2023"
 },
 "temperatura": {"N": "30"}
}'
```

### Windows (precisa 'escapar' o texto)
```shell
aws dynamodb put-item --table-name temperatura --item '{\"idDispositivo\": {\"S\": \"9aa435ca-b535-11ed-afa1-0242ac120002\"},\"dataEvento\": {\"S\": \"25-02-2023\"},\"temperatura\": {\"N\": \"30\"}}'
```

# Instalar pip
```shell
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
```

```shell
py -m pip install [options] <requirement specifier> [package-index-options] ...
py -m pip install [options] -r <requirements file> [package-index-options] ...
py -m pip install [options] [-e] <vcs project url> ...
py -m pip install [options] [-e] <local project path> ...
py -m pip install [options] <archive url/path> ...
``` 

## Requirements.txt
Criar na raiz do projeto um arquivo requirements.txt
boto3==1.26.79

## Para instalar
```shell
pip install -r requirements.txt
```

# Criar função lambda para persistência no DynamoDB

```python
# Documentação relacionada a 'invocação' (invoke) de uma função lambda feita em python.
# https://docs.aws.amazon.com/pt_br/lambda/latest/dg/python-handler.html

#deploy
#https://docs.aws.amazon.com/lambda/latest/dg/python-package.html

#Passos para publicação do código de uma função
# 1.  Você pode criar o arquivo 'inline' e fazer a publicação
# 2. Você pode criar um bucket (s3)e subir o 'zip' da aplicação
# 3. Você pode provisionar o ambiente via cloudformation para criar toda estrutura.

from datetime import datetime
import json
import logging
import boto3
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

#Tudo numa função LAMBDA começa pelo HANDLER.
# O HANDLER é responsável para 'iniciar' o processamento de uma função lambda.
# Geralmente em código python, podemos 'substituir' pelo método main(event, context)
def lambda_handler(event, context):

    #Nome da função com ARN (item identificador)
    logger.info(f"Lambda function ARN: {context.invoked_function_arn}")
    
    #Nome do grupo de log que é exibid no cloudwatch
    logger.info(f"CloudWatch log stream name: {context.log_stream_name}") 
    logger.info(f"CloudWatch log group name: {context.log_group_name}")
    
    #ID da requisição do lambda
    logger.info(f"Lambda Request ID: {context.aws_request_id}")
    
    logger.info(f"Início processamento de dados do dispositivo nº {event['idDispositivo']}")
    
    resultado = processar_dados(event, context)
    
    logger.info(f"Fim processamento de dados do dispositivo nº {event['idDispositivo']}")    
    logger.debug(resultado)
    
    return resultado
    

def processar_dados(event, context):
    response = ""
    
    # Inserir dependências no projeto do dynamodb seja o resource e cliente.
    # Um manipula os dados dentro do dynamo e o cilente, faz as consultas.
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('temperatura')
    
    #Gerar o timestamp (registro do evento) para persistência
    dataEvento = (datetime.now()).strftime("%Y-%m-%d %H:%M:%S")
    
    #Capturando dados que foram enviados por um recurso: lambda, SQS (fila), SNS(tópico)
    #As informações 'chegam' na função através de EVENTOS
    idDispositivo = event['idDispositivo']
    temperatura = event['temperatura']
    
    #Preparar os dados para inserção no DYNAMODB
    #Chamar a instância do cliente para 'manipular' as informações no banco de dados
    try:
        
        #Preparando dados para persistência
        item={
                'dataEvento': dataEvento,
                'idDispositivo': idDispositivo,
                'temperatura': int(temperatura)
            }
        logger.info("Criado objeto para persistência")
        
        #Persistência dos dados
        #response = dynamodb.put_item(TableName='temperatura',Item=item)
        response = table.put_item(Item=item)
        
        #Retorno dos dados
        return {
            'statusCode': 200,
            'message': json.dumps('Registro inserido com sucesso!'),
            'data': [item],
        }
        
    except:
        logger.debug(f"Valores recebidos: {item}")
        logger.debug(f"Retorno dynamoDB: {response}")
        #https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/400
        return {
            'statusCode': 400,
            'message': json.dumps('Erro ao registrar temperatura.'),
            'data': [item],
        }
```