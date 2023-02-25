# Documentação relacionada a 'invocação' (invoke) de uma função lambda feita em python.
# https://docs.aws.amazon.com/pt_br/lambda/latest/dg/python-handler.html

#deploy
#https://docs.aws.amazon.com/lambda/latest/dg/python-package.html

#Passos para publicação do código de uma função
# 1.  Você pode criar o arquivo 'inline' e fazer a publicação
# 2. Você pode criar um bucket (s3)e subir o 'zip' da aplicação
# 3. Você pode provisionar o ambiente via cloudformation para criar toda estrutura.

def lambda_handler(event, context):
    message = 'Hello {} {}!'.format(event['nome'], event['sobrenome'])  
    return { 
        'message' : message
    }
