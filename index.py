from dash import Dash, html, dcc
import plotly.express as px
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
from base_de_dados import dataframe, dataframenovo, df_engenharia_telematica
from tratamento_de_dados import geral
import pandas as pd
import dash

###########################Base de Dados###################################################
path_engenharia_de_computacao = '/home/iasmin/Documentos/TCC-Dashboard/dados_engenharia.xlsx'
path_telematica = '/home/iasmin/Documentos/TCC-Dashboard/dados_telematica.xlsx'

df = dataframe(path_engenharia_de_computacao,path_telematica)
df_novo = dataframenovo(path_engenharia_de_computacao,path_telematica)

df_engenharia_novo,df_telematica_novo = df_engenharia_telematica(path_engenharia_de_computacao,path_telematica)
#######################################TRATAMENTO DE DADOS################################
df,df_novo = geral(df,df_novo)

df_agrupado = df.copy()
df_agrupado['Situacao'] = df_agrupado['Situacao'].replace( ['cancelado voluntariamente', 'cancelado compulsoriamente', 'trancado', 'evadido', 'afastado', 'trancado voluntariamente','transferido externamente', 'transferido internamente'], 'evadido/trancado')
df_agrupado['Situacao'] = df_agrupado['Situacao'].replace( ['matriculado',  'intercambio', 'vinculado'], 'matriculado')
df_agrupado['Situacao'].unique()
##############################PLOTANDO GRAFICOS#############################################################

#Situação Geral
df_situacao_geral = df_novo['Situacao'].value_counts().to_frame()

valor_absoluto = df_novo['Situacao'].value_counts()
porcentagem = valor_absoluto.apply((lambda x: (x*100)/df_novo['Situacao'].value_counts().sum()))

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
                         }})

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

#Meses Conclusão Engenharia
colors = ['orange']
fig17 = px.histogram(df_conclusao_eng,x='Meses Conclusao',color_discrete_sequence=colors,title='Distribuição de Meses para conclusão - Engenharia de Computação')

#Meses Conclusão Telematica
colors = ['#FF6347']
fig18 = px.histogram(df_conclusao_tel,x='Meses Conclusao',color_discrete_sequence=colors,title='Distribuição de Meses para conclusão - Telemática')

#SituaçãoxModalidade
colors = ['#FF6347','black','#9ACD32','#6495ED']
counts = df_agrupado.groupby(['Modalidade', 'Situacao']).size()
counts = counts.unstack(level=-1)

totals = counts.sum(axis=1)
percentages = counts.divide(totals, axis=0)*100


fig9 = px.bar(percentages,barmode = 'stack',color='Situacao', title='Situação dos alunos por Modalidade',color_discrete_sequence=colors)
fig9.update_layout(yaxis={'title':'Porcentagem'},
                   xaxis={'title': 'Modalidade'})

#SituaçãoxSexo
counts = df_agrupado.groupby(['Sexo','Situacao']).size()
counts = counts.unstack(level=-1)

totals = counts.sum(axis=1)
percentages = counts.divide(totals, axis=0)*100

colors = ['#FF6347','black','#9ACD32','#6495ED']

fig10 = px.bar(percentages,barmode = 'stack',color='Situacao', title='Situação dos alunos por Sexo',color_discrete_sequence=colors)
fig10.update_layout(yaxis={'title':'Porcentagem'},
                   xaxis={'title': 'Situacao'})

#SituaçãoxZona
df_sem_traco = df_agrupado[df_agrupado.Tipo_da_zona_residencial!='-']

counts = df_sem_traco.groupby(['Tipo_da_zona_residencial','Situacao']).size()
counts = counts.unstack(level=-1)

totals = counts.sum(axis=1)
percentages = counts.divide(totals, axis=0)*100

colors = ['#FF6347','black','#9ACD32','#6495ED']

fig11 = px.bar(percentages,barmode = 'stack',color='Situacao', title='Situação dos alunos por Tipo da zona residencial',color_discrete_sequence=colors)
fig11.update_layout(yaxis={'title':'Porcentagem'},
                   xaxis={'title': 'Situacao'})

#SituaçãoXCor
counts = df_agrupado.groupby(['Cor_Raca','Situacao']).size()
counts = counts.unstack(level=-1)

totals = counts.sum(axis=1)
percentages = counts.divide(totals, axis=0)*100

colors = ['#FF6347','black','#9ACD32','#6495ED']

fig12 = px.bar(percentages,barmode = 'stack',color='Situacao', title='Situação dos alunos por Cor/Raça',color_discrete_sequence=colors)
fig12.update_layout(yaxis={'title':'Porcentagem'},
                   xaxis={'title': 'Cor/Raca'})

#SituaçãoXEscola
df_sem_traco = df_agrupado[df_agrupado.Tipo_da_escola_anterior!='-']
counts = df_sem_traco.groupby(['Tipo_da_escola_anterior','Situacao']).size()
counts = counts.unstack(level=-1)

totals = counts.sum(axis=1)
percentages = counts.divide(totals, axis=0)*100

colors = ['#FF6347','black','#9ACD32','#6495ED']

fig13 = px.bar(percentages,barmode = 'stack',color='Situacao', title='Situação dos alunos por Tipo da escola anterior',color_discrete_sequence=colors)
fig13.update_layout(yaxis={'title':'Porcentagem'},
                   xaxis={'title': 'Tipo da escola anterior'})

#SituaçãoxCota
df_sem_traco = df_agrupado[df_agrupado.Cota_SISTEC!='-']
counts = df_sem_traco.groupby(['Cota_SISTEC','Situacao']).size()
counts = counts.unstack(level=-1)

totals = counts.sum(axis=1)
percentages = counts.divide(totals, axis=0)*100

colors = ['#FF6347','black','#9ACD32','#6495ED']

fig14 = px.bar(percentages,barmode = 'stack',color='Situacao', title='Situação dos alunos por Cota SISTEC',color_discrete_sequence=colors)
fig14.update_layout(yaxis={'title':'Porcentagem'},
                   xaxis={'title': 'Cota SISTEC'})

#SituaçãoxIdade
df_idade_maior_30 = df_agrupado[df_agrupado.Idade>=30]
colors = ['#FF6347','#6495ED','#9ACD32','black']

fig14 = px.pie(values=df_idade_maior_30['Situacao'].value_counts(), names=df_idade_maior_30['Situacao'].value_counts().index,
             color_discrete_sequence=colors)

fig14.update_layout(margin = dict(t=50, l=100, r=100, b=0),title='Situação dos Alunos com idade maior que 30, nos cursos de TIC')

fig14.update_traces(textfont_size=16)

df_idade_menor_30 = df_agrupado[df_agrupado.Idade<=30]
colors = ['#6495ED','#FF6347','#9ACD32','black']

fig15 = px.pie(values=df_idade_menor_30['Situacao'].value_counts(), names=df_idade_menor_30['Situacao'].value_counts().index,
             color_discrete_sequence=colors)

fig15.update_layout(margin = dict(t=50, l=100, r=100, b=0),title='Situação dos Alunos com idade menor que 30, nos cursos de TIC')

fig15.update_traces(textfont_size=16)

#SituaçãoxRenda
counts = df_agrupado.groupby(['Faixa_de_renda_(SISTEC)','Situacao']).size()
counts = counts.unstack(level=-1)

totals = counts.sum(axis=1)
percentages = counts.divide(totals, axis=0)*100

colors = ['#FF6347','black','#9ACD32','#6495ED']

fig16 = px.bar(percentages,barmode = 'stack',color='Situacao', title='Situação dos alunos por Faixa de renda (SISTEC)',color_discrete_sequence=colors)
fig16.update_layout(yaxis={'title':'Porcentagem'},
                   xaxis={'title': 'Faixa de renda (SISTEC)'})

#AlunosxNaturalidade
df_sem_traco = df_agrupado[df_agrupado.Naturalidade!='-']
counts = df_sem_traco.groupby(['Naturalidade','Situacao']).size()
counts = counts.unstack(level=-1)

soma = counts.sum(axis=1)
counts.insert(4, "Total", soma, True)
counts=counts.sort_values(by="Total", ascending=False)
counts=counts.drop(columns=['Total'])
counts=counts.head(10)

totals = counts.sum(axis=1)
percentages = counts.divide(totals, axis=0)*100

colors = ['#FF6347','black','#9ACD32','#6495ED']

fig19 = px.bar(percentages,barmode = 'stack',color='Situacao', title='Situação dos alunos por top 10 naturalidades',color_discrete_sequence=colors)
fig19.update_layout(yaxis={'title':'Porcentagem'},
                   xaxis={'title': 'Situacao'})

#AlunosxBairro
df_sem_traco = df_agrupado[df_agrupado.Naturalidade!='-']
counts = df_sem_traco.groupby(['Bairro','Situacao']).size()
counts = counts.unstack(level=-1)

soma = counts.sum(axis=1)
counts.insert(4, "Total", soma, True)
counts=counts.sort_values(by="Total", ascending=False)
counts=counts.drop(columns=['Total'])
counts=counts.head(10)

totals = counts.sum(axis=1)
percentages = counts.divide(totals, axis=0)*100

colors = ['#FF6347','black','#9ACD32','#6495ED']

fig20 = px.bar(percentages,barmode = 'stack',color='Situacao', title='Situação dos alunos por top 10 Bairros',color_discrete_sequence=colors)
fig20.update_layout(yaxis={'title':'Porcentagem'},
                   xaxis={'title': 'Situacao'})

#Forma de Ingresso
counts = df_agrupado.groupby(['Forma_de_ingresso','Situacao']).size()
counts = counts.unstack(level=-1)

totals = counts.sum(axis=1)
percentages = counts.divide(totals, axis=0)*100

colors = ['#FF6347','black','#9ACD32','#6495ED']

fig21 = px.bar(percentages,barmode = 'stack',color='Situacao', title='Situação dos alunos por Forma de ingresso',color_discrete_sequence=colors)
fig21.update_layout(yaxis={'title':'Porcentagem'},
                   xaxis={'title': 'Forma de Ingresso'})

#QuantidadeAlunasMatriculadasENG
df_matricula_engenharia = df_engenharia_novo[(df_engenharia_novo.Sexo=='F')]
df_matricula_engenharia['Matricula'] = df_matricula_engenharia['Matricula'].astype(str)
grafico_matricula_engenharia = df_matricula_engenharia['Matricula'].value_counts().sort_index()
colors = ['#6495ED']
fig22 = px.bar(grafico_matricula_engenharia,barmode = 'stack', title='Quantidade de Alunas matriculadas por Semestre - Engenharia',color_discrete_sequence=colors)
fig22.update_layout(yaxis={'title':'Quantidade de alunas matriculadas'},
                   xaxis={'title': 'Semestre'},showlegend=False)

#SituçãoAlunasENG
df_matricula_engenharia = df_engenharia_novo[(df_engenharia_novo.Sexo=='F')]
df_matricula_engenharia['Matricula'] = df_matricula_engenharia['Matricula'].astype(str)

colors = ['#9ACD32','#FF6347','#6495ED']

counts = df_matricula_engenharia.groupby(['Matricula', 'Situacao']).size()
counts = counts.unstack(level=-1)

totals = counts.sum(axis=1)
percentages = counts.divide(totals, axis=0)*100


fig23 = px.bar(percentages,barmode = 'stack',color='Situacao', title='Situação das alunas por Semestre de Ingresso - Engenharia',color_discrete_sequence=colors)
fig23.update_layout(yaxis={'title':'Porcentagem'},
                   xaxis={'title': 'Semestre'})

#QuantidadeAlunasMatriculadasTEL
df_matricula_telematica = df_telematica_novo[(df_telematica_novo.Sexo=='F')]
df_matricula_telematica['Matricula'] = df_matricula_telematica['Matricula'].astype(str)
grafico_matricula_telematica = df_matricula_telematica['Matricula'].value_counts().sort_index()
colors = ['#6495ED']
fig24 = px.bar(grafico_matricula_telematica,barmode = 'stack', title='Quantidade de Alunas matriculadas por Semestre - Telemática',color_discrete_sequence=colors)
fig24.update_layout(yaxis={'title':'Quantidade de alunas matriculadas'},
                   xaxis={'title': 'Semestre'},showlegend=False)

#SituçãoAlunasTEL
df_matricula_tel = df_telematica_novo[(df_telematica_novo.Sexo=='F')]
df_matricula_tel['Matricula'] = df_matricula_tel['Matricula'].astype(str)

colors = ['black','#9ACD32','#FF6347','#6495ED']

counts = df_matricula_tel.groupby(['Matricula', 'Situacao']).size()
counts = counts.unstack(level=-1)

totals = counts.sum(axis=1)
percentages = counts.divide(totals, axis=0)*100


fig25 = px.bar(percentages,barmode = 'stack',color='Situacao', title='Situação das alunas por Semestre de Ingresso - Telemática',color_discrete_sequence=colors)
fig25.update_layout(yaxis={'title':'Porcentagem'},
                   xaxis={'title': 'Semestre'})
###################################LAYOUT###################################################################
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

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
                        id='quantidade-total',
                        figure=fig2
                    )),style={"width": "100%"},
            ),width=4),
        dbc.Col(
            dbc.Card(
                dbc.CardBody(
                    dcc.Graph(
                        id='quantidade-totaleng',
                        figure=fig5)
                    ),style={"width": "100%"},
        ),width=4),
        dbc.Col(
            dbc.Card(
                dbc.CardBody(
                    dcc.Graph(
                        id='quantidade-totaltel',
                        figure=fig6)
                    ),style={"width": "100%"},
        ),width=4),
    ],style={"width": "100%"}),

    dbc.Row([
        dbc.Col(
            dbc.Card(
                dbc.CardBody(
                    dcc.Graph(
                        id='grafico-situaçãogeral',
                        figure=fig1
                    )),style={"width": "100%"},
            ),width=4),
        dbc.Col(
            dbc.Card(
                dbc.CardBody(
                    dcc.Graph(
                        id='grafico-situaçãoeng',
                        figure=fig3)
                    ),style={"width": "100%"},
        ),width=4),
        dbc.Col(dbc.Card(
                dbc.CardBody(
                    dcc.Graph(
                        id='grafico-situaçãoetel',
                        figure=fig4)
                    ),style={"width": "100%"},
        ),width=4),
    ],style={"width": "100%"}),

    dbc.Row([
        dbc.Col(
            dbc.Card(
                dbc.CardBody(
                    dcc.Graph(
                        id='grafico-tempoconclusaoeng',
                        figure=fig9
                    )),style={"width": "100%"},
            ),width=3),
        dbc.Col(
            dbc.Card(
                dbc.CardBody(
                    dcc.Graph(
                        id='grafico-tempoconclusaotel',
                        figure=fig10)
                    ),style={"width": "100%"},
        ),width=3),
        dbc.Col(
            dbc.Card(
                dbc.CardBody(
                    dcc.Graph(
                        id='grafico-tempoconclusaotel',
                        figure=fig11)
                    ),style={"width": "100%"},
        ),width=3),
        dbc.Col(
            dbc.Card(
                dbc.CardBody(
                    dcc.Graph(
                        id='grafico-tempoconclusaotel',
                        figure=fig12)
                    ),style={"width": "100%"},
        ),width=3)
    ],style={"width": "100%"}),

    dbc.Row([
        dbc.Col(
            dbc.Card(
                dbc.CardBody(
                    dcc.Graph(
                        id='grafico-tempoconclusaoeng',
                        figure=fig13
                    )),style={"width": "100%"},
            ),width=3),
        dbc.Col(
            dbc.Card(
                dbc.CardBody(
                    dcc.Graph(
                        id='grafico-tempoconclusaotel',
                        figure=fig14)
                    ),style={"width": "100%"},
        ),width=3),
        dbc.Col(
            dbc.Card(
                dbc.CardBody(
                    dcc.Graph(
                        id='grafico-tempoconclusaotel',
                        figure=fig15)
                    ),style={"width": "100%"},
        ),width=3),
        dbc.Col(
            dbc.Card(
                dbc.CardBody(
                    dcc.Graph(
                        id='grafico-tempoconclusaotel',
                        figure=fig16)
                    ),style={"width": "100%"},
        ),width=3)
    ],style={"width": "100%"}),

    dbc.Row([
        dbc.Col(
            dbc.Card(
                dbc.CardBody(
                    dcc.Graph(
                        id='naturalidade',
                        figure=fig19
                    )),style={"width": "100%"},
            ),width=4),
        dbc.Col(
            dbc.Card(
                dbc.CardBody(
                    dcc.Graph(
                        id='bairros',
                        figure=fig20)
                    ),style={"width": "100%"},
        ),width=4),
        dbc.Col(
            dbc.Card(
                dbc.CardBody(
                    dcc.Graph(
                        id='ingresso',
                        figure=fig21)
                    ),style={"width": "100%"},
        ),width=4),
    ],style={"width": "100%"}),

    dbc.Row([
        dbc.Col(
            dbc.Card(
                dbc.CardBody(
                    dcc.Graph(
                        id='grafico-tempoconclusaoeng',
                        figure=fig7
                    )),style={"width": "100%"},
            ),width=3),
        dbc.Col(
                dbc.Card(
                    dbc.CardBody(
                        dcc.Graph(
                            id='ghistograma-tempoconclusaoeng',
                            figure=fig17)
                        ),style={"width": "100%"},
            ),width=3),
	    dbc.Col(
            dbc.Card(
                dbc.CardBody(
                    dcc.Graph(
                        id='grafico-tempoconclusaotel',
                        figure=fig8)
                    ),style={"width": "100%"},
        ),width=3),
	    dbc.Col(
                dbc.Card(
                    dbc.CardBody(
                        dcc.Graph(
                            id='ghistograma-tempoconclusaotel',
                            figure=fig18)
                        ),style={"width": "100%"},
            ),width=3)
    ],style={"width": "100%"}),

    dbc.Row([
        dbc.Col(
            dbc.Card(
                dbc.CardBody(
                    dcc.Graph(
                        id='grafico-tempoconclusaoeng',
                        figure=fig22
                    )),style={"width": "100%"},
            ),width=3),
        dbc.Col(
                dbc.Card(
                    dbc.CardBody(
                        dcc.Graph(
                            id='ghistograma-tempoconclusaoeng',
                            figure=fig23)
                        ),style={"width": "100%"},
            ),width=3),
	    dbc.Col(
            dbc.Card(
                dbc.CardBody(
                    dcc.Graph(
                        id='grafico-tempoconclusaotel',
                        figure=fig24)
                    ),style={"width": "100%"},
        ),width=3),
	    dbc.Col(
                dbc.Card(
                    dbc.CardBody(
                        dcc.Graph(
                            id='ghistograma-tempoconclusaotel',
                            figure=fig25)
                        ),style={"width": "100%"},
            ),width=3)
    ],style={"width": "100%"})
    
],style={"width": "100%"})

if __name__ == '__main__':
	app.run_server(debug=True)
