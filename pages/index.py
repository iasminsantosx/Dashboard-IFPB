from dash import  html, dcc
import plotly.express as px
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
from tratamento_de_dados import geral
import pandas as pd


###########################Base de Dados###################################################
path_engenharia_de_computacao = '/home/iasmin/Documentos/TCC-Dashboard/dados_engenharia.xlsx'
path_telematica = '/home/iasmin/Documentos/TCC-Dashboard/dados_telematica.xlsx'

df_engenharia = pd.read_excel(path_engenharia_de_computacao)
df_telematica = pd.read_excel(path_telematica)
df_engenharia_novo = pd.read_excel(path_engenharia_de_computacao,sheet_name="NOVO")
df_telematica_novo = pd.read_excel(path_telematica,sheet_name="NOVO")

df = pd.concat([df_engenharia,df_telematica], axis=0)
df_novo = pd.concat([df_engenharia_novo,df_telematica_novo], axis=0)
#######################################TRATAMENTO DE DADOS################################
df,df_novo = geral(df,df_novo)

df_agrupado = df.copy()
df_agrupado['Situacao'] = df_agrupado['Situacao'].replace( ['cancelado voluntariamente', 'cancelado compulsoriamente', 'trancado', 'evadido', 'afastado', 'trancado voluntariamente','transferido externamente', 'transferido internamente'], 'evadido/trancado')
df_agrupado['Situacao'] = df_agrupado['Situacao'].replace( ['matriculado',  'intercambio', 'vinculado'], 'matriculado')
df_agrupado['Situacao'].unique()
##############################PLOTANDO GRAFICOS#############################################################

#Situação Geral
df_situacao_geral = df_agrupado['Situacao'].value_counts().to_frame()

valor_absoluto1 = df_agrupado['Situacao'].value_counts()
porcentagem1 = valor_absoluto1.apply((lambda x: (x*100)/df_agrupado['Situacao'].value_counts().sum()))

colors = ['#FF6347','#6495ED','#9ACD32','black']

fig1 = px.bar(df_situacao_geral,x=df_situacao_geral.index,y='count', title='Alunos por Situações nos cursos de TIC',text=[str('{:,.2f}'.format(i)) +' %' for i in (porcentagem1)],color_discrete_sequence=[colors])
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

#Evasão por Ano de Ingresso
df_ano_evasao_engenharia = df_engenharia_novo[df_engenharia_novo.Situacao.isin(['Afastado', 'Cancelado compulsoriamente', 'Cancelado voluntariamente', 'Evadido'])]
grafico_ano_evasao_engenharia = df_ano_evasao_engenharia['Ano de ingresso'].value_counts().sort_index()

df_ano_evasao_telematica = df_telematica_novo[df_telematica_novo.Situacao.isin(['Afastado', 'Cancelado compulsoriamente', 'Cancelado voluntariamente', 'Evadido'])]
grafico_ano_evasao_telematica = df_ano_evasao_telematica['Ano de ingresso'].value_counts().sort_index()

fig3 = go.Figure()
fig3.add_trace(go.Scatter(x = grafico_ano_evasao_engenharia.index, y = grafico_ano_evasao_engenharia.values, name = 'Engenharia de Computação'))
fig3.add_trace(go.Scatter(x = grafico_ano_evasao_telematica.index, y = grafico_ano_evasao_telematica.values, name = 'Telemática'))

fig3.update_layout(yaxis={'title':'Número de Alunos evadidos'},
                   xaxis={'title': 'Ano de Ingresso'},title='Números de alunos evadidos pelo ano de ingresso')

#AlunosxModalidade
colors = ['#33e0ff','#ff33dd']
fig4 = px.pie(values=df['Modalidade'].value_counts(), names=df['Modalidade'].value_counts().index,
             color_discrete_sequence=colors)

fig4.update_traces(textposition='outside', textinfo='percent+label', 
                  hole=.6, hoverinfo="label+percent+name",title='Alunos por Modalidade')
fig4.update_layout(margin = dict(t=0, l=0, r=0, b=0))

#AlunosxSexo
colors = ['#33e0ff','#ff33dd']
fig5 = px.pie(values=df['Sexo'].value_counts(), names=df['Sexo'].value_counts().index,
             color_discrete_sequence=colors)

fig5.update_traces(textposition='outside', textinfo='percent+label', 
                  hole=.6, hoverinfo="label+percent+name",title='Alunos por Sexo')
fig5.update_layout(margin = dict(t=0, l=0, r=0, b=0))

#AlunosXCor/Raca
valor_absoluto = df['Cor_Raca'].value_counts()
porcentagem = valor_absoluto.apply((lambda x: (x*100)/df['Cor_Raca'].value_counts().sum()))
colors = ['#33e0ff','#338aff','#3342ff','#6e33ff','#bb33ff','#d133ff','#e033ff','#ff33fc','#ff33dd','#ff33af','#ff3383','#ff3361']
fig6 = px.bar(porcentagem,title='Alunos por Cor/Raca dos cursos de TIC',
             orientation='h',text=[i+' ' + str('{:,.2f}'.format(j)) +' %' for i,j in zip(valor_absoluto.index,porcentagem)],color_discrete_sequence=[colors],
            )
fig6.update_layout(plot_bgcolor = 'white',
                  margin = dict(t=35, l=10, r=0, b=10),showlegend=False,
                  yaxis={'categoryorder':'total descending'})
fig6.update_traces(textposition='auto')
fig6.update_xaxes(visible=False)
fig6.update_yaxes(visible=False)

#AlunosxTipoEscola
df_sem_traco1 = df[df.Tipo_da_escola_anterior!='-']
colors = ['#33e0ff','#338aff','#3342ff','#6e33ff','#bb33ff','#d133ff','#e033ff','#ff33fc','#ff33dd','#ff33af','#ff3383','#ff3361']

fig7 = px.pie(values=df_sem_traco1['Tipo_da_escola_anterior'].value_counts(), names=df_sem_traco1['Tipo_da_escola_anterior'].value_counts().index,
             color_discrete_sequence=colors)

fig7.update_layout(margin = dict(t=50, l=100, r=100, b=0),title='Aluno por Tipo da escola anterior nos cursos de TIC')

fig7.update_traces(textfont_size=16)

#AlunosxTipoZona
df_sem_traco2 = df[df.Tipo_da_zona_residencial!='-']
colors = ['#33e0ff','#338aff','#3342ff','#6e33ff','#bb33ff','#d133ff','#e033ff','#ff33fc','#ff33dd','#ff33af','#ff3383','#ff3361']

fig8 = px.pie(values=df_sem_traco2['Tipo_da_zona_residencial'].value_counts(), names=df_sem_traco2['Tipo_da_zona_residencial'].value_counts().index,
             color_discrete_sequence=colors)

fig8.update_layout(margin = dict(t=50, l=100, r=100, b=0),title='Aluno por Tipo da zona residencial nos cursos de TIC')

fig8.update_traces(textfont_size=16)

#Naturalidade
df_sem_traco3 = df[df.Naturalidade!='-']
cidades = df_sem_traco3['Naturalidade'].value_counts().to_list()

##################################################
#Filtrando as 10 cidades com mais alunos do curso
lista_top10_cidades_values1 = []
lista_top10_cidades_values_nomes1 = []

for i in range(9):
  lista_top10_cidades_values1.append(cidades[i])


nomes = df_sem_traco3['Naturalidade'].value_counts().index

for i in range(9):
  lista_top10_cidades_values_nomes1.append(nomes[i])
####################################################

fig9 = px.bar(x=lista_top10_cidades_values_nomes1,y=lista_top10_cidades_values1,title='Top 10 Naturalidades dos Alunos dos cursos de TIC',color_discrete_sequence=[colors])

#Bairros
df_sem_traco3 = df[df.Bairro!='-']
bairros = df_sem_traco3['Bairro'].value_counts().to_list()

##################################################
#Filtrando as 10 bairro com mais alunos do curso
lista_top10_bairros_values = []
lista_top10_bairros_values_nomes = []

for i in range(9):
  lista_top10_bairros_values.append(bairros[i])


nomes = df_sem_traco3['Bairro'].value_counts().index

for i in range(9):
  lista_top10_bairros_values_nomes.append(nomes[i])
####################################################

fig10 = px.bar(x=lista_top10_bairros_values_nomes,y=lista_top10_bairros_values,title='Top 10 Bairros dos Alunos dos cursos de TIC',color_discrete_sequence=[colors])

#CotaSISTEC
df_sem_traco4 = df[df.Cota_SISTEC!='-']
colors = ['#33e0ff','#338aff','#3342ff','#6e33ff','#bb33ff','#d133ff','#e033ff','#ff33fc','#ff33dd','#ff33af','#ff3383','#ff3361']

fig11 = px.pie(values=df_sem_traco4['Cota_SISTEC'].value_counts(), names=df_sem_traco4['Cota_SISTEC'].value_counts().index,
             color_discrete_sequence=colors)

fig11.update_layout(margin = dict(t=50, l=100, r=100, b=0),title='Aluno por Cota SISTEC nos cursos de TIC')

fig11.update_traces(textfont_size=16)

#FaixadeRenda
valor_absoluto3 = df['Faixa_de_renda_(SISTEC)'].value_counts()
porcentagem3 = valor_absoluto3.apply((lambda x: (x*100)/df['Faixa_de_renda_(SISTEC)'].value_counts().sum()))
colors = ['#33e0ff','#338aff','#3342ff','#6e33ff','#bb33ff','#d133ff','#e033ff','#ff33fc','#ff33dd','#ff33af','#ff3383','#ff3361']
fig12 = px.bar(porcentagem3,
             orientation='h',text=[i+'   ' + str('{:,.2f}'.format(j)) +' %' for i,j in zip(valor_absoluto3.index,porcentagem3)],color_discrete_sequence=[colors],title='Alunos por Faixa de Renda'
            )
fig12.update_layout(margin = dict(t=35, l=10, r=0, b=10),plot_bgcolor = 'white',
                  yaxis={'categoryorder':'total descending'},
                  showlegend=False
                 )
fig12.update_traces(textposition='auto')
fig12.update_xaxes(visible=False)
fig12.update_yaxes(visible=False)

#FormadeIngresso
valor_absoluto4 = df['Forma_de_ingresso'].value_counts()
porcentagem4 = valor_absoluto4.apply((lambda x: (x*100)/df['Forma_de_ingresso'].value_counts().sum()))
colors = ['#33e0ff','#338aff','#3342ff','#6e33ff','#bb33ff','#d133ff','#e033ff','#ff33fc','#ff33dd','#ff33af','#ff3383','#ff3361']
fig13 = px.bar(porcentagem4,
             orientation='h',text=[i+'   ' + str('{:,.2f}'.format(j)) +' %' for i,j in zip(valor_absoluto4.index,porcentagem4)],color_discrete_sequence=[colors],title='Aluno por Forma de ingresso'
            )
fig13.update_layout(margin = dict(t=35, l=10, r=0, b=10),
                    plot_bgcolor = 'white',
                    yaxis={'categoryorder':'total descending'},
                    showlegend=False
                 )
fig13.update_traces(textposition='auto')
fig13.update_xaxes(visible=False)
fig13.update_yaxes(visible=False)

#AlunoPorIdade
df_formata_idade = df.copy()
df_formata_idade.loc[:,'Idade'] = df_formata_idade['Idade'].astype(str)
df_idade = df_formata_idade['Idade'].value_counts().to_frame()
df_idade = df_idade.rename(columns={'Idade': 'Quantidade'})
df_idade = df_idade.head(10)



colors = ['#33e0ff','#338aff','#3342ff','#6e33ff','#bb33ff','#d133ff','#e033ff','#ff33fc','#ff33dd','#ff33af','#ff3383','#ff3361']
fig14 = px.bar(df_idade,x=df_idade.index,y='count',title='Aluno por idade',color_discrete_sequence=[colors])
fig14.update_layout(yaxis={'title':'Quantidade de Alunos pela Idade'},
                   xaxis={'title': 'Idade'})
###################################LAYOUT###################################################################


layout = html.Div([
    dbc.Row([
        dbc.Col(
            dbc.Card(
                dbc.CardBody(
                    dcc.Graph(
                        figure=fig1
                    )),style={"width": "100%"},
            ),width=6),
        dbc.Col(
            dbc.Card(
                dbc.CardBody(
                    dcc.Graph(
                        id='quantidade-total',
                        figure=fig2)
                    ),style={"width": "100%"},
        ),width=6)
    ],style={"width": "100%"}),

    dbc.Row([
        dbc.Col(
            dbc.Card(
                dbc.CardBody(
                    dcc.Graph(
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
                        figure=fig6)
                    ),style={"width": "100%"},
        ),width=4),
    ],style={"width": "100%"}),

    dbc.Row([
        dbc.Col(
            dbc.Card(
                dbc.CardBody(
                    dcc.Graph(
                        figure=fig9
                    )),style={"width": "100%"},
            ),width=6),
        dbc.Col(
            dbc.Card(
                dbc.CardBody(
                    dcc.Graph(
                        figure=fig10)
                    ),style={"width": "100%"},
        ),width=6)
    ],style={"width": "100%"}),

    dbc.Row([
        dbc.Col(
            dbc.Card(
                dbc.CardBody(
                    dcc.Graph(
                        figure=fig7
                    )),style={"width": "100%"},
            ),width=4),
        dbc.Col(
            dbc.Card(
                dbc.CardBody(
                    dcc.Graph(
                        id='grafico-situaçãotel',
                        figure=fig8)
                    ),style={"width": "100%"},
        ),width=4),
        dbc.Col(
            dbc.Card(
                dbc.CardBody(
                    dcc.Graph(
                        id='grafico-situaçãotel',
                        figure=fig11)
                    ),style={"width": "100%"},
        ),width=4),
    ],style={"width": "100%"}),
    dbc.Row([
        dbc.Col(
            dbc.Card(
                dbc.CardBody(
                    dcc.Graph(
                        figure=fig12
                    )),style={"width": "100%"},
            ),width=4),
        dbc.Col(
            dbc.Card(
                dbc.CardBody(
                    dcc.Graph(
                        id='grafico-situaçãotel',
                        figure=fig13)
                    ),style={"width": "100%"},
        ),width=4),
        dbc.Col(
            dbc.Card(
                dbc.CardBody(
                    dcc.Graph(
                        id='grafico-situaçãotel',
                        figure=fig14)
                    ),style={"width": "100%"},
        ),width=4),
    ],style={"width": "100%"}),
    
],style={"width": "100%"})


