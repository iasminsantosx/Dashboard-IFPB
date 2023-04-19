from dash import Dash, html, dcc
import pandas as pd
import numpy as np
import pendulum as pdl
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
import plotly.express as px
import plotly.graph_objects as go
from dash_bootstrap_templates import ThemeSwitchAIO
import dash_bootstrap_components as dbc

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

###########################Base de Dados###################################################
path_engenharia_de_computacao = '/home/iasmin/Documentos/TCC-Dashboard/dados_engenharia.xlsx'
df_engenharia = pd.read_excel(path_engenharia_de_computacao)

path_telematica = '/home/iasmin/Documentos/TCC-Dashboard/dados_telematica.xlsx'
df_telematica = pd.read_excel(path_telematica)

df_engenharia_novo = pd.read_excel(path_engenharia_de_computacao,sheet_name="NOVO")
df_telematica_novo = pd.read_excel(path_telematica,sheet_name="NOVO")

df = pd.concat([df_engenharia,df_telematica], axis=0)
df_novo = pd.concat([df_engenharia_novo,df_telematica_novo], axis=0)

#######################################TRATAMENTO DE DADOS################################
df = df.applymap(lambda x: str(x).lower() if isinstance(x, str) else x)
df.isnull().sum()
#CORRIGINDO BAIRROS
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

def get_closest_match(word, possibilities):
    if not word or not any(c.isalnum() for c in word):
        return word
    closest_match = process.extractOne(word, possibilities, scorer=fuzz.token_set_ratio)
    if closest_match[1] >= 80:
        return closest_match[0]
    else:
        return word
    
if df['Bairro'].dtype == "object":
  df['Bairro'] = df['Bairro'].apply(lambda x: get_closest_match(x, base_correcao.keys()))

# criando uma cópia do dataframe original
df_bairros = df.copy()

# aplicando o filtro para identificar as linhas que possuem "-" ou erros específicos na coluna "Bairro"
indexNames = df_bairros[(df_bairros['Bairro'] == '-') | (df_bairros['Bairro'] == '55') | (df_bairros['Bairro'] == 'a') | (df_bairros['Bairro'] == 's/n')].index

# excluindo essas linhas do dataframe temporário
df_bairros.drop(indexNames, inplace=True)

#RENOMENADO COLUNAS
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

df_novo.rename(columns = {'Ano de ingresso':'Ano_de_ingresso'}, inplace = True)
df_novo.rename(columns = {'Situacao no ultimo periodo':'Situacao_no_ultimo_periodo'}, inplace = True)
df_novo.rename(columns = {'Ano de conclusao':'Ano_de_conclusao'}, inplace = True)
df_novo.rename(columns = {'Diarios matriculados no ultimo periodo':'Diarios_matriculados_no_ultimo_periodo'}, inplace = True)
df_novo.rename(columns = {'Data da matricula':'Data_da_matricula'}, inplace = True)
df_novo.rename(columns = {'Data de conclusao':'Data_de_conclusao'}, inplace = True)
df_novo.rename(columns = {'Forma de ingresso':'Forma_de_ingresso'}, inplace = True)
df_novo.rename(columns = {'Tipo da escola anterior':'Tipo_da_escola_anterior'}, inplace = True)
df_novo.rename(columns = {'Tipo da zona residencial':'Tipo_da_zona_residencial'}, inplace = True)

#AGRUPANDO FORMAS DE INGRESSO
df['Forma_de_ingresso'] = df['Forma_de_ingresso'].replace( ['sistema de selecao unificada (sisu)', 'sisu (inativa)', 'sisu - ampla concorrencia (inativa)', 'sisu - cota_eep/ppi (inativa)', 'sisu - cota_eep (inativa)',  'sisu - cota_eep/renda/ppi (inativa)','sisu - cota_eep/renda (inativa)','sisu - cota_pcd (inativa)'], 'sistema de selecao unificada (sisu)')
df['Forma_de_ingresso'].unique()

#DATA DE NASCIMENTO EM IDADE
def idade(born):
    if born!= '-':
      born = datetime.strptime(born, "%d/%m/%Y").date()
      today = date.today()
      return int(today.year - born.year - ((today.month, 
                                        today.day) < (born.month, 
                                                      born.day)))
    
lista_idades = df['Data_de_nascimento'].apply(idade)
df.insert(13, "Idade", lista_idades, True)

#FILTRANDO IVS
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

##############################PLOTANDO GRAFICOS#############################################################

#Situação Geral
df_situacao_geral = df['Situacao'].value_counts().to_frame()

valor_absoluto = df['Situacao'].value_counts()
porcentagem = valor_absoluto.apply((lambda x: (x*100)/df['Situacao'].value_counts().sum()))

colors = ['#9ACD32','#FF6347','#FF6347','#6495ED','#FF6347','#FF6347','#FF6347','#9ACD32','#9ACD32','#FF6347','#FF6347','#FF6347','black']

fig1 = px.bar(df_situacao_geral,x=df_situacao_geral.index,y='count', title='Alunos por Situações nos cursos de TIC',text=[str('{:,.2f}'.format(i)) +' %' for i in (porcentagem)],color_discrete_sequence=[colors])
fig1.update_layout(yaxis={'title':'Quantidade de Alunos'},
                   xaxis={'title': 'Situação'})

#Total de Alunos
total_alunos = df_situacao_geral['count'].sum()
fig2 = go.Figure()
fig2 = go.Figure(go.Indicator(
    mode = "number",
    value = total_alunos,))
fig2.update_layout(
    template = {'data' : {'indicator': [{
        'title': {'text': "TOTAL DE ALUNOS DOS CURSOS DE TIC - IFPB"},}]
                         }})

#Situação Engenharia de Computação
df_engenharia_novo['Situacao'] = df_engenharia_novo['Situacao'].replace( ['Cancelado voluntariamente', 'Cancelado compulsoriamente', 'Trancado', 'Evadido', 'Afastado',  'Trancado voluntariamente','Transferido externamente', 'Transferido internamente'], 'evadido/trancado')
df_engenharia_novo['Situacao'] = df_engenharia_novo['Situacao'].replace( ['Matriculado',  'Intercambio', 'Vinculado'], 'matriculado')
df_engenharia_novo['Situacao'].unique()

df_engenharia_novo['Matricula'] = df_engenharia_novo['Matricula'].astype(str)

counts = df_engenharia_novo.groupby(['Matricula', 'Situacao']).size()
counts = counts.unstack(level=-1)

totals = counts.sum(axis=1)
percentages = counts.divide(totals, axis=0)*100

colors = ['#9ACD32','#FF6347','#6495ED','black']
fig3 = px.bar(percentages,barmode = 'stack',color='Situacao', title='Situação dos alunos de cada semestre em Engenharia de Computação',color_discrete_sequence=colors)
fig3.update_layout(yaxis={'title':'Porcentagem'},
                   xaxis={'title': 'Semestre'})

#Situação Telemática
df_telematica_novo['Situacao'] = df_telematica_novo['Situacao'].replace( ['Cancelado voluntariamente', 'Cancelado compulsoriamente', 'Trancado', 'Evadido', 'Afastado',  'Trancado voluntariamente','Transferido externamente', 'Transferido internamente'], 'evadido/trancado')
df_telematica_novo['Situacao'] = df_telematica_novo['Situacao'].replace( ['Matriculado',  'Intercambio', 'Vinculado'], 'matriculado')
df_telematica_novo['Situacao'].unique()

df_telematica_novo['Matricula'] = df_telematica_novo['Matricula'].astype(str)

counts = df_telematica_novo.groupby(['Matricula', 'Situacao']).size()
counts = counts.unstack(level=-1)

totals = counts.sum(axis=1)
percentages = counts.divide(totals, axis=0)*100

colors = ['black','#9ACD32','#FF6347','#6495ED']
fig4 = px.bar(percentages,barmode = 'stack',color='Situacao', title='Situação dos alunos de cada semestre em Telemática',color_discrete_sequence=colors)
fig4.update_layout(yaxis={'title':'Porcentagem'},
                   xaxis={'title': 'Semestre'})

#Quantidade alunos engenharia
total_alunos_eng = len(df_engenharia_novo['Matricula'])
fig5 = go.Figure()
fig5 = go.Figure(go.Indicator(
    mode = "number",
    value = total_alunos_eng,))
fig5.update_layout(
    template = {'data' : {'indicator': [{
        'title': {'text': "TOTAL DE ALUNOS DE ENGENHARIA DE COMPUTAÇÃO"},}]
                         }})

#Quantidade alunos telematica
total_alunos_tel = len(df_telematica_novo['Matricula'])
fig6 = go.Figure()
fig6 = go.Figure(go.Indicator(
    mode = "number",
    value = total_alunos_tel,))
fig6.update_layout(
    template = {'data' : {'indicator': [{
        'title': {'text': "TOTAL DE ALUNOS DE TELEMÁTICA"},}]
                         }},height = 200)

#Tempo de Conclusão eng
df_conclusao_eng = df_engenharia_novo.copy()
df_conclusao_eng = df_conclusao_eng[df_engenharia_novo.Situacao.isin(['Formado'])]

df_conclusao_eng['Data da matricula'] = pd.to_datetime(df_conclusao_eng['Data da matricula'], format='%Y/%m/%d %H:%M:%S')
df_conclusao_eng['Data de conclusao'] = pd.to_datetime(df_conclusao_eng['Data de conclusao'], format='%Y/%m/%d %H:%M:%S')

df_conclusao_eng['Meses Conclusao'] = ((df_conclusao_eng['Data de conclusao'] - df_conclusao_eng['Data da matricula']).dt.days)/30
df_conclusao_eng['Meses Conclusao'] = df_conclusao_eng['Meses Conclusao'].astype(int)

concluintes_certo2 = df_conclusao_eng[df_conclusao_eng['Meses Conclusao'] > 60]['Meses Conclusao'].value_counts().sum()
percent = (concluintes_certo2 / len(df_conclusao_eng)) * 100

labels = ['Superior 60 meses ', 'Igual ou inferior a 60 meses']
sizes = [percent, 100-percent]
colors = ["royalblue","orange"]

fig7 = px.pie(values=sizes, names=['Superior 60 meses','Igual ou inferior a 60 meses'],color_discrete_sequence=colors)

fig7.update_layout(margin = dict(t=50, l=100, r=100, b=0),title='Tempo de Conclusão - Engenharia da Computação')

fig7.update_traces(textfont_size=16)

#Tempo de Conclusão Tel
df_conclusao_tel = df_telematica_novo.copy()

indexNames = df_conclusao_tel[(df_conclusao_tel['Data de conclusao'] == '-')].index

df_conclusao_tel.drop(indexNames, inplace=True)

df_conclusao_tel['Data da matricula'] = pd.to_datetime(df_conclusao_tel['Data da matricula'], format='%Y/%m/%d %H:%M:%S')
df_conclusao_tel['Data de conclusao'] = pd.to_datetime(df_conclusao_tel['Data de conclusao'], format='%Y/%m/%d %H:%M:%S')
df_conclusao_tel['Meses Conclusao'] = ((df_conclusao_tel['Data de conclusao'] - df_conclusao_tel['Data da matricula']).dt.days)/30
df_conclusao_tel['Meses Conclusao']=df_conclusao_tel['Meses Conclusao'].astype(int)

concluintes_certo = df_conclusao_tel[df_conclusao_tel['Meses Conclusao'] > 36]['Meses Conclusao'].value_counts().sum()
percent = (concluintes_certo / len(df_conclusao_tel)) * 100

labels = ['Superior 36 meses ', 'Igual ou inferior a 36 meses']
sizes = [percent, 100-percent]
colors = ["royalblue","orange"]

fig8 = px.pie(values=sizes, names=['Superior 36 meses','Igual ou inferior a 36 meses'],color_discrete_sequence=colors)

fig8.update_layout(margin = dict(t=50, l=100, r=100, b=0),title='Tempo de Conclusão - Telemática')

fig8.update_traces(textfont_size=16)
###################################LAYOUT###################################################################


app.layout = html.Div([
    dbc.Row(
    dbc.NavbarSimple(
        children=[
            dbc.NavItem(dbc.NavLink("Page 1", href="#")),
            dbc.DropdownMenu(
                children=[
                    dbc.DropdownMenuItem("More pages", header=True),
                    dbc.DropdownMenuItem("Page 2", href="#"),
                    dbc.DropdownMenuItem("Page 3", href="#"),
                ],
                nav=True,
                in_navbar=True,
                label="More",
            ),
        ],
    brand="Dados Gerais",
    brand_href="#",
    color="primary",
    dark=True,
)),

    dbc.Row([
        dbc.Col(
            dbc.Card(
                dbc.CardBody(
                    dcc.Graph(
                        id='grafico-situçãogeral',
                        figure=fig1
                    )),style={"width": "100%"},
            ),width=8),
        dbc.Col(
            dbc.Card(
                dbc.CardBody(
                    dcc.Graph(
                        id='quantidade-total',
                        figure=fig2)
                    ),style={"width": "100%"},
        ),width=4),
    ],style={"width": "100%"}),

    dbc.Row([
        dbc.Col(
            dbc.Card(
                dbc.CardBody(
                    dcc.Graph(
                        id='grafico-situçãoeng',
                        figure=fig3
                    )),style={"width": "100%"},
            ),width=4),
        dbc.Col(
            dbc.Card(
                dbc.CardBody(
                    dcc.Graph(
                        id='grafico-situaçãotel',
                        figure=fig4)
                    ),style={"width": "100%"},
        ),width=4),
        dbc.Col([
            dbc.Row(
                dbc.Card(
                    dbc.CardBody(
                        dcc.Graph(
                            id='quantidade-totaleng',
                            figure=fig5,style={"width": "100%","height":"100%"})
                    ),style={"width": "100%","height":"100%"},
                ),style={"height":"50%"}),
            dbc.Row(dbc.Card(
                    dbc.CardBody(
                        dcc.Graph(
                            id='quantidade-totaltel',
                            figure=fig6,style={"width": "100%","height":"100%"})
                    ),style={"width": "100%","height":"100%"},
                ),style={"height":"50%"})
        ],width=4),
    ],style={"width": "100%"}),

    dbc.Row([
        dbc.Col(
            dbc.Card(
                dbc.CardBody(
                    dcc.Graph(
                        id='grafico-tempoconclusaoeng',
                        figure=fig7
                    )),style={"width": "100%"},
            ),width=6),
        dbc.Col(
            dbc.Card(
                dbc.CardBody(
                    dcc.Graph(
                        id='grafico-tempoconclusaotel',
                        figure=fig8)
                    ),style={"width": "100%"},
        ),width=6),
    ],style={"width": "100%"})
    
],style={"width": "100%"})


if __name__ == '__main__':
    app.run_server(debug=True)