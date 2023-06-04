import dash
from dash import Dash, html, Output, Input, dcc, callback
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.LUX],
		meta_tags=[{'name': 'viewport','content': 'width=device-width, initial-scale=1.0, maximum-scale=1.2, minimum-scale=0.5,'}])

# server = app.server

df = pd.read_csv('data/nobel.csv')


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
							dcc.Graph(id='gender-fig')
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
							html.H3(['Category'])
							])
						]),
					html.Hr(),
					dbc.Row([
						dbc.Col([
							html.P(['Year']),
							dcc.Dropdown(options=[x for x in df['nobel year'].unique()], id='dropdown_year'),
							html.P(['Category'], className='mt-3'),
							dcc.Dropdown(options=[x for x in df['category'].unique()], id='dropdown_cat')
							], width=2),
						dbc.Col([
							dcc.Graph(figure={}, id='cat-sun')
							], width=3),
						dbc.Col([
							dcc.Graph(figure={}, id='cat-fig')
							], width=7)
						])
					])
				],
				class_name='bg-card mb-5'
				)
			])
		])
	])
	
@callback(
	Output('gender-fig', 'figure'),
	Output('cat-sun', 'figure'),
	Output('cat-fig', 'figure'),
	Input('dropdown_year', 'value'),
	Input('dropdown_cat', 'value')
	)
def update_graph(select_year, select_cat):
	dff = df.copy()

	#------------------------- Graph on Gender #-------------------------
	dfGroup = df.groupby(['nobel year', 'category', 'gender']).size().reset_index(name='count')
	fig = px.histogram(dfGroup, x="nobel year", y='count', color="gender",
                   marginal="rug", # or violin, rug
                   hover_data=dfGroup.columns, labels={'count': 'Count of Gender'}).update_layout(yaxis_title='Count of Gender', paper_bgcolor='#F8F8FF')
	
	#------------------------- Graph on Category #-------------------------
	dffGroup = dff.groupby(['nobel year', 'category']).size().reset_index(name='count')
	figSun = px.sunburst(dff, path=['category', 'gender']).update_layout(margin=dict(l=0, r=0, t=0, b=0),paper_bgcolor='#F8F8FF')
	fig2 = px.histogram(dffGroup, x='nobel year', y='count', color='category', barmode='group', labels={'count': 'Number of Nobel Prize Received'})
	fig2.update_layout(yaxis_title='Number of Nobel Prize Received')
	
	if select_year:
		mark = (dffGroup['nobel year'] == select_year)
		fig2 = px.histogram(dffGroup[mark], x='nobel year', y='count', color='category', barmode='group', labels={'count': 'Number of Nobel Prize Received'})
		fig2.update_layout(yaxis_title='Number of Nobel Prize Received')
		fig2.update_xaxes(visible=False)
		return fig, figSun, fig2
	else:
		return fig, figSun, fig2


if __name__ == '__main__':
    app.run_server(debug=True)
