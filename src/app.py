import dash
from dash import Dash, html, Output, Input, dcc, callback
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.LUX],
		meta_tags=[{'name': 'viewport','content': 'width=device-width, initial-scale=1.0, maximum-scale=1.2, minimum-scale=0.5,'}])

# server = app.server

df = pd.read_csv('data/nobel.csv')
dff = df.groupby(['nobel year', 'category', 'gender']).size().reset_index(name='count')
fig = px.histogram(dff, x="nobel year", y='count', color="gender",
                   marginal="rug", # or violin, rug
                   hover_data=dff.columns, labels={'count': 'Count of Gender'}).update_layout(yaxis_title='Count of Gender', paper_bgcolor='#F8F8FF')

figSun = px.sunburst(df, path=['category', 'gender']).update_layout(margin=dict(l=0, r=0, t=0, b=0),paper_bgcolor='#F8F8FF')

fig2 = px.histogram(dff, x="nobel year", y='count', color="category",
                   marginal="rug", # or violin, rug
                   hover_data=dff.columns)

app.layout = dbc.Container([
	dbc.Row([
		dbc.Col([
			html.H1(['The Nobel Prize'])
			])
		],
		class_name='mt-3 mb-2'
		),
	dbc.Row([
		dbc.Col([
			dbc.Card([
				dbc.CardBody([
					dbc.Row([
						dbc.Col([
							html.H3(['Gender'])
							]),
						]),
					html.Hr(),
					dbc.Row([
						dbc.Col([
							dcc.Graph(figure=fig, id='gender-fig')
							])
						])
					])
				],
				class_name='bg-card mb-5'
				),
			dbc.Card([
				dbc.CardBody([
					dbc.Row([
						dbc.Col([
							html.H3(['Gender and Category'])
							])
						]),
					html.Hr(),
					dbc.Row([
						dbc.Col([
							html.P(['Year']),
							dcc.Dropdown(options=['1990', '1991', '1992']),
							html.P(['Category'], className='mt-3'),
							dcc.Dropdown(options=['Physic', 'Medical'])
							], width=2),
						dbc.Col([
							dcc.Graph(figure=figSun, id='cate-sun')
							], width=3),
						dbc.Col([
							dcc.Graph(figure=fig2, id='cate-fig')
							], width=7)
						])
					])
				],
				class_name='bg-card mb-5'
				)
			])
		])
	])
	


if __name__ == '__main__':
    app.run_server(debug=True)
