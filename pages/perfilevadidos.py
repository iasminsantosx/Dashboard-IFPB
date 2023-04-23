from dash import Dash, html, dcc
import plotly.express as px
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
from base_de_dados import dataframe, dataframenovo,df_engenharia_telematica
from tratamento_de_dados import geral,renomenado_colunas_tel_eng
from funcoes import descreve_informacoes
import dash

###########################Base de Dados###################################################
path_engenharia_de_computacao = '/home/iasmin/Documentos/TCC-Dashboard/dados_engenharia.xlsx'
path_telematica = '/home/iasmin/Documentos/TCC-Dashboard/dados_telematica.xlsx'

df = dataframe(path_engenharia_de_computacao,path_telematica)
df_novo = dataframenovo(path_engenharia_de_computacao,path_telematica)
df_engenharia_novo,df_telematica_novo = df_engenharia_telematica(path_engenharia_de_computacao,path_telematica)
#######################################TRATAMENTO DE DADOS################################
df,df_novo = geral(df,df_novo)
df_engenharia_novo,df_telematica_novo = renomenado_colunas_tel_eng(df_engenharia_novo,df_telematica_novo)
##############################PLOTANDO GRAFICOS#############################################################
df_evadidos = df[df.Situacao.isin(['trancado', 'evadido', 'cancelado compulsoriamente', 'cancelado voluntariamente','afastado','trancado voluntariamente','transferido externamente','transferido internamente'])]
#AlunosxModalidade
colors = ['#33e0ff','#ff33dd']
fig1 = px.pie(values=df_evadidos['Modalidade'].value_counts(), names=df_evadidos['Modalidade'].value_counts().index,
             color_discrete_sequence=colors)

fig1.update_traces(textposition='outside', textinfo='percent+label', 
                  hole=.6, hoverinfo="label+percent+name",title='Modalidade dos Alunos evadidos')
fig1.update_layout(margin = dict(t=0, l=0, r=0, b=0))

#AlunosxSexo
colors = ['#33e0ff','#ff33dd']
fig2 = px.pie(values=df_evadidos['Sexo'].value_counts(), names=df_evadidos['Sexo'].value_counts().index,
             color_discrete_sequence=colors)

fig2.update_traces(textposition='outside', textinfo='percent+label', 
                  hole=.6, hoverinfo="label+percent+name",title='Sexo dos Alunos evadidos')
fig2.update_layout(margin = dict(t=0, l=0, r=0, b=0))

#AlunosXCor/Raca
valor_absoluto = df_evadidos['Cor_Raca'].value_counts()
porcentagem = valor_absoluto.apply((lambda x: (x*100)/df_evadidos['Cor_Raca'].value_counts().sum()))
colors = ['#33e0ff','#338aff','#3342ff','#6e33ff','#bb33ff','#d133ff','#e033ff','#ff33fc','#ff33dd','#ff33af','#ff3383','#ff3361']
fig3 = px.bar(porcentagem,title='Cor/Raca dos evadidos',
             orientation='h',text=[i+' ' + str('{:,.2f}'.format(j)) +' %' for i,j in zip(valor_absoluto.index,porcentagem)],color_discrete_sequence=[colors],
            )
fig3.update_layout(plot_bgcolor = 'white',
                  margin = dict(t=35, l=10, r=0, b=10),showlegend=False)
fig3.update_traces(textposition='auto')
fig3.update_xaxes(visible=False)
fig3.update_yaxes(visible=False)

#AlunosxTipoEscola
df_evadidos = df[df.Situacao.isin(['trancado', 'evadido', 'cancelado compulsoriamente', 'cancelado voluntariamente','afastado','trancado voluntariamente','transferido externamente','transferido internamente','falecido']) & (df['Tipo_da_escola_anterior']!='-')]
colors = ['#33e0ff','#338aff','#3342ff','#6e33ff','#bb33ff','#d133ff','#e033ff','#ff33fc','#ff33dd','#ff33af','#ff3383','#ff3361']

fig4 = px.pie(values=df_evadidos['Tipo_da_escola_anterior'].value_counts(), names=df_evadidos['Tipo_da_escola_anterior'].value_counts().index,
             color_discrete_sequence=colors)

fig4.update_layout(margin = dict(t=50, l=100, r=100, b=0),title='Tipo_da_escola_anterior_dos_alunos_evadidos')

fig4.update_traces(textfont_size=16)

#AlunosxTipoZona
df_evadidos = df[df.Situacao.isin(['trancado', 'evadido', 'cancelado compulsoriamente', 'cancelado voluntariamente','afastado','trancado voluntariamente','transferido externamente','transferido internamente','falecido']) & (df['Tipo_da_zona_residencial']!='-')]
colors = ['#33e0ff','#338aff','#3342ff','#6e33ff','#bb33ff','#d133ff','#e033ff','#ff33fc','#ff33dd','#ff33af','#ff3383','#ff3361']

fig5 = px.pie(values=df_evadidos['Tipo_da_zona_residencial'].value_counts(), names=df_evadidos['Tipo_da_zona_residencial'].value_counts().index,
             color_discrete_sequence=colors)

fig5.update_layout(margin = dict(t=50, l=100, r=100, b=0),title='Tipo da zona residencial dos alunos evadidos')

fig5.update_traces(textfont_size=16)

#Naturalidade
df_evadidos = df[df.Situacao.isin(['trancado', 'evadido', 'cancelado compulsoriamente', 'cancelado voluntariamente','afastado','trancado voluntariamente','transferido externamente','transferido internamente','falecido']) & (df['Naturalidade']!='-')]
cidades = df_evadidos['Naturalidade'].value_counts().to_list()

##################################################
#Filtrando as 10 cidades com mais alunos do curso
lista_top10_cidades_values = []
lista_top10_cidades_values_nomes = []

for i in range(9):
  lista_top10_cidades_values.append(cidades[i])


nomes = df_evadidos['Naturalidade'].value_counts().index

for i in range(9):
  lista_top10_cidades_values_nomes.append(nomes[i])
####################################################
colors = ['#33e0ff','#338aff','#3342ff','#6e33ff','#bb33ff','#d133ff','#e033ff','#ff33fc','#ff33dd','#ff33af','#ff3383','#ff3361']
fig10 = px.bar(x=lista_top10_cidades_values_nomes,y=lista_top10_cidades_values,title='Top 10 Naturalidades dos Alunos evadidos',color_discrete_sequence=[colors])

#Bairros
df_evadidos = df[df.Situacao.isin(['trancado', 'evadido', 'cancelado compulsoriamente', 'cancelado voluntariamente','afastado','trancado voluntariamente','transferido externamente','transferido internamente']) & (df['Bairro']!='-')]
cidades = df_evadidos['Bairro'].value_counts().to_list()

##################################################
#Filtrando as 10 cidades com mais alunos do curso
lista_top10_cidades_values = []
lista_top10_cidades_values_nomes = []

for i in range(9):
  lista_top10_cidades_values.append(cidades[i])


nomes = df_evadidos['Bairro'].value_counts().index

for i in range(9):
  lista_top10_cidades_values_nomes.append(nomes[i])
####################################################
colors = ['#33e0ff','#338aff','#3342ff','#6e33ff','#bb33ff','#d133ff','#e033ff','#ff33fc','#ff33dd','#ff33af','#ff3383','#ff3361']
fig6 = px.bar(x=lista_top10_cidades_values_nomes,y=lista_top10_cidades_values,title='Top 10 Bairros dos Alunos evadidos',color_discrete_sequence=[colors])

#CotaSISTEC
df_evadidos = df[df.Situacao.isin(['trancado', 'evadido', 'cancelado compulsoriamente', 'cancelado voluntariamente','afastado','trancado voluntariamente','transferido externamente','transferido internamente','falecido']) & (df['Cota_SISTEC']!='-')]
colors = ['#33e0ff','#338aff','#3342ff','#6e33ff','#bb33ff','#d133ff','#e033ff','#ff33fc','#ff33dd','#ff33af','#ff3383','#ff3361']

fig7 = px.pie(values=df_evadidos['Cota_SISTEC'].value_counts(), names=df_evadidos['Cota_SISTEC'].value_counts().index,
             color_discrete_sequence=colors)

fig7.update_layout(margin = dict(t=50, l=100, r=100, b=0),title='Tipo de cotas dos alunos evadidos')

fig7.update_traces(textfont_size=16)

#FaixadeRenda
df_evadidos = df[df.Situacao.isin(['trancado', 'evadido', 'cancelado compulsoriamente', 'cancelado voluntariamente','afastado','trancado voluntariamente','transferido externamente','transferido internamente']) & (df['Faixa_de_renda_(SISTEC)']!='nao declarado')]
valor_absoluto = df_evadidos['Faixa_de_renda_(SISTEC)'].value_counts()
porcentagem = valor_absoluto.apply((lambda x: (x*100)/df_evadidos['Faixa_de_renda_(SISTEC)'].value_counts().sum()))
colors = ['#33e0ff','#338aff','#3342ff','#6e33ff','#bb33ff','#d133ff','#e033ff','#ff33fc','#ff33dd','#ff33af','#ff3383','#ff3361']
fig8 = px.bar(porcentagem,
             orientation='h',text=[i+'   ' + str('{:,.2f}'.format(j)) +' %' for i,j in zip(valor_absoluto.index,porcentagem)],color_discrete_sequence=[colors],title='Faixa de Renda dos alunos evadidos'
            )
fig8.update_layout(plot_bgcolor = 'white',
                  margin = dict(t=35, l=10, r=0, b=10),
                  yaxis={'categoryorder':'total descending'},
                  showlegend=False
                 )
fig8.update_traces(textposition='auto')
fig8.update_xaxes(visible=False)
fig8.update_yaxes(visible=False)

#FormadeIngresso
df_evadidos = df[df.Situacao.isin(['trancado', 'evadido', 'cancelado compulsoriamente', 'cancelado voluntariamente','afastado','trancado voluntariamente','transferido externamente','transferido internamente'])]
valor_absoluto = df_evadidos['Forma_de_ingresso'].value_counts()
porcentagem = valor_absoluto.apply((lambda x: (x*100)/df_evadidos['Forma_de_ingresso'].value_counts().sum()))
colors = ['#33e0ff','#338aff','#3342ff','#6e33ff','#bb33ff','#d133ff','#e033ff','#ff33fc','#ff33dd','#ff33af','#ff3383','#ff3361']
fig9 = px.bar(porcentagem,
             orientation='h',text=[i+'   ' + str('{:,.2f}'.format(j)) +' %' for i,j in zip(valor_absoluto.index,porcentagem)],color_discrete_sequence=[colors],title='Forma de Ingresso do Alunos Evadidos')
fig9.update_layout(plot_bgcolor = 'white',
                  margin = dict(t=35, l=10, r=0, b=10),
                  yaxis={'categoryorder':'total descending'},
                  showlegend=False
                 )
fig9.update_traces(textposition='auto')
fig9.update_xaxes(visible=False)
fig9.update_yaxes(visible=False)

#EvasãoXAno
df_ano_evasao_engenharia = df_engenharia_novo[df_engenharia_novo.Situacao.isin(['Afastado', 'Cancelado compulsoriamente', 'Cancelado voluntariamente', 'Evadido'])]
grafico_ano_evasao_engenharia = df_ano_evasao_engenharia['Ano_de_ingresso'].value_counts().sort_index()

df_ano_evasao_telematica = df_telematica_novo[df_telematica_novo.Situacao.isin(['Afastado', 'Cancelado compulsoriamente', 'Cancelado voluntariamente', 'Evadido'])]
grafico_ano_evasao_telematica = df_ano_evasao_telematica['Ano_de_ingresso'].value_counts().sort_index()

fig11 = go.Figure()
fig11.add_trace(go.Scatter(x = grafico_ano_evasao_engenharia.index, y = grafico_ano_evasao_engenharia.values, name = 'Engenharia de Computação'))
fig11.add_trace(go.Scatter(x = grafico_ano_evasao_telematica.index, y = grafico_ano_evasao_telematica.values, name = 'Telemática'))

fig11.update_layout(yaxis={'title':'Número de Alunos evadidos'},
                   xaxis={'title': 'Ano de Ingresso'},title='Números de alunos evadidos pelo ano de ingresso')

#CoeficientedeProgressão
df_evadidos = df[(df.Situacao.isin(['trancado', 'evadido', 'cancelado compulsoriamente', 'cancelado voluntariamente','afastado','trancado voluntariamente','transferido externamente','transferido internamente']) & (df.Coeficiente_de_progressao!='-'))]
descreve_informacoes(df_evadidos)
fig12 = go.Figure(data=[go.Table(
    header=dict(values=['Medidas', 'Coeficiente de Progressão'],
                line_color='#6495ED',
                fill_color='lightskyblue',
                align='center'),
    cells=dict(values=[['Quantidade', 'Média', 'Desvio padrão', 'Valor mínimo','Q1','Q2/Mediana','Q3','Valor máximo','Moda','Variância','Amplitude','Assimetria'], # 1st column
                       [512, 15.49, 19.88, 0.0,0.0,7.76,25.81,98.14,0.0,395.27,98,0.39]], # 2nd column
               line_color='darkslategray',
               fill_color='lightcyan',
               align='center'))
])
###################################LAYOUT###################################################################


#dash.register_page(__name__)
layout = html.Div([
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
    ],style={"width": "100%"}),
    dbc.Row([
        dbc.Col(
            dbc.Card(
                dbc.CardBody(
                    dcc.Graph(
                        id='grafico-situçãoeng',
                        figure=fig9
                    )),style={"width": "100%"},
            ),width=4),
        dbc.Col(
            dbc.Card(
                dbc.CardBody(
                    dcc.Graph(
                        id='grafico-situaçãotel',
                        figure=fig11)
                    ),style={"width": "100%"},
        ),width=4),
        dbc.Col(
            dbc.Card(
                dbc.CardBody(
                    dcc.Graph(
                        id='grafico-situaçãotel',
                        figure=fig12)
                    ),style={"width": "100%"},
        ),width=4),
    ],style={"width": "100%"}),
    
],style={"width": "100%"})


# if __name__ == '__main__':
#     app.run_server(debug=True)