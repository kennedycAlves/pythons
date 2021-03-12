import re
from urllib.request import urlopen
from io import StringIO
import csv
import mysql.connector
from mysql.connector import errorcode


try:
    con = mysql.connector.connect(user='', password='', host='', database='')
except mysql.connector.Error as erro:
    if erro.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Usuário ou senha inválidos")
    elif erro.errno == errorcode.ER_BAD_DB_ERROR:
        print("Banco de dados não encontrado")
    else:
        print(erro)


arquivo = open("C:/Users/T-Gamer/PycharmProjects/pythonProject1/venv/dados.txt", "w")

url = "http://www.anatel.gov.br/dadosabertos/PDA/Estacoes_Licenciadas/Estacoes_Licenciadas_SCM.csv"
dados = str(urlopen(url).read().decode('iso-8859-1'))
arqDados = StringIO(dados)
csvReade = csv.reader(arqDados)


for linha in csvReade:
    arquivo.writelines(str(linha).strip() + '\n')

arquivo.close

lerArquivo = open("C:/Users/T-Gamer/PycharmProjects/pythonProject1/venv/dados.txt", "r")

def limpa(entrada):
    entrada = re.sub(r'\s+', " ", entrada)
    entrada = re.sub(r'\\n', "", entrada)
    entrada = entrada.replace("\\", "")
    entrada = entrada.replace("\"", "")
    entrada = entrada.replace("\'", "")
    entrada = entrada.replace("[", "")
    entrada = entrada.replace("]", "")
    entrada = entrada.split(";")
    return entrada




def criarDatabase():
    cursor = con.cursor()
    lerArquivo.seek
    primeiralinha = lerArquivo.readline()
    campos = limpa(primeiralinha)
    #print(campos)

    cursor.execute("CREATE DATABASE IF NOT EXISTS Estacoes_Licenciadas_DB")
    cursor.execute("USE Estacoes_Licenciadas_DB ")
    cursor.execute("CREATE TABLE IF NOT EXISTS Estacoes_Licenciadas_TB (ID INT NOT NULL AUTO_INCREMENT PRIMARY KEY, PRESTADORA VARCHAR(255), CNPJ VARCHAR(255), NUMERO_ESTACAO VARCHAR(255),\
        TIPO_ESTACAO VARCHAR(255), UF VARCHAR(255), CODIGO_UF VARCHAR(255),  MUNICIPIO VARCHAR(255), LOGRADOURO VARCHAR(255), LATITUDE VARCHAR(255), \
            LONGITUDE VARCHAR(255), ALTITUDE VARCHAR(255), FREQUENCIA_TRANSMISSAO VARCHAR(255), FREQUENCIA_RECEPCAO VARCHAR(255), \
                AZIMUTE VARCHAR(255),  DESIGNACAO_EMISSAO_LARGURA_FAIXA VARCHAR(255), POTENCIA VARCHAR(255), DATA_lICENCIAMENTO VARCHAR(255),\
                    DATA_VALIDADE VARCHAR(255), CODIGO_MUNICIPIO VARCHAR(255), BAIRRO VARCHAR(255)) ")
   
    
criarDatabase()



cursor = con.cursor()
for linha in lerArquivo:
        
    dados = limpa(linha)

    sql = ("INSERT INTO Estacoes_Licenciadas_TB (PRESTADORA, CNPJ, NUMERO_ESTACAO, TIPO_ESTACAO,\
                UF, CODIGO_UF, MUNICIPIO, LOGRADOURO, LATITUDE, LONGITUDE, ALTITUDE, FREQUENCIA_TRANSMISSAO, FREQUENCIA_RECEPCAO,\
                AZIMUTE, DESIGNACAO_EMISSAO_LARGURA_FAIXA, POTENCIA, DATA_LICENCIAMENTO, DATA_VALIDADE,\
                CODIGO_MUNICIPIO, BAIRRO) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)")

    #print (dados)
    
    while(len(dados)) > 20:
        dados.remove("")
        print(dados)

    
    while (len(dados)) < 20:
        dados.append('*')
        print(dados)
    
    

    if(len(dados)) == 20:

        
        prestadora = ''.join(dados[0])
        cnpj = ''.join(dados[1])
        numero_estacao = ''.join(dados[2])
        tipo_estacao = ''.join(dados[3])
        uf = ''.join(dados[4])
        codigo_uf = ''.join(dados[5])
        municipio = ''.join(dados[6])
        logradouro = ''.join(dados[7])
        latitude = ''.join(dados[8])
        longitude = ''.join(dados[9])
        altitude = ''.join(dados[10])
        frequencia_transmissao = ''.join(dados[11])
        frequencia_recepcao = ''.join(dados[12])
        azimute = ''.join(dados[13])
        designacao_emissao_largura_faixa = ''.join(dados[14])
        potencia = ''.join(dados[15])
        data_licenciamento = ''.join(dados[16])
        data_validade = ''.join(dados[17])
        codigo_municipio = ''.join(dados[18])
        bairro = ''.join(dados[19])


        cursor.execute(sql, (prestadora,cnpj,numero_estacao,tipo_estacao,uf,codigo_uf,municipio,logradouro,latitude,longitude,altitude,frequencia_transmissao,
                        frequencia_recepcao,azimute,designacao_emissao_largura_faixa,potencia,data_licenciamento,data_validade,codigo_municipio,bairro))
        
    
    


con.commit()  
 

    
