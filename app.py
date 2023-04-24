import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
from pages import index,perfilgeral,perfilevadidos,resultado_forms

app = dash.Dash(__name__, use_pages=True,external_stylesheets=[dbc.themes.LUX],suppress_callback_exceptions=True)

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div([
        dbc.NavbarSimple(
            children=[
                dbc.NavItem(dbc.NavLink("Dados Gerais", href="/")),
                dbc.NavItem(dbc.NavLink("Perfil Geral", href="/perfilgeral")),
                dbc.NavItem(dbc.NavLink("Perfil Evadido", href="/perfilevadidos")),
                dbc.NavItem(dbc.NavLink("Resultado Forms", href="/resultadoforms"))
            ] ,
            brand="Evasão Escolar em Cursos Superiores da Área de TI: Um Estudo de Caso no IFPB ",
            brand_href="/",
            color="#6495ED",
            dark=True,
        ), 
    ]), 
    html.Div(id='page-content', children=[]), 
])

@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/':
        return index.layout
    if pathname == '/perfilgeral':
        return perfilgeral.layout
    if pathname == '/perfilevadidos':
        return perfilevadidos.layout
    if pathname == '/resultadoforms':
        return resultado_forms.layout
    else:
        return "404 Page Error! Please choose a link"

if __name__ == "__main__":
    app.run(debug=True)