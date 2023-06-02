import dash
from dash import Dash, html, Output, Input, dcc, callback
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.QUARTZ],
		meta_tags=[{'name': 'viewport','content': 'width=device-width, initial-scale=1.0, maximum-scale=1.2, minimum-scale=0.5,'}])

# server = app.server

df = pd.read_csv('data/nobel.csv')

#-------------- For Line Chart -----------------------------------------
dfGroup = df.groupby(['nobel year', 'gender']).size().to_frame(name='count').reset_index()
figLine = px.line(dfGroup, x='nobel year', y='count', color='gender', labels={'count': 'Numbers for Nobel Prize'})
figLine.update_layout(
			font=dict(color='white'), 
			margin=dict(l=0, r=0, t=40, b=3),
			paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(255,255,255,0.5)')

#-------------- For Sunburst Chart -----------------------------------------
figSun = px.sunburst(df, path=['category', 'gender'])
figSun.update_layout(font=dict(color='white'), 
			margin=dict(l=0, r=0, t=0, b=0),
			paper_bgcolor='rgba(0,0,0,0)',) # making eges transparent
            #plot_bgcolor='rgb(255,255,255)')
figSun.update_traces(marker_line_color='rgba(255,0,255,0.3)') # set the color border

#-------------- For Choropeth Map -----------------------------------------
dfChoro = df.groupby(['alpha-3','birth_country']).size().reset_index(name='count')
figChoro = px.choropleth(dfChoro, locations='alpha-3', color='count', hover_name='birth_country')
#figChoro.update_geos(fitbounds="locations", visible=True)
figChoro.update_layout(margin={"r":0,"t":0,"l":0,"b":0}, geo=dict(bgcolor= 'rgba(0,0,0,0)'), paper_bgcolor='rgba(0,0,0,0)',)
#figChoro.update_traces(marker_line_width=0)

#--------------------------------------------------------------------------

navbar = dbc.NavbarSimple(
    children=[
        #dbc.NavItem(dbc.NavLink("Page 1", href="#")),
        dbc.DropdownMenu(
            children=[
                dbc.DropdownMenuItem("All", href="#", id='all'),
                dbc.DropdownMenuItem("Physics", href="#", id='physics'),
                dbc.DropdownMenuItem("Chemistry", href="#", id='chemistry'),
                dbc.DropdownMenuItem("Peace", href="#", id='peace'),
                dbc.DropdownMenuItem("Literature", href="#", id='literature'),
                dbc.DropdownMenuItem("Economics", href="#", id='economics'),
                dbc.DropdownMenuItem("Medicine", href="#", id='medicine'),
            ],
            nav=True,
            in_navbar=True,
            label="Category",
        ),
    ],
    brand="The Nobel Prize",
    brand_href="#",
    color="primary",
    dark=True,
    class_name='mb-2',
)

container_style = {
	'margin-left': '0rem',
	#'margin-right': '0rem',
}

app.layout = html.Div([
	navbar,
	dbc.Container([
		dbc.Row([
			dbc.Col([
				dcc.Graph(figure=figSun, id='my-sun')
				], width=3),			
			dbc.Col([
				dcc.Graph(figure=figLine, id='my-graph2')
				], width=9)
			], class_name='mb-3'),
		dbc.Row([
			dbc.Col([
				dcc.Graph(figure=figChoro, id='my-graph3')
				])
			])
		])
	])
	

@app.callback(
    Output('my-sun', "figure"),
    Output('my-graph2', 'figure'),
    Output('my-graph3', 'figure'),
    Input('all', 'n_clicks'),
    Input('physics', 'n_clicks'),
    Input('chemistry', 'n_clicks'),
    Input('peace', 'n_clicks'),
    Input('literature', 'n_clicks'),
    Input('economics', 'n_clicks'),
    Input('medicine', 'n_clicks'),
    prevent_initial_update=True
)
def update_label(n_all, n_physics, n_chem, n_peace, n_lite, n_econ, n_med):
	ctx = dash.callback_context

	if not ctx.triggered:
		
		return figSun, figLine, figChoro
	elif ctx.triggered:
		button_id = ctx.triggered[0]['prop_id'].split('.')[0]
		#print(button_id)
		if button_id == 'physics':
			
			# button_id = ctx.triggered[0]['prop_id'].split('.')[0]
			# print(button_id)
			return figSun, figLine, figChoro
		if button_id == 'chemistry':
			data_canada = px.data.gapminder().query("country == 'Canada'")
			figBar = px.bar(data_canada, x='year', y='pop')
			
			return figSun, figLine, figBar
		else:
			return figSun, figLine, figChoro
	

if __name__ == '__main__':
    app.run_server(debug=True)
