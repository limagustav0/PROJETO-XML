import pandas as pd


def qsa(dict):
    responsaveis = [i['nome'] for i in dict['qsa']]
    cargos = [i['qual'] for i in dict['qsa']]
    df_responsaveisCargos = pd.DataFrame(list(zip(responsaveis,cargos)),columns=['Nome','Cargo'])
    return df_responsaveisCargos

def atividade(dict):
    textoPrincipal = [i['text'] for i in dict['atividade_principal']]
    return textoPrincipal






