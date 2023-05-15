import pandas as pd
import numpy as np

from dash import Dash, html, dcc, callback, Output, Input
import dash_bootstrap_components as dbc

import plotly.express as px
import plotly.graph_objects as go

colorScheme = ['#212529', '#343A40', '#495057', '#6C757D', '#ADB5BD', '#F8F9FA', '#E9ECEF', '#DEE2E6', '#CED4DA']
colorScheme2 = ['#71093B', '#023578', '#990B52', '#CB8B15', '#FFFFFF', '#EAAA34', '#F1F4F9', '#749ED2', '#022450', '#467EC3']

data_source = r"https://github.com/TatKhachatryan/Messi-Dashboard/blob/3704653279ea2720e5606223efead05217940613/messi_starplayerstats.xlsx?raw=true"

all_time_games = pd.read_excel(data_source, engine="openpyxl", sheet_name='all_time_games')
all_time_goals = pd.read_excel(data_source, engine="openpyxl", sheet_name='all_time_goals')
first_goal_of_the_game = pd.read_excel(data_source, engine="openpyxl", sheet_name='first_goal_of_the_game')
last_goal_of_the_game = pd.read_excel(data_source, engine="openpyxl", sheet_name='last_goal_of_the_game')
first_goal_of_the_team = pd.read_excel(data_source, engine="openpyxl", sheet_name='first_goal_of_the_team')
Camp_Nou_goals = pd.read_excel(data_source, engine="openpyxl", sheet_name='Camp_Nou_goals')
wins = pd.read_excel(data_source, engine="openpyxl", sheet_name='wins')
draws = pd.read_excel(data_source, engine="openpyxl", sheet_name='draws')
loses = pd.read_excel(data_source, engine="openpyxl", sheet_name='loses')
assists_to = pd.read_excel(data_source, engine="openpyxl", sheet_name='assists_to')
assists_from = pd.read_excel(data_source, engine="openpyxl", sheet_name='assists_from')
opponents = pd.read_excel(data_source, engine="openpyxl", sheet_name='opponents')

# get rid of the last unnecessary column
# all_time_games = all_time_games[all_time_games.columns[:-1]]
# all_time_goals = all_time_goals[all_time_goals.columns[:-1]]
# first_goal_of_the_game = first_goal_of_the_game[first_goal_of_the_game.columns[:-1]]
# last_goal_of_the_game = last_goal_of_the_game[last_goal_of_the_game.columns[:-1]]
# first_goal_of_the_team = first_goal_of_the_team[first_goal_of_the_team.columns[:-1]]
# last_goal_of_the_team = last_goal_of_the_team[last_goal_of_the_team.columns[:-1]]
# game_decider = game_decider[game_decider.columns[:-1]]
# stoppage_time_goals = stoppage_time_goals[stoppage_time_goals.columns[:-1]]
# Camp_Nou_goals = Camp_Nou_goals[Camp_Nou_goals.columns[:-1]]
# wins = wins[wins.columns[:-1]]
# draws = draws[draws.columns[:-1]]
# loses = loses[loses.columns[:-1]]
# assists_to = assists_to[assists_to.columns[:-1]]
# assists_from = assists_from[assists_from.columns[:-1]]
# opponents = opponents[opponents.columns[:-1]]

# change column names to convenient names
all_time_games.columns = ['#', 'Date', 'Competition', 'Home team', 'Result', 'Away team', 'Lineup', 'Minutes', 'Goals', 'Assists', 'Cards', 'Jersey']
all_time_goals.columns = ['#', 'Date', 'Competition', 'Home team',  'Result', 'Away team', 'Minute', 'Score', 'What', 'How', 'Jersey']
first_goal_of_the_game.columns = ['#', 'Date', 'Competition', 'Home team',  'Result', 'Away team', 'Minute', 'Score', 'What', 'How', 'Jersey']
last_goal_of_the_game.columns = ['#', 'Date', 'Competition', 'Home team',  'Result', 'Away team', 'Minute', 'Score', 'What', 'How', 'Jersey']
first_goal_of_the_team.columns = ['#', 'Date', 'Competition', 'Home team',  'Result', 'Away team', 'Minute', 'Score', 'What', 'How', 'Jersey']
Camp_Nou_goals.columns = ['#', 'Date', 'Competition', 'Home team', 'Result', 'Away team', 'Lineup', 'Minutes', 'Goals', 'Assists', 'Cards']
wins.columns = ['#', 'Date', 'Competition', 'Home team', 'Result', 'Away team', 'Lineup', 'Minutes', 'Goals', 'Assists', 'Cards', 'Jersey']
draws.columns = ['#', 'Date', 'Competition', 'Home team', 'Result', 'Away team', 'Lineup', 'Minutes', 'Goals', 'Assists', 'Cards', 'Jersey']
loses.columns = ['#', 'Date', 'Competition', 'Home team', 'Result', 'Away team', 'Lineup', 'Minutes', 'Goals', 'Assists', 'Cards', 'Jersey']
assists_to.columns = ['#', 'Date', 'Competition', 'Home', 'Result', 'Away', 'Minute', 'Assist on', 'Score']
assists_from.columns = ['#', 'Date', 'Competition', 'Home', 'Result', 'Away', 'Minute', 'Assist on', 'Score']
opponents.columns = ['#', 'Opponents', 'Country', 'Games', 'Wins', 'Draws', 'Defeats', 'Winning percentage',
                     'Goals', 'Coefficient', 'Assists', 'Cards', 'Penalties', 'Penalties missed']


# convert Date to datetime
all_time_games['Date'] = pd.to_datetime(all_time_games['Date'])
# set team names
all_time_games['Team'] = np.where((all_time_games['Home team']=='Paris Saint-Germain') | (all_time_games['Away team']=='Paris Saint-Germain'), "Paris Saint-Germain",
                                  np.where(((all_time_games['Home team']=='FC Barcelona') | (all_time_games['Away team']=='FC Barcelona')),"FC Barcelona", "Argentina"))

# set seasons
all_time_games['Year'] = all_time_games['Date'].dt.year
all_time_games['Season'] = np.where(all_time_games['Year']==2023, '2022-23',
                           np.where(all_time_games['Year']==2022, '2021-22',
                           np.where(all_time_games['Year']==2021, '2020-21',
                           np.where(all_time_games['Year']==2020, '2019-20',
                           np.where(all_time_games['Year']==2019, '2018-19',
                           np.where(all_time_games['Year']==2018, '2017-18',
                           np.where(all_time_games['Year']==2017, '2016-17',
                           np.where(all_time_games['Year']==2016, '2015-16',
                           np.where(all_time_games['Year']==2015, '2014-2015',
                           np.where(all_time_games['Year']==2014, '2013-14',
                           np.where(all_time_games['Year']==2013, '2012-13',
                           np.where(all_time_games['Year']==2012, '2011-12',
                           np.where(all_time_games['Year']==2011, '2010-11',
                           np.where(all_time_games['Year']==2010, '2009-10',
                           np.where(all_time_games['Year']==2009, '2008-09',
                           np.where(all_time_games['Year']==2007, '2006-07',
                           np.where(all_time_games['Year']==2006, '2005-06', '2004-05')))))))))))))))))

all_time_goals['Date'] = pd.to_datetime(all_time_goals['Date'])
all_time_goals['What']= all_time_goals['What'].replace({'': 'Blank'})
# set team names
all_time_goals['Team'] = np.where((all_time_goals['Home team']=='Paris Saint-Germain') | (all_time_goals['Away team']=='Paris Saint-Germain'), "Paris Saint-Germain",
                                  np.where(((all_time_goals['Home team']=='FC Barcelona') | (all_time_goals['Away team']=='FC Barcelona')),"FC Barcelona", "Argentina"))

# set seasons
all_time_goals['Year'] = all_time_goals['Date'].dt.year
all_time_goals['Season'] = np.where(all_time_goals['Year']==2023, '2022-23',
                           np.where(all_time_goals['Year']==2022, '2021-22',
                           np.where(all_time_goals['Year']==2021, '2020-21',
                           np.where(all_time_goals['Year']==2020, '2019-20',
                           np.where(all_time_goals['Year']==2019, '2018-19',
                           np.where(all_time_goals['Year']==2018, '2017-18',
                           np.where(all_time_goals['Year']==2017, '2016-17',
                           np.where(all_time_goals['Year']==2016, '2015-16',
                           np.where(all_time_goals['Year']==2015, '2014-2015',
                           np.where(all_time_goals['Year']==2014, '2013-14',
                           np.where(all_time_goals['Year']==2013, '2012-13',
                           np.where(all_time_goals['Year']==2012, '2011-12',
                           np.where(all_time_goals['Year']==2011, '2010-11',
                           np.where(all_time_goals['Year']==2010, '2009-10',
                           np.where(all_time_goals['Year']==2009, '2008-09',
                           np.where(all_time_goals['Year']==2007, '2006-07',
                           np.where(all_time_goals['Year']==2006, '2005-06', '2004-05')))))))))))))))))

# convert Date to datetime
assists_to['Date'] = pd.to_datetime(assists_to['Date'])
# set team names
assists_to['Team'] = np.where((assists_to['Home']=='Paris Saint-Germain') | (assists_to['Away']=='Paris Saint-Germain'), "Paris Saint-Germain",
                                  np.where(((assists_to['Home']=='FC Barcelona') | (assists_to['Away']=='FC Barcelona')),"FC Barcelona", "Argentina"))

# convert Date to datetime
assists_from['Date'] = pd.to_datetime(assists_from['Date'])
# set team names
assists_from['Team'] = np.where((assists_from['Home']=='Paris Saint-Germain') | (assists_from['Away']=='Paris Saint-Germain'), "Paris Saint-Germain",
                                  np.where(((assists_from['Home']=='FC Barcelona') | (assists_from['Away']=='FC Barcelona')),"FC Barcelona", "Argentina"))


# sort by most scored games
opponents = opponents.sort_values(by='Goals', ascending=False, ignore_index=True)
opponents['Winning %'] = (opponents['Wins']/opponents['Games'])*100


date = '12-05-2023'

# set values for cards blocks
total_games = all_time_games.shape[0]
total_wins = wins.shape[0]
total_draws = draws.shape[0]
total_lost = loses.shape[0]
red_cards = 3
yellow_cards = all_time_games['Cards'].sum()-red_cards


# goals_what
goals_what = all_time_goals.groupby(['Team', 'Season', 'What'])['What'].count().rename('Count').to_frame()
goals_what = goals_what.reset_index()
goals_what = goals_what.sort_values(by='Count', ascending=True)

# left foot / right foot etc.
goals_how = all_time_goals.groupby(['Team', 'Season', 'How'])['How'].count().rename('Count').to_frame()
goals_how = goals_how.reset_index()
goals_how = goals_how.sort_values(by='Count', ascending=True)


# left or rigth side of the cards
teams = all_time_games.groupby(['Team'])['Team'].count().rename('Count').to_frame()
teams = teams.reset_index()
teams = teams.sort_values(by='Count', ascending=False)
fig1 = px.bar(teams, x='Count', y='Team', color='Team', orientation='h',
              color_discrete_sequence=['#DB0030', '#43A1D5', '#004170'],
              text_auto='.2s',
              title='Total Games Played in Teams')

fig1.update_layout(legend=dict(yanchor="bottom", y=0.05, xanchor="right", x=0.99),
                   yaxis = dict(showticklabels=False))


competitions = all_time_games.groupby(['Competition', 'Team'])['Competition'].count().rename('Count').to_frame()
competitions = competitions.reset_index()
competitions['Competition'] = competitions['Competition'].replace({'CPA Copa América 2007': 'Copa América',
                                                            'CPA Copa América 2011': 'Copa América',
                                                            'CPA Copa América 2015': 'Copa América',
                                                            'CPA Copa América 2019': 'Copa América',
                                                            'CPA Copa América 2021': 'Copa América',
                                                            'CPA Copa América Centenario': 'Copa América',
                                                            'WCQ World Cup 2006 Qualification': 'World Cup Qualification',
                                                            'WCQ World Cup 2010 Qualification': 'World Cup Qualification',
                                                            'WCQ World Cup 2014 Qualification': 'World Cup Qualification',
                                                            'WCQ World Cup 2018 Qualification': 'World Cup Qualification',
                                                            'WCQ World Cup 2022 Qualification': 'World Cup Qualification',
                                                            'WCP World Cup 2006': 'World Cup',
                                                            'WCP World Cup 2010': 'World Cup',
                                                            'WCP World Cup 2014': 'World Cup',
                                                            'WCP World Cup 2018': 'World Cup',
                                                            'WCP World Cup 2022': 'World Cup',
                                                            'CUP Copa del Rey': 'Copa del Rey',
                                                            'CUP Coupe de France': 'Coupe de France',
                                                            'EUR UEFA Champions League': 'UEFA Champions League',
                                                            'FRN International friendly': 'International friendly',
                                                            'IUP UEFA European Super Cup': 'UEFA European Super Cup',
                                                            'PRM La Liga': 'La Liga',
                                                            'PRM Ligue 1': 'Ligue 1',
                                                            'SUP Spanish Super Cup': 'Spanish Super Cup',
                                                            'SUP Trophée des Champions': 'Trophée des Champions',
                                                            'WCT FIFA Club World Cup': 'FIFA Club World Cup',
                                                            'COC CONMEBOL–UEFA Cup of Champions 2022': 'UEFA Cup of Champions'
                                                            })

competitions = competitions.sort_values(by='Count', ascending=False)
competitions = competitions.groupby(['Competition', 'Team'])['Count'].sum().to_frame()
competitions = competitions.sort_values(by='Count', ascending=False)
competitions.reset_index(inplace=True)

fig2 = px.bar(competitions, x='Competition', y='Count', color='Team',
             color_discrete_sequence=['#DB0030', '#43A1D5', '#004170'],
             text_auto='.2s',
             title='Competitions Count by Team')
fig2.update_layout(showlegend=False)


year_teams = all_time_games.groupby(['Competition', 'Team', 'Date'])['Competition'].count().rename('Count').to_frame()
year_teams = year_teams.reset_index()
year_teams['Date'] = year_teams['Date'].dt.year

year_teams = year_teams.groupby(['Date', 'Team'])['Count'].sum().to_frame()
year_teams = year_teams.sort_values(by='Count', ascending=False)
year_teams.reset_index(inplace=True)

fig3 = px.bar(year_teams, x='Date', y='Count', color='Team',
             color_discrete_sequence=['#DB0030',  '#004170', '#43A1D5'],
             text_auto='.2s',
             pattern_shape="Team", pattern_shape_sequence=["\\", "", "|"],
             title='Games Count by Years and Team')
fig3.update_layout(showlegend=False)


goals = all_time_games.groupby(['Team', 'Year'])['Goals'].sum().to_frame()
goals = goals.reset_index()
assists = all_time_games.groupby(['Team','Year'])['Assists'].sum().to_frame()
assists = assists.reset_index()


goals_by_minutes = all_time_goals.groupby(['Season', 'Minute'])['Minute'].count().rename('Count').to_frame()
goals_by_minutes = goals_by_minutes.reset_index()


# set input value for seasons
assists_to_df = assists_to.groupby(['Assist on'])['Assist on'].count().rename('Count').to_frame()
assists_to_df = assists_to_df.reset_index()
assists_to_df.columns = ['player', 'to count']
assists_from_df = assists_from.groupby(['Assist on'])['Assist on'].count().rename('Count').to_frame()
assists_from_df = assists_from_df.reset_index()
assists_from_df.columns = ['player', 'from count']

total_assists = pd.merge(assists_to_df, assists_from_df, on='player', how='inner')
total_assists = total_assists.sort_values(['from count', 'to count'], ascending=False, ignore_index=True)

fig4 = go.Figure()
fig4.add_trace(go.Bar(
    x=total_assists['player'][:11],
    y=total_assists['to count'][:11],
    name='Assists to',
    marker_color='#DB0030'))

fig4.add_trace(go.Bar(
    x=total_assists['player'][:11],
    y=total_assists['from count'][:11],
    name='Assists from',
    marker_color='#004170'))

fig4.update_layout(title='Assists FROM and TO', barmode='stack', xaxis_tickangle=-45)


fig5 = px.bar(opponents[:5], x='Opponents', y='Goals', color='Opponents',
              text_auto='.2s', title='Top 5: Goals by Opponent',
              color_discrete_sequence=colorScheme)


external_stylesheets = [dbc.themes.SIMPLEX]

app = Dash(__name__, external_stylesheets=external_stylesheets,
           meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}])
server = app.server
app.title = 'Lionel Messi Dashboard'

app.layout = html.Div([
    html.H1(children=f'Lionel Messi Statistics as of {date}', style={'textAlign':'center', 'marginBottom': 25, 'marginTop': 25}),
    
    # START cards Div
    html.Div([
        dbc.Row([
            # card 1
            dbc.Col(dbc.Card([
                dbc.CardHeader(" "),
                dbc.CardBody([html.H4("Games Played", className="card-title", style={'text-align': 'center'}),
                             html.P(f"{total_games}", className="card-title", style={'text-align': 'center'})]),
                dbc.CardFooter(" ")], color='info', inverse=True)),
            # card 2
            dbc.Col(dbc.Card([
                dbc.CardHeader(" "),
                dbc.CardBody([html.H4("Wins", className="card-title", style={'text-align': 'center'}),
                             html.P(f"{total_wins}", className="card-title", style={'text-align': 'center'})]),
                dbc.CardFooter(" ")], color='dark', inverse=True)),
            # card 3
            dbc.Col(dbc.Card([
                dbc.CardHeader(" "),
                dbc.CardBody([html.H4("Draws", className="card-title", style={'text-align': 'center'}),
                             html.P(f"{total_draws}", className="card-title", style={'text-align': 'center'})]),
                dbc.CardFooter(" ")], color='info', inverse=True)),
            # card 4
            dbc.Col(dbc.Card([
                dbc.CardHeader(" "),
                dbc.CardBody([html.H4("Defeats", className="card-title", style={'text-align': 'center'}),
                             html.P(f"{total_lost}", className="card-title", style={'text-align': 'center'})]),
                dbc.CardFooter(" ")], color='dark', inverse=True)),
            # card 5
            dbc.Col(dbc.Card([
                dbc.CardHeader(" "),
                dbc.CardBody([html.H4("Yellow Cards", className="card-title", style={'text-align': 'center'}),
                             html.P(f"{yellow_cards}", className="card-title", style={'text-align': 'center'})]),
                dbc.CardFooter(" ")], color='info', inverse=True)),
            # card 6
            dbc.Col(dbc.Card([
                dbc.CardHeader(" "),
                dbc.CardBody([html.H4("Red Cards", className="card-title", style={'text-align': 'center'}),
                              html.P(f"{red_cards}", className="card-title", style={'text-align': 'center'})]),
                dbc.CardFooter(" ")], color='dark', inverse=True)),            
        ])
    ]),
    # END cards Div
    
    # START Graph Block 1
    html.H2(children="General Statistics", style={'textAlign':'center', 'marginBottom': 25, 'marginTop': 25, "font-weight": "bold"}),
    html.Div([dbc.Row([
        dbc.Col([dcc.Graph(id='graph-content1', figure=fig1)]),
        dbc.Col([dcc.Graph(id='graph-content2', figure=fig2)]),
    ])]),
    
    html.H2(children="Games Count by Years and Team", style={'textAlign':'center', 'marginTop': 25, "font-weight": "bold"}),
    html.Div([dcc.Graph(id='graph-content3', figure=fig3)]),
    # END Graph Block 1
    
    # START Graph Block 2
    html.H2(children="Goals Statistics", style={'textAlign':'center', 'marginTop': 25, "font-weight": "bold"}),
    html.Div([html.H6(children="Select Season:", style={'textAlign':'left','marginLeft': 10, "font-weight": "bold"}),
              dcc.Dropdown(options=[{'label': i, 'value': i} for i in goals_what['Season'].unique()],
                           value=['2020-21', '2021-22', '2022-23'],
                           multi=True,
                           clearable=False,
                           disabled=False,
                           style=dict(width='50%', display='inline-block'),
                           placeholder='Select season',
                           id='dropdown-selection'),
              
              dcc.Checklist(options=[{'label': i, 'value': i} for i in goals_what['Team'].unique()],
                            value=['Argentina', 'FC Barcelona', 'Paris Saint-Germain'],
                            inline=True,
                            style={'width': '45%', 'display': 'inline-block'},
                            id='checklist-selection')]),
    html.Div([dbc.Row([
        dbc.Col([dcc.Graph(id='graph-content4')]),
        dbc.Col([dcc.Graph(id='graph-content5')]),
        dbc.Col([dcc.Graph(id='graph-content6')]),
    ])]),
    # END Graph Block 2
    
    # START Graph Block 3
    html.Div([dbc.Row([
        dbc.Col([dcc.Graph(id='graph-content7')]),
        dbc.Col([dcc.Graph(id='graph-content8', figure=fig4)]),
        dbc.Col([dcc.Graph(id='graph-content9', figure=fig5)]),
    ])]),
    # END Graph Block 3

    html.H4(children="Source of data: http://messi.starplayerstats.com/en", style={'textAlign':'center', 'marginTop': 25, "font-weight": "bold"}),

], id="mainContainer")


@app.callback(Output('graph-content4', 'figure'),
              Input('dropdown-selection', 'value'),
              Input('checklist-selection', 'value'))
def update_graph1(value_season, value_team):
    dff = goals_how[(goals_how['Season'].isin(value_season))&(goals_how['Team'].isin(value_team))]
    dff = dff.groupby(['Team', 'How'])['Count'].sum().to_frame()
    dff.reset_index(inplace=True)
    fig = px.bar(dff, x='Count', y='How', color='Team', orientation='h',
                 color_discrete_sequence=['#CB8B15', '#749ED2', '#71093B'],
                 title='How the goal was scored?')
    return fig


@app.callback(Output('graph-content5', 'figure'),
              Input('dropdown-selection', 'value'),
              Input('checklist-selection', 'value'))
def update_graph2(value_season, value_team):
    dff = goals_what[(goals_what['Season'].isin(value_season))&(goals_what['Team'].isin(value_team))]
    dff = dff.groupby(['Team', 'What'])['Count'].sum().to_frame()
    dff.reset_index(inplace=True)
    fig = px.bar(dff, x='Count', y='What', color='Team', orientation='h',
                 color_discrete_sequence=['#CB8B15', '#749ED2', '#71093B'],
                 title='What was the type of goal?')
    return fig


@app.callback(Output('graph-content6', 'figure'),
              Input('dropdown-selection', 'value'))
def update_graph4(value_season):
    df = goals_by_minutes[goals_by_minutes['Season'].isin(value_season)]
    fig = px.line(df, x="Minute", y="Count", color='Season',
                  color_discrete_sequence=colorScheme2, title='Goals by Minutes')
    
    return fig


@app.callback(Output('graph-content7', 'figure'),
              Input('checklist-selection', 'value'))
def update_graph3(value_team):
    df1 = goals[goals['Team'].isin(value_team)]
    df2 = assists[assists['Team'].isin(value_team)]
    # Create traces
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df1['Year'], y=df1['Goals'],
                             mode='lines',
                             name='Goals',
                             line=dict(color='#DB0030')))

    fig.add_trace(go.Scatter(x=df2['Year'], y=df2['Assists'],
                             mode='lines',
                             name='Assists',
                             line=dict(color='#004170')))

    fig.update_layout(title='Total Assist and Goals',
                      xaxis_title='Year',
                      yaxis_title='Count')

    return fig


app.css.append_css({'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'})

if __name__ == '__main__':
    app.run_server(debug=False)




