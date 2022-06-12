import pandas as pd
import xmltodict
from cnpj import puxarDados
from multiplosDados import qsa, atividade
from sqlalchemy import create_engine
import psycopg2







def insert(filemane):
    with open(f"C:\\Users\\gusta\\PycharmProjects\\teste\\uploads\\{filemane}") as archive:
        line=[]
        columns = ['ID','Forcenedor','CódigoProduto','Produto','Preço','Desconto','Preço total','CNPJ','Telefone','Ramo']
        content = archive.read()
        doc = xmltodict.parse(content)
        data = {
            'nf_id' : doc["nfeProc"]["NFe"]["infNFe"]["ide"]["nNF"],
            'fornecedor' : doc["nfeProc"]["NFe"]["infNFe"]["emit"]["xFant"],
            'cod_produto' : doc["nfeProc"]["NFe"]["infNFe"]['det']['prod']['cProd'],
            'produto' : doc["nfeProc"]["NFe"]["infNFe"]['det']['prod']['xProd'],
            'preco' : doc["nfeProc"]["NFe"]["infNFe"]['det']['prod']['vProd'],
            'desconto' : doc["nfeProc"]["NFe"]["infNFe"]['det']['prod']['vDesc'],
            'preco_total' : doc["nfeProc"]["NFe"]["infNFe"]['total']['ICMSTot']['vNF'],
            'cnpj' : doc["nfeProc"]["NFe"]["infNFe"]["emit"]["CNPJ"],
            'telefone' : doc["nfeProc"]["NFe"]["infNFe"]["emit"]["enderEmit"]['fone']
        }

    suplier_dict = puxarDados(data['cnpj'])
    suplier_people = qsa(suplier_dict)
    data['ramo'] = suplier_activity = atividade(suplier_dict)[0]

    df = pd.DataFrame([data])


    conectstring = 'postgresql://postgres:123456@localhost/xml'
    engine = create_engine(conectstring)
    conect = engine.connect()
    df.to_sql('data', con=conect, if_exists='replace', index=False)
    conect = psycopg2.connect(conectstring)
    conect.autocommit = True
    cursor = conect.cursor()