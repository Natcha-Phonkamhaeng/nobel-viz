import dash
from dash import Dash, html, Output, Input, dcc, callback
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import dash_ag_grid as dag

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.LUX],
		meta_tags=[{'name': 'viewport','content': 'width=device-width, initial-scale=1.0, maximum-scale=1.2, minimum-scale=0.5,'}])

server = app.server

df = pd.read_csv('data/nobel.csv')

color_mapping = {
	'medicine': 'limegreen',
	'physics': 'darkkhaki',
	'chemistry': 'goldenrod',
	'peace': 'darkslategray',
	'literature': 'darkviolet',
	'economics': 'darkcyan',
	'male':'royalblue',
	'female':'	fuchsia',
	'org': 'silver',
}

columnDefs = [
	{'field': 'nobel year'},
	{'field': 'firstname'},
	{'field': 'lastname'},
	{'field': 'category'},
	{'field': 'motivation'},
	{'field': 'gender'},
	{'field': 'age'},
	{'field': 'birth_country'},
]

def figMap():
	# world map of country category
	dfMap = df.groupby(['alpha-3','birth_country']).size().reset_index(name='count')
	figMap = px.choropleth(dfMap, locations='alpha-3', color='count', hover_name='birth_country')
	figMap.update_layout(paper_bgcolor='rgb(248,248,255)')
	return figMap

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
		]),
	dbc.Row([
		dbc.Col([
			dbc.Card([
				dbc.CardBody([
					dbc.Row([
						dbc.Col([
							html.H3(['Country']),
							html.Label(['Based on birth country'])
							])
						]),
					html.Hr(),
					dbc.Row([
						dbc.Col([
							html.P(['Country']),
							dcc.Dropdown(options=sorted([x for x in df['birth_country'].unique()], key=lambda x: (str(type(x)), x))[1:], 
										id='dropdown-country')
							], width=4)
						]),
					html.Br(),
					dbc.Row([
						dbc.Col([
							dcc.Graph(figure=figMap(), id='country-map'),
							html.Br(),
							dag.AgGrid(
								id='grid-table', 
								rowData=df.to_dict('records'), 
								columnDefs=columnDefs,
								defaultColDef={"resizable": True, "sortable": True, "filter": True, "minWidth":115},
								dashGridOptions={"pagination": True, "paginationPageSize":8, "domLayout": "autoHeight"},
								)
							])
						])
					])
				],
				class_name='bg-card mb-5'
				)
			])
		])
	])

# callback for Category
@callback(
	Output('gender-fig', 'figure'),
	Output('cat-sun', 'figure'),
	Output('cat-fig', 'figure'),
	Input('dropdown_year', 'value')
	)
def update_graph(select_year):
	dff = df.copy()

	#------------------------- Graph on Gender #-------------------------
	dfGroup = df.groupby(['nobel year', 'category', 'gender']).size().reset_index(name='count')
	fig = px.histogram(dfGroup, x="nobel year", y='count', color="gender",
                   marginal="rug", # or violin, rug
                   hover_data=dfGroup.columns, labels={'count': 'Count of Gender'}).update_layout(yaxis_title='Count of Gender', paper_bgcolor='#F8F8FF')
	
	#------------------------- Graph on Category #-------------------------
	# Sun burst chart
	figSun = px.sunburst(dff, path=['category', 'gender']).update_layout(margin=dict(l=0, r=0, t=0, b=0),paper_bgcolor='#F8F8FF')
	figSun.update_traces(marker_colors=[color_mapping[cat] for cat in figSun.data[-1].labels])
	# bar chart
	dffGroup = dff.groupby(['nobel year', 'category']).size().reset_index(name='count')
	fig2 = px.histogram(dffGroup, x='nobel year', y='count', color='category', barmode='group',
			labels={'count': 'Number of Nobel Prize Received'},
			color_discrete_map=color_mapping)
	fig2.update_layout(yaxis_title='Number of Nobel Prize Received',paper_bgcolor='#F8F8FF')
	
	if select_year:
		# update sunburst chart
		figSun = px.sunburst(dff[dff['nobel year'] == select_year], path=['category', 'gender']).update_layout(margin=dict(l=0, r=0, t=0, b=0),paper_bgcolor='#F8F8FF')
		figSun.update_traces(marker_colors=[color_mapping[cat] for cat in figSun.data[-1].labels])
		# update barchart
		mark = (dffGroup['nobel year'] == select_year)
		fig2 = px.histogram(dffGroup[mark], x='nobel year', y='count', color='category', barmode='group',
				labels={'count': 'Number of Nobel Prize Received'},
				color_discrete_map=color_mapping)
		fig2.update_layout(yaxis_title='Number of Nobel Prize Received',paper_bgcolor='#F8F8FF')
		fig2.update_xaxes(visible=False)
		return fig, figSun, fig2
	else:
		return fig, figSun, fig2

#callback for Country
@callback(
	Output('grid-table', 'rowData'),
	Input('dropdown-country', 'value')
	)
def update_map(select_country):
	dff = df.copy()

	if select_country:
		mask = (dff['birth_country'] == select_country)
		dff = dff[mask]
		return dff.to_dict('records')
	else:
		return dff.to_dict('records')

if __name__ == '__main__':
    app.run_server(debug=True)
