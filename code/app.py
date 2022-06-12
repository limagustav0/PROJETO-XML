from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import os
from datetime import datetime
import pandas as pd
import xmltodict
from cnpj import puxarDados
from multiplosDados import qsa, atividade
import psycopg2
import psycopg2.extras

app = Flask(__name__)

diretorio = "C:\\Users\\gusta\\PycharmProjects\\teste\\uploads"
ALLOWED_EXTENSIONS = ['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif','xml']

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def main():
    return render_template('index.html')

@app.route("/upload", methods=["POST", "GET"])
def upload():
    if request.method == 'POST':
        file = request.files['file']
        filename = secure_filename(file.filename)
        file.save(os.path.join(diretorio, filename))
        insert(filename)
        return "",200

def insert(filename):
    with open(f"{diretorio}\\{filename}") as archive:

        content = archive.read()
        doc = xmltodict.parse(content)
        data = {
            'nf_id': doc["nfeProc"]["NFe"]["infNFe"]["ide"]["nNF"],
            'fornecedor': doc["nfeProc"]["NFe"]["infNFe"]["emit"]["xFant"],
            'cod_produto': doc["nfeProc"]["NFe"]["infNFe"]['det']['prod']['cProd'],
            'produto': doc["nfeProc"]["NFe"]["infNFe"]['det']['prod']['xProd'],
            'preco': doc["nfeProc"]["NFe"]["infNFe"]['det']['prod']['vProd'],
            'desconto': doc["nfeProc"]["NFe"]["infNFe"]['det']['prod']['vDesc'],
            'preco_total': doc["nfeProc"]["NFe"]["infNFe"]['total']['ICMSTot']['vNF'],
            'cnpj': doc["nfeProc"]["NFe"]["infNFe"]["emit"]["CNPJ"],
            'telefone': doc["nfeProc"]["NFe"]["infNFe"]["emit"]["enderEmit"]['fone']
        }
        suplier_dict = puxarDados(data['cnpj'])
        suplier_people = qsa(suplier_dict)
        data['ramo'] = suplier_activity = atividade(suplier_dict)[0]
        data['now'] = datetime.now()

        df = pd.DataFrame([data])

        def conecta_db():
            con = psycopg2.connect(host='localhost',
                                   database='xml',
                                   user='postgres',
                                   password='123456')
            return con

        def criar_db(sql):
            con = conecta_db()
            cur = con.cursor()
            cur.execute(sql)
            con.commit()
            con.close()

        def inserir_db(sql):
            con = conecta_db()
            cur = con.cursor()
            try:
                cur.execute(sql)
                con.commit()
            except (Exception, psycopg2.DatabaseError) as error:
                print("Error: %s" % error)
                con.rollback()
                cur.close()
                return 1
            cur.close()

        sql = 'DROP TABLE IF EXISTS public.xml'
        criar_db(sql)
        # Criando a tabela dos deputados
        sql = '''CREATE TABLE  if not exists public.xml_data(
                    nf_id character varying(10) NOT NULL,
                    fornecedor character varying(40),
                    cod_produto character varying(15),
                    produto character varying(200),
                    preco double precision,
                    desconto double precision,
                    preco_total double precision,
                    cnpj character varying(14),
                    telefone character varying(15),
                    ramo character varying(150),
                    now character varying,
                    PRIMARY KEY (nf_id)
                    );

                    ALTER TABLE IF EXISTS public.xml_data
                        OWNER to postgres;'''
        criar_db(sql)

        for i in df.index:
            sql = """
            INSERT into public.xml_data (nf_id,fornecedor,cod_produto,produto,preco,desconto,preco_total,cnpj,telefone,ramo,now) 
            values('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s');
            """ % (
            df['nf_id'][i], df['fornecedor'][i], df['cod_produto'][i], df['produto'][i], df['preco'][i], df['desconto'][i],
            df['preco_total'][i], df['cnpj'][i], df['telefone'][i],df['ramo'][i],df['now'][i])
            inserir_db(sql)

        #cur.execute("INSERT INTO data (data[nf_id],data[fornecedor],data[cod_produto],data[produto],data[preco],data[desconto],data[preco_total],data[cnpj],data[telefone],data[ramo],data[now]) "
                    #"VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", [filename])






if __name__ == "__main__":
    app.run(debug=True)

