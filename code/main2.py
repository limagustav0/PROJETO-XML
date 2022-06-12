import xmltodict

with open("code/xml/NF.xml") as archive:
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










print(data)