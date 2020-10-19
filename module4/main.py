import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import data_collect as dc
import plotly.graph_objs as go
import numpy as np
import pandas as pd
import plotly.express as px

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
all_tree_data = dc.get_all_tree_data()

df_totals = all_tree_data.groupby(['borocode', 'spc_common'])['count_tree_id'].sum()
df_total_by_borocode_specie_health = all_tree_data.groupby(['borocode', 'spc_common', 'health'])['count_tree_id'].sum()
df_totals = df_totals.reset_index(drop=False)
df_total_by_borocode_specie_health = df_total_by_borocode_specie_health.reset_index(drop=False)
df_totals.columns = ['borocode', 'spc_common', 'total_for_specie_in_borough']
df_total_by_borocode_specie_health.columns = ['borocode', 'spc_common', 'health', 'total']
tree_proportions = pd.merge(df_total_by_borocode_specie_health, df_totals, on=['borocode', 'spc_common'])
tree_proportions['ratio'] = tree_proportions['total']/ tree_proportions['total_for_specie_in_borough']
tree_proportions['spc_common'] = tree_proportions['spc_common'].apply(lambda x: x.title())

species = np.sort(tree_proportions.spc_common.unique())


borough_index = {1:'Manhattan', 2: 'Bronx', 3: 'Brooklyn', 4:'Queens', 5: 'Staten Island'}
tree_proportions['boroname'] = tree_proportions['borocode'].map(borough_index)
borough_list = np.sort(tree_proportions.boroname.unique())

health_index = {'Poor':1, 'Fair':2, 'Good':3}
# create columns that specify tree health
all_data2 = all_tree_data
all_data2['health_level'] = all_data2['health'].map(health_index)
all_data2[['steward']] = all_data2[['steward']].apply(lambda x: pd.factorize(x)[0])
all_data2['boroname'] = all_data2['borocode'].map(borough_index)


app.layout = html.Div([
    html.H2('Question 1:'),
    html.H4('Select Tree Specie'),

    dcc.Dropdown(
        id='specie',
        options=[{'label': i, 'value': i} for i in species],
        value="'Schubert' Chokecherry",
        style={'height': 'auto', 'width': '300px'}
    ),

    dcc.Graph(id='graph-ratio'),

    html.H2('Question 2:'),
    html.H4('Select borough'),

    dcc.Dropdown(
        id='borough',
        options=[{'label': i, 'value': i} for i in borough_list],
        value='Bronx',
        style={'height': 'auto', 'width': '300px'}
    ),
    dcc.Graph(id='Health by Steward')

], style={'columnCount': 1})


# Display Proportion Graph
@app.callback(
    Output('graph-ratio', 'figure'),
    [Input('specie', 'value')])
def update_figure(selected_specie):
    filtered_df = tree_proportions[tree_proportions.spc_common == selected_specie]
    manhattan = filtered_df[filtered_df.borocode == 1]
    bronx = filtered_df[filtered_df.borocode == 2]
    brooklyn = filtered_df[filtered_df.borocode == 3]
    queens = filtered_df[filtered_df.borocode == 4]
    staten_island = filtered_df[filtered_df.borocode == 5]

    traces = []

    traces.append(go.Bar(
        x=queens['health'],
        y=queens['ratio'],
        name='Queens',
        opacity=0.9
    ))

    traces.append(go.Bar(
        x=manhattan['health'],
        y=manhattan['ratio'],
        name='Manhattan',
        opacity=0.9
    ))

    traces.append(go.Bar(
        x=bronx['health'],
        y=bronx['ratio'],
        name='Bronx',
        opacity=0.9
    ))

    traces.append(go.Bar(
        x=brooklyn['health'],
        y=brooklyn['ratio'],
        name='Brooklyn',
        opacity=0.9
    ))

    traces.append(go.Bar(
        x=staten_island['health'],
        y=staten_island['ratio'],
        name='Staten Island',
        opacity=0.9
    ))

    return {
        'data': traces,
        'layout': go.Layout(
            xaxis={'title': 'Health of Trees'},
            yaxis={'title': 'Proportion of Trees in Borough'},
            margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
            legend=dict(x=-.1, y=1.2)
        )
    }

@app.callback(
    Output('Health by Steward', 'figure'),
    [Input('borough', 'value')])
def steward_graph(input_data):
    df = all_data2[all_data2.boroname == input_data]
    fig = px.histogram(df, x=['health_level'], y=df['steward'])
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
