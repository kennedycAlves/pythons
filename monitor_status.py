import re 
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup as BS
from urllib.request import urlopen
import mysql.connector
from mysql.connector import errorcode
from time import sleep

con = mysql.connector.connect(user='root', password='1q2w3e4r,', host='127.0.0.1', database='status_licitacao')


browser = webdriver.Firefox()  
type(browser)

tipo = "?Opc=2"
browser.get('http://comprasnet.gov.br/livre/Pregao/Lista_Pregao_Filtro.asp'+tipo)

codUasg = browser.find_element_by_id("co_uasg")
numprp = browser.find_element_by_id("numprp")
lstSituacao = browser.find_element_by_id("lstSituacao")
ok = browser.find_element_by_id("ok")

#Usasg
teste = '925373'

#N° Pregão
teste2 = '2802020'
lstSituacao.send_keys("Todas")
codUasg.send_keys(teste)
numprp.send_keys(teste2)
ok.click()

 


link = browser.find_element_by_partial_link_text('2802020')

link.click()





print('Informe os caracteres solicitados: ')
caracteres = input()

insericaracteres = browser.find_element_by_id('idLetra')
confirmar = browser.find_element_by_id('idSubmit')
insericaracteres.send_keys(caracteres)
confirmar.click()

tag = browser.find_element_by_tag_name('html').text

#print (tag)

compItem = re.compile(r'(\d+)\sServiço', re.IGNORECASE)
itens = compItem.findall(tag)

#print(item)


tag = re.sub(r'Tratamento Diferenciado Tipo.+', '', tag)

listaTag = tag.split('\n')
#print(listaTag)

orgao = ' '.join(listaTag[0:2])
#print(orgao)

pregao = ''.join(listaTag[4])
#print (pregao)

objeto = ''.join(listaTag[6])
#print(objeto)

modo  = ''.join(listaTag[7])
#print(modo)

data_realizacao  = ''.join(listaTag[8])
#print(data_realizacao)

data_abertura  = ''.join(listaTag[9])
#print(data_abertura)

cursor = con.cursor()
sql = "INSERT INTO pregao(orgao, pregao, objeto, modo, data_realizacao, data_abertura) VALUES(%s,%s,%s,%s,%s,%s)"
cursor.execute(sql, (orgao, pregao, objeto, modo, data_realizacao, data_abertura))
con.commit()  


#select_idpregao = ("SELECT id FROM pregao WHERE pregao like('%s')" % (pregao))
cursor.execute("SELECT id FROM pregao WHERE pregao like('%s')" % (pregao))

select_pregao_id = cursor.fetchone()

pregao_id = select_pregao_id[0]



#pregao_id = 0
#for id in select_pregao_id:
#
#    pregao_id = int(id[0])
#   
#print(pregao_id)   





lista_itens = (listaTag[15:-3])
browser.find_element_by_partial_link_text(itens[0]).click()
i = 0
inicio = 0


for linha in lista_itens:
    
    split_linha = linha.split()
    item = ''.join(split_linha[0])
    descricao = ' '.join(split_linha[1:5])
    tratamento_diferenciado = ''.join(split_linha[6])
    aplicabilidade = ''.join(split_linha[7])
    aplic_margem = ''.join(split_linha[8])
    
    if(len(split_linha) == 11):
        situacao = ''.join(split_linha[9])
        recurso = ''.join(split_linha[-1])
        #print(situacao + " " + recurso)
    else:
        situacao = ' '.join(split_linha[9:13])
        recurso = ''.join(split_linha[-1])
        #print(situacao + " " + recurso)
    
    sql2 = "INSERT INTO lista_itens(pregao_id, item, descricao, tratamento_diferenciado, aplicabilidade, aplic_margem, situacao, recurso  ) VALUES(%s,%s,%s,%s,%s,%s,%s,%s)"
    cursor.execute(sql2, (pregao_id, item, descricao, tratamento_diferenciado, aplicabilidade, aplic_margem, situacao, recurso))
    con.commit() 
    
    
    janelas = browser.window_handles
    browser.switch_to.window(janelas[1])
    
    urllista = browser.current_url
    
    if(inicio == 0):
        inicio = int(urllista[59:])
        #print(inicio)
        #inicio = int(inicio)
    else:
        inicio+=1
    
    getUrl = urllista[:59]
    
   
    
    while (i < int(item)):
       
       
        print('tratando:',getUrl+str(inicio))
        #print(i)
      
        browser.get(getUrl+str(inicio))
        i+=1
        sleep(3)
        propostas = browser.find_element_by_tag_name('html').text  
        texto_split = propostas.split('\n')
        #print(texto_split)


        for ind,linha in enumerate(texto_split):
            #print(ind,linha.strip())
            if('Descrição Detalhada' in linha.strip()):

            #   print('primeiro IF')
                cnpj_cpf = str(texto_split[ind - 1]).split()[0]
                fornecedor = ' '.join((texto_split[ind - 1]).split()[1:-2])
                qtde_ofertada = str(texto_split[ind - 1]).split()[-2]
                valor_total = str(texto_split[ind - 1]).split()[-1]
                descricao_detalhada = ' '.join(texto_split[ind].split()[5:-1])
                porte_ME_EPP = str(texto_split[ind + 1]).split()[2]
                declaracao_ME_EPP_COOP = str(texto_split[ind + 1]).split()[-1]
                declaracao7174 = str(texto_split[ind + 2]).split()[-1]
                #print(Declaracao7174)
                
                cursor.execute("SELECT id FROM lista_itens WHERE pregao_id = %s AND item = %s " % (pregao_id, item))
                select_lista_itens_id = cursor.fetchone()
                lista_itens_id = select_lista_itens_id[0]



                sql3 = "INSERT INTO propostas(lista_itens_id,cnpj_cpf_fornecedor,fornecedor,qtde,valor_total,descricao_detalhada,porte_ME_EPP,declaracao_ME_EPP_COOP,declaração7174) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                cursor.execute(sql3, (lista_itens_id,str(cnpj_cpf),str(fornecedor),str(qtde_ofertada),str(valor_total),str(descricao_detalhada),str(porte_ME_EPP),str(declaracao_ME_EPP_COOP),str(declaracao7174))) 
                                             #print(lista_itens_id,cnpj_cpf_fornecedor,fornecedor,qtde,valor_total,descricao_detalhada,porte_ME_EPP,declaracao_ME_EPP_COOP,declaração7174)
            con.commit()
       