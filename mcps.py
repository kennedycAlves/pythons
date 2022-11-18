import re
from urllib.request import urlopen
from urllib.error import HTTPError, URLError
from bs4 import BeautifulSoup
import mysql.connector
from mysql.connector import errorcode
from datetime import date
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


con = mysql.connector.connect(user='root', password='1q2w3e4r,', host='127.0.0.1', database='comprasnet')
'''
except mysql.connector.Error as erro:
    if erro.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Usuário ou senha inválidos")
    elif erro.errno == errorcode.ER_BAD_DB_ERROR:
        print("Banco de dados não encontrado")
    else:
        print(erro)
'''
arquivo = open("C:/PycharmProjects/pythonProject1/venv/log.txt", "a")
dia = str(date.today())

try:
    html = urlopen("http://comprasnet.gov.br/ConsultaLicitacoes/ConsLicitacaoDia.asp")
    soup = BeautifulSoup(html, "html.parser")
    
    validaStatusLicitacoes = soup.find("", {"class":"mensagem"})
    print(validaStatusLicitacoes)
    if validaStatusLicitacoes == "Não existe licitação para o critério informado.":

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



    while total > controla:

        numPagina += 1

        address = ('http://comprasnet.gov.br/ConsultaLicitacoes/ConsLicitacaoDia.asp?pagina=' + str(numPagina))
        controla += int(paginas[2:4])

        texto = urlopen(address).read().decode('iso-8859-1')
        print(controla)
        print(total)
        print(numPagina)

        # padrao = r'(<\w*>([^</tr><tr].+?)<\/.+?>(.{,60}))'
        # padrao = r'[^<.+?>]((?=Objeto:)(\w*))'
        # padrao = r'(<.+?>([^<.+?>].+?)<\/.+?>([^<.+?>].[^<.+?>]{,1000}))'
        # padrao = r'(<.+?>([^<.+?>].+?)<\/.+?>([^</table][^<.+?>].[^<.+?>]*))'
        # padrao = r'(<.+?>([^<.+?>].+?)<\/.+?>([^</table][^<.+?>].+?[^<.+?>]*))'
        padrao = r'(<.+?>([^<.+?>].+?)<\/.+?>([^<.+?>].*))'
        # padrao = r'(<.+?>([^<.+?>].+?)<\/.+?>(.[^<.+?>]*))'

        resultado = re.findall(padrao, str(texto))

       
        
        
        
        #def validaEntrega(coduasg, numprp):

          
                                          
        browser = webdriver.Firefox()  
        tipo = "?Opc=0"
        browser.get('http://comprasnet.gov.br/livre/Pregao/lista_pregao_filtro.asp'+tipo)
                    

        for tags in resultado:

                         
            um, dois, tres = tags

            

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
            #dois = re.sub(r'Histórico de eventos publicados...', '\n' + link, dois)

            cursor = con.cursor()

                          

            compnRegistro = re.compile(r'(^\d+)', re.IGNORECASE)
            nRegistro = compnRegistro.findall(dois)

            compOrgao = re.compile(r'(.+\sCódigo da UASG:.\d+)', re.IGNORECASE)
            orgao = compOrgao.findall(tres)

            compTipo = re.compile(r'Código da UASG:.+\n(.+)Nº', re.IGNORECASE)
            tipo = compTipo.findall(tres)
            tipoEdital = str(tipo)


            compnTipo = re.compile(r'Código da UASG:.+\n.+Nº\s(\d+' + '.\d+)', re.IGNORECASE)
            nTipo = compnTipo.findall(tres)
            
            numeroPregao = str(nTipo)
            numeroPregao = str(re.sub(r'[\/|\[\'|\'\]]','', numeroPregao))
            #print(numeroPregao)
            
            compObjeto = re.compile(r'Objeto:\s+(.+)', re.IGNORECASE)
            objeto = compObjeto.findall(tres)
            

            compDataIni = re.compile(r'Edital a partir de:\s+(.+)', re.IGNORECASE)
            dataIni = compDataIni.findall(tres)

            compEndereco = re.compile(r'Endereço:\s+(.+)', re.IGNORECASE)
            endereco = compEndereco.findall(tres)

            compTelefone = re.compile(r'Telefone:(\s+.\d+.\d+)', re.IGNORECASE)
            telefone = compTelefone.findall(tres)
            

            compEntrega = re.compile(r'Entrega da Proposta:\s+(.+)', re.IGNORECASE)
            entrega = compEntrega.findall(tres)

            compUasg = re.compile(r'Código da UASG:\s+(.+)', re.IGNORECASE)
            uasg = compUasg.findall(tres)

            coduasg = str(uasg)
            coduasg = re.sub(r'[\[\'|\s+|\'\]]', '', coduasg)

            
            numprp = numeroPregao
            modprp = ''

            if ('Tomada de preço' in tipoEdital):
                    modprp = str(2)

            if ('Concorrência' in tipoEdital):
                    modprp = str(3)

            if ('Pregão Eletrônico' in tipoEdital):
                    modprp = str(5)

            if ('Concurso' in tipoEdital):
                    modprp = str(20)

            if ('RDC Eletrônico' in tipoEdital):
                    modprp = str(99)

            
            link = ('http://comprasnet.gov.br/ConsultaLicitacoes/download/download_editais_detalhe.asp?coduasg=' + coduasg + '&modprp=' + modprp + '&numprp=' + numprp)


                      
            trataCoduasg = coduasg
            trataNumprp = numprp

            listaTrataCoduasg  = []
           
            listaTrataNumprp = []


            listaTrataCoduasg.append(trataCoduasg)
            listaTrataNumprp.append(trataNumprp)

            
            
            
            for i in listaTrataCoduasg:
                if i != "":
                    for x in listaTrataNumprp:
                        if x != "":
                            
                            
                            
                            
                            
                            codUasg = browser.find_element_by_id("co_uasg")
                            numprp = browser.find_element_by_id("numprp")
                            lstSituacao = browser.find_element_by_id("lstSituacao")
                            ok = browser.find_element_by_id("ok")

                            
                            lstSituacao.send_keys("Todas")
                            codUasg.send_keys(i)
                            numprp.send_keys(x)
                            ok.click()
                            

                            
                            tag = browser.find_element_by_tag_name('html').text


                            listaTag = tag.split(' ')
                            data = listaTag[-2]
                            hora = listaTag[-1]

                            validaEntrega = data + ' ' + hora
                            compEntrega = re.compile(r'\d{2}\/\d{2}\/\d{4}\s\d{2}\:\d{2}')
                            
                            if (compEntrega.search(validaEntrega)):
                                entregaFinal = validaEntrega
                            else:
                                entregaFinal = ''.join(entrega)


                            browser.back()
                            browser.refresh()
                            
                         
                    


            for inRegistro in nRegistro:
                for iOrgao in orgao:
                    for iTipo in tipo:
                        for inTipo in nTipo:
                            for iObjeto in objeto:
                                for iDataIni in dataIni:
                                    for inEndereco in endereco:
                                        for iTelefone in telefone:
                                            for iUasg in uasg:
                                                sql = "INSERT INTO COMPRASNET_TB (N_REGISTRO, LINK, ORGAO, TIPO_EDITAL, EDITAL, OBJETO, DATA_ABERTURA, ENDERECO, TELEFONE, ENTREGA,UASG) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"

                                                cursor.execute(sql, (
                                                        inRegistro, link, iOrgao, iTipo, inTipo, iObjeto, iDataIni,
                                                        inEndereco,
                                                        iTelefone, entregaFinal, iUasg))

        con.commit()
        browser.quit()  
           
    arquivo.write(dia + ' - ' + inRegistro + ' Novos registros cadastrados\n')

    arquivo.write(dia + ' - ' + inRegistro + ' Novos registros cadastrados\n')
except HTTPError as erro:
    writeErro = str(erro)
    arquivo.write(dia + ' ' + writeErro + '\n')
except URLError as erro:
    writeErro = str(erro)
    arquivo.write(dia + ' ' + writeErro + '\n')
