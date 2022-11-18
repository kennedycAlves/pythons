import mysql.connector
from mysql.connector import errorcode

try:
    con = mysql.connector.connect(user='root', password='1q2w3e4r,', host='127.0.0.1', database='comprasnet')
    cursor = con.cursor()
    
    sql = "SELECT ar.nome_interesse, ar.cliente_id, ch.nome_chave FROM comprasnet.areainteresses as ar \
                    inner join clientes as c on c.id = ar.cliente_id \
                    inner join chavebuscas as ch on ch.areainteresse_id = ar.id"
    cursor.execute(sql)
    
    chaves = cursor.fetchall()
    
    for nome_interesse, cliente_id, nome_chave in chaves:
        str_nome_interesse = (''.join(nome_interesse))
        str_nome_chave = (''.join(nome_chave))
        

      
        #cursor.execute("select * from comprasnet_tb  where OBJETO LIKE('%%%s%%')" % str_nome_chave)
       
        #licitacoes = cursor.fetchall()
        #for licitacao in licitacoes:
        cursor.execute("INSERT INTO licitacoes(id, cliente_id, nome_interesse, creation_time, n_registro, uasg, orgao, tipo_edital,edital, objeto, data_abertura, entrega, estado, telefone, link, created_at, updated_at)\
                        SELECT 0,\
                        %s,\
                        '%s',\
                        CREATION_TIME,\
                        N_REGISTRO,\
                        UASG, ORGAO,\
                        TIPO_EDITAL,\
                        EDITAL,\
                        OBJETO,\
                        DATA_ABERTURA,\
                        ENTREGA,\
                        substring(ENDERECO,-3),\
                        TELEFONE,\
                        LINK,\
                        now(),\
                        now()\
                        from comprasnet_tb where OBJETO LIKE('%%%s%%') \
                        AND  CREATION_TIME  BETWEEN CURDATE() - INTERVAL 7 DAY AND SYSDATE()"%(cliente_id,str_nome_interesse,str_nome_chave))
      
    con.commit() 


except Exception as erro:
    print(erro)

