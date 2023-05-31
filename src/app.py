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
fig = px.line(dfGroup, x='nobel year', y='count', color='gender')
fig.update_layout(
			font=dict(color='white'), 
			margin=dict(l=0, r=0, t=40, b=3),
			paper_bgcolor='rgba(0,0,0,0)',)
            #plot_bgcolor='rgb(0,0,0,0)')

#-------------- For Sunburst Chart -----------------------------------------
fig2 = px.sunburst(df, path=['category', 'gender'])
fig2.update_layout(title='Proportion of Gender',
			font=dict(color='white'), 
			margin=dict(l=0, r=0, t=40, b=3),
			paper_bgcolor='rgba(0,0,0,0.3)',
            plot_bgcolor='rgb(255,255,255)')

#-------------- For Choropeth Map -----------------------------------------
dfChoro = df.groupby(['alpha-3','birth_country']).size().reset_index(name='count')
figChoro = px.choropleth(dfChoro, locations='alpha-3', color='count', hover_name='birth_country')
#figChoro.update_geos(fitbounds="locations", visible=True)
figChoro.update_layout(margin={"r":0,"t":0,"l":0,"b":0}, geo=dict(bgcolor= 'rgba(0,0,0,0)'), paper_bgcolor='rgba(0,0,0,0.1)',)
figChoro.update_traces(marker_line_width=0)

#--------------------------------------------------------------------------

navbar = dbc.NavbarSimple(
    children=[
        #dbc.NavItem(dbc.NavLink("Page 1", href="#")),
        dbc.DropdownMenu(
            children=[
                dbc.DropdownMenuItem("All", href="#", id='page-1'),
                dbc.DropdownMenuItem("Page 2", href="#", id='page-2'),
                dbc.DropdownMenuItem("Page 3", href="#", id='page-3'),
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
					dcc.Graph(figure=fig2, id='my-pie', style={'width': '40vh', 'height': '40vh'})
				], style={'width': '50vh', 'height': '50vh'}, xs=10, sm=5, md=5, lg=6, xl=5),			
			dbc.Col([
				
				])
			], class_name='g-0'),
		dbc.Row([
			dbc.Col([
				dcc.Graph(figure=fig, id='my-graph')
				])
			])
		])
	])
	

@app.callback(
    Output('my-graph', "figure"),
    Input('page-1', 'n_clicks'),
    Input('page-2', 'n_clicks'),
    Input('page-3', 'n_clicks'),
    prevent_initial_update=True
)
def update_label(n1, n2, n3):
	dff = px.data.tips()
	wide_df = px.data.medals_wide()

	ctx = dash.callback_context

	if not ctx.triggered:
		
		# button_id = ctx.triggered[0]['prop_id'].split('.')[0]
		return figChoro
	elif ctx.triggered:
		button_id = ctx.triggered[0]['prop_id'].split('.')[0]
		#print(button_id)
		if button_id == 'page-2':
			fig2 = px.pie(dff, values='tip', names='day')
			# button_id = ctx.triggered[0]['prop_id'].split('.')[0]
			# print(button_id)
			return fig
		if button_id == 'page-3':
			fig3 = px.bar(wide_df, x="nation", y=["gold", "silver", "bronze"], title="Wide-Form Input")
			return fig3
		else:
			return figChoro
	

if __name__ == '__main__':
    app.run_server(debug=True)
