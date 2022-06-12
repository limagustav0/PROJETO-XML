import requests



def trataCnpj(cnpj):
    sujeira = []
    cnpj = cnpj.replace("/","")
    cnpj = cnpj.replace("-","")
    cnpj = cnpj.replace(".","")

    [sujeira.append(i) for i in cnpj if not i.isnumeric()]
    if len(sujeira) == 0 and len(cnpj) == 14:
        return cnpj
    elif len(cnpj) > 14:
        print(f"O CNPJ contém letras a mais:  {cnpj}")
    else:
        print(f"Existem caracteres inválidos no CNPJ {sujeira}")

def puxarDados(cnpj):
    cnpjLimpo = trataCnpj(cnpj)
    if cnpjLimpo:
        r = requests.get(f"https://receitaws.com.br/v1/cnpj/{cnpjLimpo}")
        return r.json()
    else:
        return cnpjLimpo


