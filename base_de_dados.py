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

def matriculado_evadido(path_matriculado,path_evadido):

    df_matriculado = pd.read_excel(path_matriculado)
    df_evadido= pd.read_excel(path_evadido)
    
    df_eng_mat = df_matriculado.loc[df_matriculado['Qual curso você está matriculado?'] == 'Engenharia de Computação']
    df_tel_mat = df_matriculado.loc[df_matriculado['Qual curso você está matriculado?'] == 'Telemática']
    df_eng_evd = df_evadido.loc[df_evadido['Qual curso você fazia: '] == 'Engenharia de Computação']
    df_tel_evd = df_evadido.loc[df_evadido['Qual curso você fazia: '] == 'Telemática']

    return df_matriculado,df_evadido,df_eng_mat,df_tel_mat,df_eng_evd,df_tel_evd