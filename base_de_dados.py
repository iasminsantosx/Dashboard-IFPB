import pandas as pd 

def dataframe(path_engenharia_de_computacao,path_telematica):
    df_engenharia = pd.read_excel(path_engenharia_de_computacao)
    df_telematica = pd.read_excel(path_telematica)

    df = pd.concat([df_engenharia,df_telematica], axis=0)

    return df 

def dataframenovo(path_engenharia_de_computacao,path_telematica):
    df_engenharia_novo = pd.read_excel(path_engenharia_de_computacao,sheet_name="NOVO")
    df_telematica_novo = pd.read_excel(path_telematica,sheet_name="NOVO")

    df_novo = pd.concat([df_engenharia_novo,df_telematica_novo], axis=0)

    return df_novo

def df_engenharia_telematica(path_engenharia_de_computacao,path_telematica):

    df_engenharia_novo = pd.read_excel(path_engenharia_de_computacao,sheet_name="NOVO")
    df_telematica_novo = pd.read_excel(path_telematica,sheet_name="NOVO")

    return df_engenharia_novo,df_telematica_novo