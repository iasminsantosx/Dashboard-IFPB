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

#AlunosxModalidade
colors = ['#33e0ff','#ff33dd']
fig1 = px.pie(values=df['Modalidade'].value_counts(), names=df['Modalidade'].value_counts().index,
             color_discrete_sequence=colors)

fig1.update_traces(textposition='outside', textinfo='percent+label', 
                  hole=.6, hoverinfo="label+percent+name",title='Alunos por Modalidade')
fig1.update_layout(margin = dict(t=0, l=0, r=0, b=0))

#AlunosxSexos
colors = ['#33e0ff','#ff33dd']
fig2 = px.pie(values=df['Sexo'].value_counts(), names=df['Sexo'].value_counts().index,
             color_discrete_sequence=colors)

fig2.update_traces(textposition='outside', textinfo='percent+label', 
                  hole=.6, hoverinfo="label+percent+name",title='Alunos por Sexo')
fig2.update_layout(margin = dict(t=0, l=0, r=0, b=0))

#AlunosXCor/Raca
valor_absoluto = df['Cor_Raca'].value_counts()
porcentagem = valor_absoluto.apply((lambda x: (x*100)/df['Cor_Raca'].value_counts().sum()))
colors = ['#33e0ff','#338aff','#3342ff','#6e33ff','#bb33ff','#d133ff','#e033ff','#ff33fc','#ff33dd','#ff33af','#ff3383','#ff3361']
fig3 = px.bar(porcentagem,title='Alunos por Cor/Raca dos cursos de TIC',
             orientation='h',text=[i+' ' + str('{:,.2f}'.format(j)) +' %' for i,j in zip(valor_absoluto.index,porcentagem)],color_discrete_sequence=[colors],
            )
fig3.update_layout(plot_bgcolor = 'white',
                  margin = dict(t=35, l=10, r=0, b=10),showlegend=False,
                  yaxis={'categoryorder':'total descending'})
fig3.update_traces(textposition='auto')
fig3.update_xaxes(visible=False)
fig3.update_yaxes(visible=False)

#AlunosxTipoEscola
df_sem_traco = df[df.Tipo_da_escola_anterior!='-']
colors = ['#33e0ff','#338aff','#3342ff','#6e33ff','#bb33ff','#d133ff','#e033ff','#ff33fc','#ff33dd','#ff33af','#ff3383','#ff3361']

fig4 = px.pie(values=df_sem_traco['Tipo_da_escola_anterior'].value_counts(), names=df_sem_traco['Tipo_da_escola_anterior'].value_counts().index,
             color_discrete_sequence=colors)

fig4.update_layout(margin = dict(t=50, l=100, r=100, b=0),title='Aluno por Tipo da escola anterior sem os não declarados nos cursos de TIC')

fig4.update_traces(textfont_size=16)

#AlunosxTipoZona
df_sem_traco = df[df.Tipo_da_zona_residencial!='-']
colors = ['#33e0ff','#338aff','#3342ff','#6e33ff','#bb33ff','#d133ff','#e033ff','#ff33fc','#ff33dd','#ff33af','#ff3383','#ff3361']

fig5 = px.pie(values=df_sem_traco['Tipo_da_zona_residencial'].value_counts(), names=df_sem_traco['Tipo_da_zona_residencial'].value_counts().index,
             color_discrete_sequence=colors)

fig5.update_layout(margin = dict(t=50, l=100, r=100, b=0),title='Aluno por Tipo da zona residencial, sem os não declarados nos cursos de TIC')

fig5.update_traces(textfont_size=16)

#Naturalidade
df_sem_traco = df[df.Naturalidade!='-']
cidades = df_sem_traco['Naturalidade'].value_counts().to_list()

##################################################
#Filtrando as 10 cidades com mais alunos do curso
lista_top10_cidades_values = []
lista_top10_cidades_values_nomes = []

for i in range(9):
  lista_top10_cidades_values.append(cidades[i])


nomes = df_sem_traco['Naturalidade'].value_counts().index

for i in range(9):
  lista_top10_cidades_values_nomes.append(nomes[i])
####################################################

fig10 = px.bar(x=lista_top10_cidades_values_nomes,y=lista_top10_cidades_values,title='Top 10 Naturalidades dos Alunos dos cursos de TIC',color_discrete_sequence=[colors])

#Bairros
df_sem_traco = df[df.Bairro!='-']
bairros = df_sem_traco['Bairro'].value_counts().to_list()

##################################################
#Filtrando as 10 bairro com mais alunos do curso
lista_top10_bairros_values = []
lista_top10_bairros_values_nomes = []

for i in range(9):
  lista_top10_bairros_values.append(bairros[i])


nomes = df_sem_traco['Bairro'].value_counts().index

for i in range(9):
  lista_top10_bairros_values_nomes.append(nomes[i])
####################################################

fig6 = px.bar(x=lista_top10_bairros_values_nomes,y=lista_top10_bairros_values,title='Top 10 Bairros dos Alunos dos cursos de TIC',color_discrete_sequence=[colors])

#CotaSISTEC
df_sem_traco = df[df.Cota_SISTEC!='-']
colors = ['#33e0ff','#338aff','#3342ff','#6e33ff','#bb33ff','#d133ff','#e033ff','#ff33fc','#ff33dd','#ff33af','#ff3383','#ff3361']

fig7 = px.pie(values=df_sem_traco['Cota_SISTEC'].value_counts(), names=df_sem_traco['Cota_SISTEC'].value_counts().index,
             color_discrete_sequence=colors)

fig7.update_layout(margin = dict(t=50, l=100, r=100, b=0),title='Aluno por Cota SISTEC, sem os não declarados nos cursos de TIC')

fig7.update_traces(textfont_size=16)

#FaixadeRenda
valor_absoluto = df['Faixa_de_renda_(SISTEC)'].value_counts()
porcentagem = valor_absoluto.apply((lambda x: (x*100)/df['Faixa_de_renda_(SISTEC)'].value_counts().sum()))
colors = ['#33e0ff','#338aff','#3342ff','#6e33ff','#bb33ff','#d133ff','#e033ff','#ff33fc','#ff33dd','#ff33af','#ff3383','#ff3361']
fig8 = px.bar(porcentagem,
             orientation='h',text=[i+'   ' + str('{:,.2f}'.format(j)) +' %' for i,j in zip(valor_absoluto.index,porcentagem)],color_discrete_sequence=[colors],title='Alunos por Faixa de Renda'
            )
fig8.update_layout(margin = dict(t=35, l=10, r=0, b=10),plot_bgcolor = 'white',
                  yaxis={'categoryorder':'total descending'},
                  showlegend=False
                 )
fig8.update_traces(textposition='auto')
fig8.update_xaxes(visible=False)
fig8.update_yaxes(visible=False)

#FormadeIngresso
valor_absoluto = df['Forma_de_ingresso'].value_counts()
porcentagem = valor_absoluto.apply((lambda x: (x*100)/df['Forma_de_ingresso'].value_counts().sum()))
colors = ['#33e0ff','#338aff','#3342ff','#6e33ff','#bb33ff','#d133ff','#e033ff','#ff33fc','#ff33dd','#ff33af','#ff3383','#ff3361']
fig9 = px.bar(porcentagem,
             orientation='h',text=[i+'   ' + str('{:,.2f}'.format(j)) +' %' for i,j in zip(valor_absoluto.index,porcentagem)],color_discrete_sequence=[colors],
            )
fig9.update_layout(margin = dict(t=10, l=10, r=0, b=10),
                  yaxis={'categoryorder':'total descending'},
                  legend=dict(title='Aluno por Forma de ingresso'),
                  showlegend=True
                 )
fig9.update_traces(textposition='auto')
fig9.update_xaxes(visible=False)
fig9.update_yaxes(visible=False)
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
    brand="Perfil Geral",
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
            ),width=3),
        dbc.Col(
            dbc.Card(
                dbc.CardBody(
                    dcc.Graph(
                        id='quantidade-total',
                        figure=fig2)
                    ),style={"width": "100%"},
        ),width=3),
        dbc.Col(
            dbc.Card(
                dbc.CardBody(
                    dcc.Graph(
                        id='quantidade-total',
                        figure=fig3)
                    ),style={"width": "100%"},
        ),width=3),
        dbc.Col(
            dbc.Card(
                dbc.CardBody(
                    dcc.Graph(
                        id='quantidade-total',
                        figure=fig8)
                    ),style={"width": "100%"},
        ),width=3)
    ],style={"width": "100%"}),

    dbc.Row([
        dbc.Col(
            dbc.Card(
                dbc.CardBody(
                    dcc.Graph(
                        id='grafico-situçãoeng',
                        figure=fig4
                    )),style={"width": "100%"},
            ),width=4),
        dbc.Col(
            dbc.Card(
                dbc.CardBody(
                    dcc.Graph(
                        id='grafico-situaçãotel',
                        figure=fig5)
                    ),style={"width": "100%"},
        ),width=4),
        dbc.Col(
            dbc.Card(
                dbc.CardBody(
                    dcc.Graph(
                        id='grafico-situaçãotel',
                        figure=fig7)
                    ),style={"width": "100%"},
        ),width=4),
    ],style={"width": "100%"}),

    dbc.Row([
        dbc.Col(
            dbc.Card(
                dbc.CardBody(
                    dcc.Graph(
                        id='grafico-tempoconclusaoeng',
                        figure=fig6
                    )),style={"width": "100%"},
            ),width=6),
        dbc.Col(
            dbc.Card(
                dbc.CardBody(
                    dcc.Graph(
                        id='grafico-tempoconclusaotel',
                        figure=fig10)
                    ),style={"width": "100%"},
        ),width=6)
    ],style={"width": "100%"})
    
],style={"width": "100%"})


if __name__ == '__main__':
    app.run_server(debug=True)