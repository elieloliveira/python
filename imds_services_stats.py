#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys # pip install sys
import requests  # pip install requests
import smtplib  # pip install smtplib
import time 
from threading import Thread

def Consumir_API_Saneamento():
    try:
        url = "http://consultatributos.com.br:8080/api/v1/public/Saneamento"
        
        body = "{\n \"Cabecalho\":{\"cnpj\":\"39104545850\",\"uf\":\"PR\",\"crt\":\"3\",\"cnae\":\"1234567\",\"amb\":\"2\",\"versao\":\"2\"},\n \"Produto\":[\n \t{\"id\":\"1\",\"EAN\":\"\",\"cod\":\"1\",\"descricao\":\"ARROZ 01\"}\n \t]\n}"
        headers = {
            'login': "10353098000114",
            'senha': "deusfiel",
            'Content-Type': "application/json",
            'cache-control': "no-cache",
            'Postman-Token': "85b838d3-ca16-4cce-b18e-d00a5d54ab07"
            }

        erros = int(0)
        giros = int(1)

        while giros <= 2: #Consome a API 2x
            response = requests.request("POST", url, data=body, headers=headers)

            if response.status_code != 200: #Se der algum erro incrementa a variável "erros"
                erros += 1
            else:
                if(erros > 0): #Tratamento para decrementar a variável "erros"
                    erros -= 1

            giros += 1

            if(giros <= 2):
                time.sleep(600) #10 minutos

        if(erros > 1):
            EnviarEmail("Web API COM ERRO.")
    except Exception as e:
        GravaLogTexto("Erro Consumir_WS_Consulta: " + str(e))


def Consumir_WS_Consulta():
    try:
        url = "http://consultatributos.com.br:8888/wsGeral.asmx"

        querystring = {"WSDL":""}

        payload = "<x:Envelope xmlns:x=\"http://schemas.xmlsoap.org/soap/envelope/\" xmlns:tem=\"http://tempuri.org/\">\n <x:Header/><x:Body>\n<tem:MetodoConsultaProdutoXML>\n<tem:xml>\n<![CDATA[\n<EnvioDados><Cabecalho><CNPJ>10353098000114</CNPJ><UF>SP</UF><CRT>1</CRT><CNAE>1099601</CNAE><tpConsulta>1</tpConsulta><codFaixa>101</codFaixa><versao>2.0</versao></Cabecalho><Produto><ID>1</ID><EAN>7896720320312</EAN><codigoInterno></codigoInterno><Descricao>GAS DE COZINHA</Descricao></Produto></EnvioDados>\n]]>\n</tem:xml>\n</tem:MetodoConsultaProdutoXML>\n</x:Body>\n</x:Envelope>"
        headers = { 'Content-Type': "text/xml",
                    'cache-control': "no-cache",
                    'Postman-Token': "f6e5fa38-0f78-425c-969f-3b61ebafe606"
                }

        erros = int(0)
        giros = int(1)

        while giros <= 2: #Consome o WS 2x
            response = requests.request("POST", url, data=payload, headers=headers, params=querystring)

            if response.status_code != 200: #Se der algum erro incrementa a variável "erros"
                erros += 1
            else:
                if(erros > 0): #Tratamento para decrementar a variável "erros"
                    erros -= 1

            giros += 1

            if(giros <= 2):
                time.sleep(600) #10 minutos

        if(erros > 1):
            EnviarEmail("WEB SERVICE COM ERRO.")
    except Exception as e:
        GravaLogTexto("Erro Consumir_WS_Consulta: " + str(e))


def EnviarEmail(msgParam): 
    try:
        from_addr = ['suporte@imendes.com.br']
        to_addr_list = ['eliel@imendes.com.br']
        #to_addr_list = ['eliel@imendes.com.br', 'renzo@imendes.com.br']
        #cc_addr_list = ['eliels2@gmail.com', 'renzo@imendes.com.br']
        subject = "Teste Email Python"
        message = msgParam
        login = "suporte@imendes.com.br"
        password = "suporte@17!!"
        smtpserver='smtp.gmail.com:587'

        header  = 'From: %s\n' % from_addr
        header += 'To: %s\n' % ','.join(to_addr_list)
        #header += 'Cc: %s\n' % ','.join(cc_addr_list)
        header += 'Subject: %s\n\n' % subject
        message = header + message

        server = smtplib.SMTP(smtpserver)
        server.starttls()
        server.login(login,password)
        problems = server.sendmail(from_addr, to_addr_list, message)
        server.quit()
    except Exception as e:
        GravaLogTexto("Erro Consumir_WS_Consulta: " + str(e))


def GravaLogTexto(msgLog):
    # Criando e escrevendo em arquivos de texto (modo 'w').
    arquivo = open('log.txt','a')
    arquivo.write(msgLog + "\n")
    arquivo.close()


#Calling methods below
Consumir_API_Saneamento()
Consumir_WS_Consulta()

print('Processo finalizado')