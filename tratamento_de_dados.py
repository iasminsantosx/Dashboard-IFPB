from fuzzywuzzy import fuzz
from fuzzywuzzy import process
from datetime import datetime, date

#CORRIGINDO BAIRROS
def get_closest_match(word, possibilities):
        if not word or not any(c.isalnum() for c in word):
            return word
        closest_match = process.extractOne(word, possibilities, scorer=fuzz.token_set_ratio)
        if closest_match[1] >= 80:
            return closest_match[0]
        else:
            return word
def correcao_bairros(df):
    base_correcao = {"sandra cavalcante": "bairro sandra cavalcante", 
                "presidente medici": "presidente medice",
                "zona rural": "area rural",
                "pedregal": "pedregal 58428-158",
                "jardim paulistano": "pardim paulistano",
                "rocha cavalcante": "rocha calvocante",
                "ramadinha ii": "ramadinha 2",
                "correa lima ii": "correia lima ii",
                "tres irmas": "tres irmas (acacio figueiredo)",
                "tres irmas": "tres irmas (portal sudoeste)",
                "portal sudoeste": "portal sudoesta",
                "portal sudoeste": "portal",
                "serrotao": "sao januario-serrotao",
                "bodocongo iii": "bodocongo 3",
                "centro": "boa vista/ centro",
                "malvinas": "malvinhas",
                "universitario": "universitatio",
                "palmeira": "palmeiras",
                "mutirao": "multirao"
                }
        
    if df['Bairro'].dtype == "object":
        df['Bairro'] = df['Bairro'].apply(lambda x: get_closest_match(x, base_correcao.keys()))
    
    return df

#RENOMENADO COLUNAS
def renomenado_colunas(df):
    df.rename(columns = {'Cor/Raca':'Cor_Raca'}, inplace = True)
    df.rename(columns = {'Situacao no ultimo periodo':'Situacao_no_ultimo_periodo'}, inplace = True)
    df.rename(columns = {'Ano de conclusao':'Ano_de_conclusao'}, inplace = True)
    df.rename(columns = {'IVS valido':'IVS_valido'}, inplace = True)
    df.rename(columns = {'Coeficiente de progressao':'Coeficiente_de_progressao'}, inplace = True)
    df.rename(columns = {'Cota SISTEC':'Cota_SISTEC'}, inplace = True)
    df.rename(columns = {'Data da matricula':'Data_da_matricula'}, inplace = True)
    df.rename(columns = {'Data de nascimento':'Data_de_nascimento'}, inplace = True)
    df.rename(columns = {'Faixa de renda (SISTEC)':'Faixa_de_renda_(SISTEC)'}, inplace = True)
    df.rename(columns = {'Forma de ingresso':'Forma_de_ingresso'}, inplace = True)
    df.rename(columns = {'Notas da selecao':'Notas_da_selecao'}, inplace = True)
    df.rename(columns = {'Tipo da escola anterior':'Tipo_da_escola_anterior'}, inplace = True)
    df.rename(columns = {'Tipo da zona residencial':'Tipo_da_zona_residencial'}, inplace = True)
    df.rename(columns = {'Ano de ingresso':'Ano_de_ingresso'}, inplace = True)

    return df



#AGRUPANDO FORMAS DE INGRESSO
def agrupando_formas_de_ingresso(df):
    df['Forma_de_ingresso'] = df['Forma_de_ingresso'].replace( ['sistema de selecao unificada (sisu)', 'sisu (inativa)', 'sisu - ampla concorrencia (inativa)', 'sisu - cota_eep/ppi (inativa)', 'sisu - cota_eep (inativa)',  'sisu - cota_eep/renda/ppi (inativa)','sisu - cota_eep/renda (inativa)','sisu - cota_pcd (inativa)'], 'sistema de selecao unificada (sisu)')
    df['Forma_de_ingresso'].unique()
    return df

#DATA DE NASCIMENTO EM IDADE
def idade(born):
    if born!= '-':
      born = datetime.strptime(born, "%d/%m/%Y").date()
      today = date.today()
      return int(today.year - born.year - ((today.month, 
                                        today.day) < (born.month, 
                                                      born.day)))

#FILTRANDO IVS
def filtrando_ivs(df):
    lista_ivs = df['IVS_valido'].to_list()
    sim = [
        '<span class="status status-success">sim</span>'
    ]

    nao = [
        '<span class="status status-error">nao</span>'
    ]
    for i in range(len(lista_ivs)):
        ivs = lista_ivs[i]
        if ivs in sim:
            lista_ivs[i] = 'sim'
        elif ivs in nao:
            lista_ivs[i] = 'nao'

    df['IVS_valido'] = lista_ivs
    return df

def geral(df):
    # colocando todos os valores em letras minúsculas
    df = df.applymap(lambda x: str(x).lower() if isinstance(x, str) else x)
    df.isnull().sum()
    
    renomenado_colunas(df)

    if 'Bairro' in df.columns :
        correcao_bairros(df)
        # criando uma cópia do dataframe original
        df_bairros = df.copy()

        # aplicando o filtro para identificar as linhas que possuem "-" ou erros específicos na coluna "Bairro"
        indexNames = df_bairros[(df_bairros['Bairro'] == '-') | (df_bairros['Bairro'] == '55') | (df_bairros['Bairro'] == 'a') | (df_bairros['Bairro'] == 's/n')].index

        # excluindo essas linhas do dataframe temporário
        df_bairros.drop(indexNames, inplace=True)


    agrupando_formas_de_ingresso(df)

    if 'Data_de_nascimento' in df.columns :
        lista_idades = df['Data_de_nascimento'].apply(idade)
        df.insert(13, "Idade", lista_idades, True)

    if 'IVS_valido' in df.columns :
        filtrando_ivs(df)

    return df