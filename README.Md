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

**Exemplo 3**
```shell
aws lambda create-function \
--function-name function01 \
--zip-file fileb://lambda_function.zip \
--runtime python3.9 \
--role arn:aws:iam::251822626625:role/LabRole \
--handler lambda_function.lambda_handler --profile aws_academy --region us-east-1
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

