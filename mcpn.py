import re
from urllib.request import urlopen
from urllib.error import HTTPError, URLError
from bs4 import BeautifulSoup
import mysql.connector
from mysql.connector import errorcode
from datetime import date

try:
    con = mysql.connector.connect(user='root', password='1q2w3e4r,', host='127.0.0.1', database='comprasnet')
except mysql.connector.Error as erro:
    if erro.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Usuário ou senha inválidos")
    elif erro.errno == errorcode.ER_BAD_DB_ERROR:
        print("Banco de dados não encontrado")
    else:
        print(erro)

arquivo = open("C:/PycharmProjects/pythonProject1/venv/log.txt", "a")
dia = str(date.today())

try:
    html = urlopen("http://comprasnet.gov.br/ConsultaLicitacoes/ConsLicitacaoDia.asp")
    soup = BeautifulSoup(html, "html.parser")
    
    validaStatusLicitacoes = soup.find("", {"class":"mensagem"})
    if "Não existe licitação para o critério informado." in validaStatusLicitacoes:

        raise Exception(arquivo.write(dia+" Não existe licitação para o critério informado - Licitações indisponíveis"+ "\n"))
    
    
    paginas = str(soup.center.string)

    total = paginas[5:7]

    limpa = re.sub(r'\s+', '', paginas)
    limpa = re.sub(r'Licitações', '', limpa)
    limpa = re.sub(r'[()]', '', limpa)
    limpa = re.sub(r'[-|de]', ' ', limpa)

    paginas = limpa

    total = int(paginas[6:9])

    controla = 0

    numPagina = 0

    while controla <= total:

        numPagina += 1

        address = ('http://comprasnet.gov.br/ConsultaLicitacoes/ConsLicitacaoDia.asp?pagina=' + str(numPagina))
        controla += int(paginas[2:4])

        texto = urlopen(address).read().decode('iso-8859-1')

        # padrao = r'(<\w*>([^</tr><tr].+?)<\/.+?>(.{,60}))'
        # padrao = r'[^<.+?>]((?=Objeto:)(\w*))'
        # padrao = r'(<.+?>([^<.+?>].+?)<\/.+?>([^<.+?>].[^<.+?>]{,1000}))'
        # padrao = r'(<.+?>([^<.+?>].+?)<\/.+?>([^</table][^<.+?>].[^<.+?>]*))'
        # padrao = r'(<.+?>([^<.+?>].+?)<\/.+?>([^</table][^<.+?>].+?[^<.+?>]*))'
        padrao = r'(<.+?>([^<.+?>].+?)<\/.+?>([^<.+?>].*))'
        # padrao = r'(<.+?>([^<.+?>].+?)<\/.+?>(.[^<.+?>]*))'

        resultado = re.findall(padrao, str(texto))

        coduasg = ''
        numprp = ''
        modprp = ''

        for tags in resultado:
            um, dois, tres = tags

            findUasg = re.findall(r'Código da UASG:\s(\d+)', str(tres))
            findNumprp = re.findall(r'[Tomada de preço | Concorrência | Pregão Eletrônico | Concurso | RDC Eletrônico]\s\w.?\s(\d+)[^.](\d+)',str(tres))

            if (findUasg) and (findNumprp):

                if ('Tomada de preço' in tres):
                    modprp = str(2)

                if ('Concorrência' in tres):
                    modprp = str(3)

                if ('Pregão Eletrônico' in tres):
                    modprp = str(5)

                if ('Concurso' in tres):
                    modprp = str(20)

                if ('RDC Eletrônico' in tres):
                    modprp = str(99)

                for strNumprd in findNumprp:
                    umD, doisD = strNumprd
                    numprp = umD + doisD

                for strUasg in findUasg:
                    coduasg = strUasg

            link = ('http://comprasnet.gov.br/ConsultaLicitacoes/download/download_editais_detalhe.asp?coduasg=' + coduasg + '&modprp=' + modprp + '&numprp=' + numprp)

            tres = re.sub(r'&nbsp', ' ', tres)
            tres = re.sub(r'\s+', ' ', tres)
            tres = re.sub(r'<..>', ' ', tres)
            tres = re.sub(r'<b>', '\n', tres)
            tres = re.sub(r';Objeto:', '', tres)
            tres = re.sub(r';Objeto:', '', tres)
            tres = re.sub(r'  ;', ' ', tres)
            tres = re.sub(r'xx', '', tres)
            tres = re.sub(r'</td>', '', tres)
            tres = re.sub(r'<table style=.+>', '', tres)
            tres = re.sub(r'</table>', '', tres)
            tres = re.sub(r'Código da UASG:', '\nCódigo da UASG:', tres)
            tres = re.sub(r'[(|)]', '', tres)
            tres = re.sub(r'Telefone:\s+', 'Telefone: +55', tres)
            tres = re.sub(r'Fax:', '', tres)

            dois = re.sub(r'<iframe.+>', '', dois)
            dois = re.sub(r'Aguarde!', '', dois)
            dois = re.sub(r'</td>', '', dois)
            dois = re.sub(r'Histórico de eventos publicados...', '\n' + link, dois)

            cursor = con.cursor()

            compnRegistro = re.compile(r'(^\d+)', re.IGNORECASE)
            nRegistro = compnRegistro.findall(dois)

            compOrgao = re.compile(r'(.+\sCódigo da UASG:.\d+)', re.IGNORECASE)
            orgao = compOrgao.findall(tres)

            compTipo = re.compile(r'Código da UASG:.+\n(.+)Nº', re.IGNORECASE)
            tipo = compTipo.findall(tres)

            compnTipo = re.compile(r'Código da UASG:.+\n.+Nº\s(\d+' + '.\d+)', re.IGNORECASE)
            nTipo = compnTipo.findall(tres)

            compObjeto = re.compile(r'Objeto:\s+(.+)', re.IGNORECASE)
            objeto = compObjeto.findall(tres)

            compDataIni = re.compile(r'Edital a partir de:\s+(.+)', re.IGNORECASE)
            dataIni = compDataIni.findall(tres)

            compEndereco = re.compile(r'Endereço:\s+(.+)', re.IGNORECASE)
            endereco = compEndereco.findall(tres)

            compTelefone = re.compile(r'Telefone:(\s+.\d+.+)', re.IGNORECASE)
            telefone = compTelefone.findall(tres)

            compEntrega = re.compile(r'Entrega da Proposta:\s+(.+)', re.IGNORECASE)
            entrega = compEntrega.findall(tres)

            compUasg = re.compile(r'Código da UASG:\s+(.+)', re.IGNORECASE)
            uasg = compUasg.findall(tres)

            for inRegistro in nRegistro:
                for iOrgao in orgao:
                    for iTipo in tipo:
                        for inTipo in nTipo:
                            for iObjeto in objeto:
                                for iDataIni in dataIni:
                                    for inEndereco in endereco:
                                        for iTelefone in telefone:
                                            for iEntrega in entrega:
                                                for iUasg in uasg:
                                                    sql = "INSERT INTO COMPRASNET_TB (N_REGISTRO, LINK, ORGAO, TIPO_EDITAL, EDITAL, OBJETO, DATA_ABERTURA, ENDERECO, TELEFONE, ENTREGA,UASG) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"

                                                    cursor.execute(sql, (
                                                        inRegistro, link, iOrgao, iTipo, inTipo, iObjeto, iDataIni,
                                                        inEndereco,
                                                        iTelefone, iEntrega, iUasg))

        con.commit()

    arquivo.write(dia + ' - ' + inRegistro + ' Novos registros cadastrados\n')
except HTTPError as erro:
    writeErro = str(erro)
    arquivo.write(dia + ' ' + writeErro + '\n')
except URLError as erro:
    writeErro = str(erro)
    arquivo.write(dia + ' ' + writeErro + '\n')
