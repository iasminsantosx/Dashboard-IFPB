from dash import html, dcc
import plotly.express as px
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
import pandas as pd
from tratamento_de_dados import geral
from funcoes import descreve_informacoes
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
from datetime import datetime, date
import re
###########################Base de Dados###################################################
path_engenharia_de_computacao = '/home/iasmin/Documentos/TCC-Dashboard/dados_engenharia.xlsx'

df_engenharia = pd.read_excel(path_engenharia_de_computacao)
df_engenharia_novo = pd.read_excel(path_engenharia_de_computacao,sheet_name="NOVO")
#######################################TRATAMENTO DE DADOS################################
df_engenharia = df_engenharia.applymap(lambda x: str(x).lower() if isinstance(x, str) else x)

# função para encontrar a correspondência mais próxima
def get_closest_match(word, possibilities):
    if not word or not any(c.isalnum() for c in word):
        return word
    closest_match = process.extractOne(word, possibilities, scorer=fuzz.token_set_ratio)
    if closest_match[1] >= 80:
        return closest_match[0]
    else:
        return word
    
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

if df_engenharia['Bairro'].dtype == "object":
  df_engenharia['Bairro'] = df_engenharia['Bairro'].apply(lambda x: get_closest_match(x, base_correcao.keys()))

# criando uma cópia do dataframe original
df_bairros = df_engenharia.copy()

# aplicando o filtro para identificar as linhas que possuem "-" ou erros específicos na coluna "Bairro"
indexNames = df_bairros[(df_bairros['Bairro'] == '-') | (df_bairros['Bairro'] == '55') | (df_bairros['Bairro'] == 'a') | (df_bairros['Bairro'] == 's/n')].index

# excluindo essas linhas do dataframe temporário
df_bairros.drop(indexNames, inplace=True)

df_engenharia.rename(columns = {'Cor/Raca':'Cor_Raca'}, inplace = True)
df_engenharia.rename(columns = {'Situacao no ultimo periodo':'Situacao_no_ultimo_periodo'}, inplace = True)
df_engenharia.rename(columns = {'Ano de conclusao':'Ano_de_conclusao'}, inplace = True)
df_engenharia.rename(columns = {'IVS valido':'IVS_valido'}, inplace = True)
df_engenharia.rename(columns = {'Coeficiente de progressao':'Coeficiente_de_progressao'}, inplace = True)
df_engenharia.rename(columns = {'Cota SISTEC':'Cota_SISTEC'}, inplace = True)
df_engenharia.rename(columns = {'Data da matricula':'Data_da_matricula'}, inplace = True)
df_engenharia.rename(columns = {'Data de nascimento':'Data_de_nascimento'}, inplace = True)
df_engenharia.rename(columns = {'Faixa de renda (SISTEC)':'Faixa_de_renda_(SISTEC)'}, inplace = True)
df_engenharia.rename(columns = {'Forma de ingresso':'Forma_de_ingresso'}, inplace = True)
df_engenharia.rename(columns = {'Notas da selecao':'Notas_da_selecao'}, inplace = True)
df_engenharia.rename(columns = {'Tipo da escola anterior':'Tipo_da_escola_anterior'}, inplace = True)
df_engenharia.rename(columns = {'Tipo da zona residencial':'Tipo_da_zona_residencial'}, inplace = True)

df_engenharia['Forma_de_ingresso'] = df_engenharia['Forma_de_ingresso'].replace( ['sistema de selecao unificada (sisu)', 'sisu (inativa)', 'sisu - ampla concorrencia (inativa)', 'sisu - cota_eep/ppi (inativa)', 'sisu - cota_eep (inativa)',  'sisu - cota_eep/renda/ppi (inativa)','sisu - cota_eep/renda (inativa)','sisu - cota_pcd (inativa)'], 'sistema de selecao unificada (sisu)')
df_engenharia['Forma_de_ingresso'].unique()

def idade(born):
    if born!= '-':
      born = datetime.strptime(born, "%d/%m/%Y").date()
      today = date.today()
      return int(today.year - born.year - ((today.month, 
                                        today.day) < (born.month, 
                                                      born.day)))
    
lista_idades1 = df_engenharia['Data_de_nascimento'].apply(idade)
df_engenharia.insert(13, "Idade", lista_idades1, True)

df_conclusao_eng = df_engenharia_novo.copy()
df_conclusao_eng = df_conclusao_eng[df_engenharia_novo.Situacao.isin(['Formado'])]

df_conclusao_eng['Data da matricula'] = pd.to_datetime(df_conclusao_eng['Data da matricula'], format='%Y/%m/%d %H:%M:%S')
df_conclusao_eng['Data de conclusao'] = pd.to_datetime(df_conclusao_eng['Data de conclusao'], format='%Y/%m/%d %H:%M:%S')

df_conclusao_eng['Meses Conclusao'] = ((df_conclusao_eng['Data de conclusao'] - df_conclusao_eng['Data da matricula']).dt.days)/30
df_conclusao_eng.loc[:,'Meses Conclusao'] = df_conclusao_eng['Meses Conclusao'].astype(int)

df_agrupado_engenharia = df_engenharia.copy()
df_agrupado_engenharia['Situacao'] = df_agrupado_engenharia['Situacao'].replace( ['cancelado voluntariamente', 'cancelado compulsoriamente', 'trancado', 'evadido', 'afastado', 'trancado voluntariamente','transferido externamente', 'transferido internamente'], 'evadido/trancado')
df_agrupado_engenharia['Situacao'] = df_agrupado_engenharia['Situacao'].replace( ['matriculado',  'intercambio', 'vinculado'], 'matriculado')
df_agrupado_engenharia['Situacao'].unique()

df_engenharia_novo['Situacao'] = df_engenharia_novo['Situacao'].replace( ['Cancelado voluntariamente', 'Cancelado compulsoriamente', 'Trancado', 'Evadido', 'Afastado',  'Trancado voluntariamente','Transferido externamente', 'Transferido internamente'], 'evadido/trancado')
df_engenharia_novo['Situacao'] = df_engenharia_novo['Situacao'].replace( ['Matriculado',  'Intercambio', 'Vinculado'], 'matriculado')
df_engenharia_novo['Situacao'].unique()
##############################PLOTANDO GRAFICOS#############################################################

#Situação Geral
df_situacao_geral_eng = df_agrupado_engenharia['Situacao'].value_counts().to_frame()
colors = ['#6495ED','#FF6347','#9ACD32']

valor_absoluto1 = df_agrupado_engenharia['Situacao'].value_counts()

porcentagem1 = valor_absoluto1.apply((lambda x: (x*100)/valor_absoluto1.sum()))

fig1 = px.bar(df_situacao_geral_eng,x=df_situacao_geral_eng.index,y='count',title='Situação Geral',text=[str('{:,.2f}'.format(i)) +' %' for i in (porcentagem1)],color_discrete_sequence=[colors])
fig1.update_layout(yaxis={'title':'Quantidade de Alunos'},
                   xaxis={'title': 'Situacao'})

#AlunosxSexo
counts1 = df_agrupado_engenharia.groupby(['Sexo','Situacao']).size()
counts1 = counts1.unstack(level=-1)

totals1 = counts1.sum(axis=1)
percentages1 = counts1.divide(totals1, axis=0)*100

colors = ['#FF6347','#9ACD32','#6495ED']

fig2 = px.bar(percentages1,barmode = 'stack',color='Situacao', title='Situação dos alunos por Sexo',color_discrete_sequence=colors)
fig2.update_layout(yaxis={'title':'Porcentagem'},
                   xaxis={'title': 'Situacao'})

#Situaçãoxnaturalidade
df_sem_traco1 = df_agrupado_engenharia[df_agrupado_engenharia.Naturalidade!='-']
counts2 = df_sem_traco1.groupby(['Naturalidade','Situacao']).size()
counts2 = counts2.unstack(level=-1)

soma2 = counts2.sum(axis=1)
counts2.insert(3, "Total", soma2, True)
counts2=counts2.sort_values(by="Total", ascending=False)
counts2=counts2.drop(columns=['Total'])
counts2=counts2.head(10)

totals2 = counts2.sum(axis=1)
percentages2 = counts2.divide(totals2, axis=0)*100

colors = ['#FF6347','#9ACD32','#6495ED']

fig3 = px.bar(percentages2,barmode = 'stack',color='Situacao', title='Situação dos alunos por top 10 naturalidades',color_discrete_sequence=colors)
fig3.update_layout(yaxis={'title':'Porcentagem'},
                   xaxis={'title': 'Situacao'})

#SituaçãoxBairro
df_sem_traco2 = df_agrupado_engenharia[df_agrupado_engenharia.Bairro!='-']
counts3 = df_sem_traco2.groupby(['Bairro','Situacao']).size()
counts3 = counts3.unstack(level=-1)

soma3 = counts3.sum(axis=1)
counts3.insert(3, "Total", soma3, True)
counts3=counts3.sort_values(by="Total", ascending=False)
counts3=counts3.drop(columns=['Total'])
counts3=counts3.head(10)

totals3 = counts3.sum(axis=1)
percentages3 = counts3.divide(totals3, axis=0)*100

colors = ['#FF6347','#9ACD32','#6495ED']

fig4 = px.bar(percentages3,barmode = 'stack',color='Situacao', title='Situação dos alunos por top 10 bairros',color_discrete_sequence=colors)
fig4.update_layout(yaxis={'title':'Porcentagem'},
                   xaxis={'title': 'Situacao'})

#AlunosxTipoZona
df_sem_traco3 = df_agrupado_engenharia[df_agrupado_engenharia.Tipo_da_zona_residencial!='-']

counts4 = df_sem_traco3.groupby(['Tipo_da_zona_residencial','Situacao']).size()
counts4 = counts4.unstack(level=-1)

totals4 = counts4.sum(axis=1)
percentages4 = counts4.divide(totals4, axis=0)*100

colors = ['#FF6347','#9ACD32','#6495ED']

fig5 = px.bar(percentages4,barmode = 'stack',color='Situacao', title='Situação dos alunos por Tipo da zona residencial',color_discrete_sequence=colors)
fig5.update_layout(yaxis={'title':'Porcentagem'},
                   xaxis={'title': 'Situacao'})

#SituaçãoxFormaDeIngresso
counts5 = df_agrupado_engenharia.groupby(['Forma_de_ingresso','Situacao']).size()
counts5 = counts5.unstack(level=-1)

totals5 = counts5.sum(axis=1)
percentages5 = counts5.divide(totals5, axis=0)*100

colors = ['#FF6347','#9ACD32','#6495ED']

fig6 = px.bar(percentages5,barmode = 'stack',color='Situacao', title='Situação dos alunos por Forma de ingresso',color_discrete_sequence=colors)
fig6.update_layout(yaxis={'title':'Porcentagem'},
                   xaxis={'title': 'Forma de Ingresso'})

#SituaçãoxCor/Raca
counts6 = df_agrupado_engenharia.groupby(['Cor_Raca','Situacao']).size()
counts6 = counts6.unstack(level=-1)

totals6 = counts6.sum(axis=1)
percentages6 = counts6.divide(totals6, axis=0)*100

colors = ['#FF6347','#9ACD32','#6495ED']

fig7 = px.bar(percentages6,barmode = 'stack',color='Situacao', title='Situação dos alunos por Cor/Raça',color_discrete_sequence=colors)
fig7.update_layout(yaxis={'title':'Porcentagem'},
                   xaxis={'title': 'Cor/Raca'})

#SituaçãoxEscola
df_sem_traco3 = df_agrupado_engenharia[df_agrupado_engenharia.Tipo_da_escola_anterior!='-']
counts7 = df_sem_traco3.groupby(['Tipo_da_escola_anterior','Situacao']).size()
counts7 = counts7.unstack(level=-1)

totals7 = counts7.sum(axis=1)
percentages7 = counts7.divide(totals7, axis=0)*100

colors = ['#FF6347','#9ACD32','#6495ED']

fig20 = px.bar(percentages7,barmode = 'stack',color='Situacao', title='Situação dos alunos por Tipo da escola anterior',color_discrete_sequence=colors)
fig20.update_layout(yaxis={'title':'Porcentagem'},
                   xaxis={'title': 'Tipo da escola anterior'})

#FaixadeRenda
counts8 = df_agrupado_engenharia.groupby(['Faixa_de_renda_(SISTEC)','Situacao']).size()
counts8 = counts8.unstack(level=-1)

totals8 = counts8.sum(axis=1)
percentages8 = counts8.divide(totals8, axis=0)*100

colors = ['#FF6347','#9ACD32','#6495ED']

fig8 = px.bar(percentages8,barmode = 'stack',color='Situacao', title='Situação dos alunos por Faixa de renda (SISTEC)',color_discrete_sequence=colors)
fig8.update_layout(yaxis={'title':'Porcentagem'},
                   xaxis={'title': 'Faixa de renda (SISTEC)'})

#SituaçãoxIdade
df_idade_maior_30 = df_agrupado_engenharia[df_agrupado_engenharia.Idade>=30]
colors = ['#6495ED','#FF6347','#9ACD32']

fig9 = px.pie(values=df_idade_maior_30['Situacao'].value_counts(), names=df_idade_maior_30['Situacao'].value_counts().index,
             color_discrete_sequence=colors)

fig9.update_layout(margin = dict(t=50, l=100, r=100, b=0),title='Situação dos Alunos com idade maior que 30')

fig9.update_traces(textfont_size=16)

df_idade_menor_30 = df_agrupado_engenharia[df_agrupado_engenharia.Idade<=30]
colors = ['#6495ED','#FF6347','#9ACD32','black']

fig10 = px.pie(values=df_idade_menor_30['Situacao'].value_counts(), names=df_idade_menor_30['Situacao'].value_counts().index,
             color_discrete_sequence=colors)

fig10.update_layout(margin = dict(t=50, l=100, r=100, b=0),title='Situação dos Alunos com idade menor que 30')

fig10.update_traces(textfont_size=16)

#SituaçãoxCota
df_sem_traco4 = df_agrupado_engenharia[df_agrupado_engenharia.Cota_SISTEC!='-']
counts9 = df_sem_traco4.groupby(['Cota_SISTEC','Situacao']).size()
counts9 = counts9.unstack(level=-1)

totals9 = counts9.sum(axis=1)
percentages9 = counts9.divide(totals9, axis=0)*100

colors = ['#FF6347','#9ACD32','#6495ED']

fig11 = px.bar(percentages9,barmode = 'stack',color='Situacao', title='Situação dos alunos por Cota SISTEC',color_discrete_sequence=colors)
fig11.update_layout(yaxis={'title':'Porcentagem'},
                   xaxis={'title': 'Cota SISTEC'})

#Coeficiente de progressão

fig21 = go.Figure(data=[go.Table(
    header=dict(values=['Medidas', 'Coeficiente de Progressão'],
                line_color='#6495ED',
                fill_color='lightskyblue',
                align='center'),
    cells=dict(values=[['Quantidade', 'Média', 'Desvio padrão', 'Valor mínimo','Q1','Q2/Mediana','Q3','Valor máximo','Moda','Variância','Amplitude','Assimetria'], # 1st column
                       [655, 32.28, 32.83, 0.0,4.58,21.19,49.41,100.00,0.0,1077.84,100,0.25]], # 2nd column
               line_color='darkslategray',
               fill_color='lightcyan',
               align='center'))
])
#SituaçãoxNotasSeleção

df_evadidos = df_agrupado_engenharia[df_agrupado_engenharia.Situacao.isin(['evadido/trancado'])]
df_matriculado = df_agrupado_engenharia[df_agrupado_engenharia.Situacao.isin(['matriculado'])]
df_formado = df_agrupado_engenharia[df_agrupado_engenharia.Situacao.isin(['formado'])]

#Evadido
df_notas_evadidos = df_evadidos['Notas_da_selecao'].str.split('; ', expand=True)

df_notas_evadidos.columns = ['C.N.T.', 'C.H.T.', 'L.C.T.', 'M.T.', 'RED.']
df_notas_evadidos = df_notas_evadidos.dropna()


df_notas_evadidos = df_notas_evadidos.replace(r'[a-zA-Z\.= ]+', '', regex=True)
df_notas_evadidos = df_notas_evadidos.replace(r'(?<!\d)\.(?!\d)', '', regex=True)
df_notas_evadidos = df_notas_evadidos.replace(r'.*:', '', regex=True)
df_notas_evadidos = df_notas_evadidos.astype(float).fillna(0)

df_notas_evadidos = df_notas_evadidos / 100
df_notas_evadidos = df_notas_evadidos.mean()

#Matriculado
df_notas_matriculados = df_matriculado['Notas_da_selecao'].str.split('; ', expand=True)

df_notas_matriculados.columns = ['C.N.T.', 'C.H.T.', 'L.C.T.', 'M.T.', 'RED.']
df_notas_matriculados = df_notas_matriculados.dropna()


df_notas_matriculados = df_notas_matriculados.replace(r'[a-zA-Z\.= ]+', '', regex=True)
df_notas_matriculados = df_notas_matriculados.replace(r'(?<!\d)\.(?!\d)', '', regex=True)
df_notas_matriculados = df_notas_matriculados.replace(r'.*:', '', regex=True)
df_notas_matriculados = df_notas_matriculados.astype(float).fillna(0)

df_notas_matriculados = df_notas_matriculados / 100
df_notas_matriculados = df_notas_matriculados.mean()

#Formado
df_notas_formados = df_formado['Notas_da_selecao'].str.split('; ', expand=True)

df_notas_formados.columns = ['C.N.T.', 'C.H.T.', 'L.C.T.', 'M.T.', 'RED.']
df_notas_formados = df_notas_formados.dropna()


df_notas_formados = df_notas_formados.replace(r'[a-zA-Z\.= ]+', '', regex=True)
df_notas_formados = df_notas_formados.replace(r'(?<!\d)\.(?!\d)', '', regex=True)
df_notas_formados = df_notas_formados.replace(r'.*:', '', regex=True)
df_notas_formados = df_notas_formados.astype(float).fillna(0)

df_notas_formados = df_notas_formados /100
df_notas_formados = df_notas_formados.mean()

df_concat = pd.concat([df_notas_matriculados,df_notas_evadidos,df_notas_formados], axis=1)

df_concat.rename(columns = {0:'matriculado'}, inplace = True)
df_concat.rename(columns = {1:'evadido/trancado'}, inplace = True)
df_concat.rename(columns = {2:'formado'}, inplace = True)

colors = ['#6495ED','#FF6347','#9ACD32']
fig12 = px.bar(df_concat, title='Situação dos alunos por Notas de Seleção',color_discrete_sequence=colors,barmode="group")
fig12.update_layout(yaxis={'title':'Notas'},
                   xaxis={'title': 'Áreas'})


#Situação por semestres das alunas de engenharia
df_matricula_engenharia = df_engenharia_novo[(df_engenharia_novo.Sexo=='F')]
df_matricula_engenharia.loc[:,'Matricula'] = df_matricula_engenharia['Matricula'].astype(str)

colors = ['#9ACD32','#FF6347','#6495ED']

counts10 = df_matricula_engenharia.groupby(['Matricula', 'Situacao']).size()
counts10 = counts10.unstack(level=-1)

totals10 = counts10.sum(axis=1)
percentages10 = counts10.divide(totals10, axis=0)*100


fig13 = px.bar(percentages10,barmode = 'stack',color='Situacao', title='Situação das alunas por Semestre de Ingresso - Engenharia',color_discrete_sequence=colors)
fig13.update_layout(yaxis={'title':'Porcentagem'},
                   xaxis={'title': 'Semestre'})

#Alunas matriculadas por Semestre
df_matricula_engenharia1 = df_engenharia_novo[(df_engenharia_novo.Sexo=='F')]
df_matricula_engenharia1.loc[:,'Matricula'] = df_matricula_engenharia1['Matricula'].astype(str)
grafico_matricula_engenharia1 = df_matricula_engenharia1['Matricula'].value_counts().sort_index()

colors = ['#6495ED']

fig14 = px.bar(grafico_matricula_engenharia1,barmode = 'stack', title='Quantidade de Alunas matriculadas por Semestre de Ingresso - Engenharia',color_discrete_sequence=colors)
fig14.update_layout(yaxis={'title':'Quantidade de alunas matriculadas'},
                   xaxis={'title': 'Semestre'},showlegend=False)

#Situação por semestres dos alunos de engenharia
df_matricula_engenharia2 = df_engenharia_novo[(df_engenharia_novo.Sexo=='M')]
df_matricula_engenharia2.loc[:,'Matricula'] = df_matricula_engenharia2['Matricula'].astype(str)

colors = ['#9ACD32','#FF6347','#6495ED']

counts11 = df_matricula_engenharia2.groupby(['Matricula', 'Situacao']).size()
counts11 = counts11.unstack(level=-1)

totals11 = counts11.sum(axis=1)
percentages11 = counts11.divide(totals11, axis=0)*100


fig15 = px.bar(percentages11,barmode = 'stack',color='Situacao', title='Situação dos alunos por Semestre de Ingresso - Engenharia',color_discrete_sequence=colors)
fig15.update_layout(yaxis={'title':'Porcentagem'},
                   xaxis={'title': 'Semestre'})

#Situação por semestre
df_engenharia_novo.loc[:,'Matricula'] = df_engenharia_novo['Matricula'].astype(str)

counts12 = df_engenharia_novo.groupby(['Matricula', 'Situacao']).size()
counts12 = counts12.unstack(level=-1)

totals12 = counts12.sum(axis=1)
percentages12 = counts12.divide(totals12, axis=0)*100

colors = ['#9ACD32','#FF6347','#6495ED','black']
fig16 = px.bar(percentages12,barmode = 'stack',color='Situacao', title='Situação dos alunos de cada semestre em Engenharia de Computação',color_discrete_sequence=colors)
fig16.update_layout(yaxis={'title':'Porcentagem'},
                   xaxis={'title': 'Semestre'})

#Meses conclusão
colors = ['orange']
fig17 = px.histogram(df_conclusao_eng,x='Meses Conclusao',color_discrete_sequence=colors)

#Tempo Conclusão

concluintes_certo2 = df_conclusao_eng[df_conclusao_eng['Meses Conclusao'] > 60]['Meses Conclusao'].value_counts().sum()
percent = (concluintes_certo2 / len(df_conclusao_eng)) * 100

labels = ['Superior 60 meses ', 'Igual ou inferior a 60 meses']
sizes = [percent, 100-percent]
colors = ["royalblue","orange"]

fig18 = px.pie(values=sizes, names=['Superior 60 meses','Igual ou inferior a 60 meses'],color_discrete_sequence=colors)

fig18.update_layout(margin = dict(t=50, l=100, r=100, b=0),title='Tempo de Conclusão - Engenharia da Computação')

fig18.update_traces(textfont_size=16)

#Quantidade Alunos Engenharia
total_alunos_eng = len(df_engenharia['Situacao'])
fig19 = go.Figure()
fig19 = go.Figure(go.Indicator(
    mode = "number",
    value = total_alunos_eng,))
fig19.update_layout(
    template = {'data' : {'indicator': [{
        'title': {'text': "TOTAL DE ALUNOS DO CURSO DE ENGENHARIA DE COMPUTAÇÃO "},}]
                         }})
###################################LAYOUT###################################################################




layout = html.Div([
    dbc.Row([
        dbc.Col(
            dbc.Card(
                dbc.CardBody(
                    dcc.Graph(
                        figure=fig1
                    )),style={"width": "100%"},
            ),width=4),
        dbc.Col(
            dbc.Card(
                dbc.CardBody(
                    dcc.Graph(
                        figure=fig16)
                    ),style={"width": "100%"},
        ),width=4),
        dbc.Col(
            dbc.Card(
                dbc.CardBody(
                    dcc.Graph(
                        id='quantidade-total',
                        figure=fig19)
                    ),style={"width": "100%"},
        ),width=4),
    ],style={"width": "100%"}),

    dbc.Row([
        dbc.Col(
            dbc.Card(
                dbc.CardBody(
                    dcc.Graph(
                        figure=fig14
                    )),style={"width": "100%"},
            ),width=4),
        dbc.Col(
            dbc.Card(
                dbc.CardBody(
                    dcc.Graph(
                        figure=fig13)
                    ),style={"width": "100%"},
        ),width=4),
        dbc.Col(
            dbc.Card(
                dbc.CardBody(
                    dcc.Graph(
                        figure=fig15)
                    ),style={"width": "100%"},
        ),width=4),
    ],style={"width": "100%"}),

    dbc.Row([
        dbc.Col(
            dbc.Card(
                dbc.CardBody(
                    dcc.Graph(
                        figure=fig2
                    )),style={"width": "100%"},
            ),width=3),
        dbc.Col(
            dbc.Card(
                dbc.CardBody(
                    dcc.Graph(
                        figure=fig7)
                    ),style={"width": "100%"},
        ),width=3),
        dbc.Col(
            dbc.Card(
                dbc.CardBody(
                    dcc.Graph(
                        figure=fig8
                    )),style={"width": "100%"},
            ),width=3),
        dbc.Col(
            dbc.Card(
                dbc.CardBody(
                    dcc.Graph(
                        figure=fig5
                    )),style={"width": "100%"},
            ),width=3)
    ],style={"width": "100%"}),

    dbc.Row([
        dbc.Col(
            dbc.Card(
                dbc.CardBody(
                    dcc.Graph(
                        figure=fig3
                    )),style={"width": "100%"},
            ),width=6),
        dbc.Col(
            dbc.Card(
                dbc.CardBody(
                    dcc.Graph(
                        figure=fig4)
                    ),style={"width": "100%"},
        ),width=6),
    ],style={"width": "100%"}),

    dbc.Row([
        dbc.Col(
            dbc.Card(
                dbc.CardBody(
                    dcc.Graph(
                        figure=fig20
                    )),style={"width": "100%"},
            ),width=4),
        dbc.Col(
            dbc.Card(
                dbc.CardBody(
                    dcc.Graph(
                        figure=fig6)
                    ),style={"width": "100%"},
        ),width=4),
        dbc.Col(
            dbc.Card(
                dbc.CardBody(
                    dcc.Graph(
                        figure=fig12)
                    ),style={"width": "100%"},
        ),width=4),
    ],style={"width": "100%"}),

    dbc.Row([
        dbc.Col(
            dbc.Card(
                dbc.CardBody(
                    dcc.Graph(
                        figure=fig11
                    )),style={"width": "100%"},
            ),width=3),
        dbc.Col(
            dbc.Card(
                dbc.CardBody(
                    dcc.Graph(
                        figure=fig9)
                    ),style={"width": "100%"},
        ),width=3),
        dbc.Col(
            dbc.Card(
                dbc.CardBody(
                    dcc.Graph(
                        figure=fig10
                    )),style={"width": "100%"},
            ),width=3),
        dbc.Col(
            dbc.Card(
                dbc.CardBody(
                    dcc.Graph(
                        figure=fig21
                    )),style={"width": "100%"},
            ),width=3)
    ],style={"width": "100%"}),

    dbc.Row([
        dbc.Col(
            dbc.Card(
                dbc.CardBody(
                    dcc.Graph(
                        figure=fig17
                    )),style={"width": "100%"},
            ),width=6),
        dbc.Col(
            dbc.Card(
                dbc.CardBody(
                    dcc.Graph(
                        figure=fig18)
                    ),style={"width": "100%"},
        ),width=6),
    ],style={"width": "100%"}),
    
],style={"width": "100%"})


