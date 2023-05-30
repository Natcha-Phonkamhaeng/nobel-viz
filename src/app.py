import dash
from dash import Dash, html, Output, Input, dcc, callback
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.QUARTZ])

# server = app.server

df = pd.read_csv('data/nobel.csv')

df = df.groupby(['nobel year', 'gender']).size().to_frame(name='count').reset_index()
fig = px.line(df, x='nobel year', y='count', color='gender')



navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Page 1", href="#")),
        dbc.DropdownMenu(
            children=[
                # dbc.DropdownMenuItem("More pages", header=True),
                dbc.DropdownMenuItem("Page 2", href="#", id='page-2'),
                dbc.DropdownMenuItem("Page 3", href="#", id='page-3'),
            ],
            nav=True,
            in_navbar=True,
            label="More",
        ),
    ],
    brand="NavbarSimple",
    brand_href="#",
    color="primary",
    dark=True,
)

container_style = {
	'margin-left': '0rem',
	'margin-right': '0rem',
}

app.layout = html.Div([
	navbar,
	dbc.Container([
		dbc.Row([
			dbc.Col([
				dcc.Graph(figure=fig, id='my-graph')
				])
			])
		],
		style=container_style)
	])


@app.callback(
    Output('my-graph', "figure"),
    Input('page-2', 'n_clicks'),
    Input('page-3', 'n_clicks'),
    prevent_initial_update=True
)
def update_label(n2, n3):
    # use a dictionary to map ids back to the desired label
    # makes more sense when there are lots of possible labels
	dff = px.data.tips()
	wide_df = px.data.medals_wide()

	ctx = dash.callback_context

	if not ctx.triggered:
		
		# button_id = ctx.triggered[0]['prop_id'].split('.')[0]
		return fig
	elif ctx.triggered:
		button_id = ctx.triggered[0]['prop_id'].split('.')[0]
		print(button_id)
		if button_id == 'page-2':
			fig2 = px.pie(dff, values='tip', names='day')
			# button_id = ctx.triggered[0]['prop_id'].split('.')[0]
			# print(button_id)
			return fig2
		if button_id == 'page-3':
			fig3 = px.bar(wide_df, x="nation", y=["gold", "silver", "bronze"], title="Wide-Form Input")
			return fig3
	




if __name__ == '__main__':
    app.run_server(debug=True)
























