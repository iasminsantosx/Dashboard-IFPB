from dash import Dash, html, dcc
import dash
import plotly.express as px
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
from base_de_dados import dataframe, dataframenovo
from tratamento_de_dados import geral
from funcoes import descreve_informacoes


###########################Base de Dados###################################################
path_engenharia_de_computacao = '/home/iasmin/Documentos/TCC-Dashboard/dados_engenharia.xlsx'
path_telematica = '/home/iasmin/Documentos/TCC-Dashboard/dados_telematica.xlsx'

df = dataframe(path_engenharia_de_computacao,path_telematica)
df_novo = dataframenovo(path_engenharia_de_computacao,path_telematica)

#######################################TRATAMENTO DE DADOS################################
df,df_novo = geral(df,df_novo)

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

fig4.update_layout(margin = dict(t=50, l=100, r=100, b=0),title='Aluno por Tipo da escola anterior nos cursos de TIC')

fig4.update_traces(textfont_size=16)

#AlunosxTipoZona
df_sem_traco = df[df.Tipo_da_zona_residencial!='-']
colors = ['#33e0ff','#338aff','#3342ff','#6e33ff','#bb33ff','#d133ff','#e033ff','#ff33fc','#ff33dd','#ff33af','#ff3383','#ff3361']

fig5 = px.pie(values=df_sem_traco['Tipo_da_zona_residencial'].value_counts(), names=df_sem_traco['Tipo_da_zona_residencial'].value_counts().index,
             color_discrete_sequence=colors)

fig5.update_layout(margin = dict(t=50, l=100, r=100, b=0),title='Aluno por Tipo da zona residencial nos cursos de TIC')

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

fig7.update_layout(margin = dict(t=50, l=100, r=100, b=0),title='Aluno por Cota SISTEC nos cursos de TIC')

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
             orientation='h',text=[i+'   ' + str('{:,.2f}'.format(j)) +' %' for i,j in zip(valor_absoluto.index,porcentagem)],color_discrete_sequence=[colors],title='Aluno por Forma de ingresso'
            )
fig9.update_layout(margin = dict(t=35, l=10, r=0, b=10),
                    plot_bgcolor = 'white',
                    yaxis={'categoryorder':'total descending'},
                    showlegend=False
                 )
fig9.update_traces(textposition='auto')
fig9.update_xaxes(visible=False)
fig9.update_yaxes(visible=False)

#AlunoPorIdade
df_idade = df['Idade'].value_counts().to_frame()
df_idade = df_idade.rename(columns={'Idade': 'Quantidade'})
df_idade = df_idade.head(10)

colors = ['#33e0ff','#338aff','#3342ff','#6e33ff','#bb33ff','#d133ff','#e033ff','#ff33fc','#ff33dd','#ff33af','#ff3383','#ff3361']
fig10 = px.bar(df_idade,x=df_idade.index,y='count',title='Aluno por idade',color_discrete_sequence=[colors])
fig10.update_layout(yaxis={'title':'Quantidade de Alunos pela Idade'},
                   xaxis={'title': 'Idade'})

#Coeficiente de progressão
tabela = descreve_informacoes(df)
fig11 = go.Figure(data=[go.Table(
    header=dict(values=['Medidas', 'Coeficiente de Progressão'],
                line_color='#6495ED',
                fill_color='lightskyblue',
                align='center'),
    cells=dict(values=[['Quantidade', 'Média', 'Desvio padrão', 'Valor mínimo','Q1','Q2/Mediana','Q3','Valor máximo','Moda','Variância','Amplitude','Assimetria'], # 1st column
                       [1278, 30.96, 33.36, 0.0,0.0,18.43,47.11,100.00,0.0,1112.95,100,0.21]], # 2nd column
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
                        figure=fig10)
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
    
],style={"width": "100%"})


# if __name__ == '__main__':
#     app.run_server(debug=True)