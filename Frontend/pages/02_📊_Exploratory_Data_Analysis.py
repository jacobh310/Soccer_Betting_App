import streamlit as st
import pandas as pd
from utils.importer import *
import plotly.express as px
import plotly.graph_objects as go
import warnings

warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.simplefilter(action='ignore', category=FutureWarning)
pd.options.mode.chained_assignment = None  # default='warn'

# Load and reformat Data
data = DataImport()
data.fetch_and_clean_data()
stats_df = data.stats
game_team_stats_season = data.prep_data()

# Load and Format Plots
plot1 = make_scatter(game_team_stats_season, x='Target Shots', y='Goals', animation_frame='Season', hover_name='Team',
                     color='WDL', animation_group='Team', size='Shots')

plot2 = make_scatter(df=stats_df, x='HTGD', y='ATGD', animation_frame='Season', hover_name='HomeTeam', size='HTP',
                     color='Home Result')

plot3 = make_scatter(df=stats_df, x='HTP', y='ATP', animation_frame='Season', hover_name='HomeTeam',
                     color='Home Result')

x = 'HTGD'
y = 'ATGD'
z = 'FPD'

range_x = [stats_df[x].min(), stats_df[x].max()]
range_y = [stats_df[y].min(), stats_df[y].max()]
range_z = [stats_df[z].min(), stats_df[z].max()]

plot4 = px.scatter_3d(stats_df, x=x, y=y, z=z, animation_frame='Season', hover_name='HomeTeam', color='Home Result',
                      range_x=range_x, range_y=range_y, range_z=range_z, width=700, height=500,
                      color_discrete_sequence=px.colors.qualitative.Antique)
plot4.update_traces(marker_line_width=1, marker_size=3)

# Format And Style Page

st.set_page_config(page_title="EDA", layout='wide')
st.title("Exploratory Data Analysis")
st.markdown('''##### <span style="color:gray">This EDA uses British Premier League Data from 2000-2022. Enjoy the interactive plots made with Plotly </span>''', unsafe_allow_html=True)
t1, t2, t3 = st.tabs(["Scatter Plots", "Bar Charts", "Build Your Own"])

with t1:
    col1, col2 = st.columns(2)
    col1.markdown("<h3 style='text-align: Left;'>Target Shots vs Goals</h3>",
                  unsafe_allow_html=True)
    col1.markdown("""<p style='color:gray';>The scatter plot below takes the average target shots and plots them versus the 
            average goals. The size ofthe markers were scaled to resemble the average number of shots. It is clear from 
            looking at this plot that the number of target shots is positively correlated with the number of goals.
            The teams that win also score a lot of goals.</p>""",
                  unsafe_allow_html=True)

    col1.markdown("""<p style='color:gray';>It is important to note that this looks at the averages target shots and goals after the outcome. From this
        plot you cannot conclude that teams that average a lot of target shots will have a higher chance of winning</p>""",
                  unsafe_allow_html=True)

    col1.plotly_chart(plot1)

    col2.markdown("<h3 >Home Team Goal Difference (HTGD) vs Away Team Goal Difference (ATGD)</h3>",
                  unsafe_allow_html=True)

    col2.markdown("""<p style='color:gray';>Team Goal Difference is defined by the average difference of goals between that team and 
            their opponent. Looking at the scatter plots from each season a patter starts to arise. The home team would
            win when they had a highest goal difference from the away team. Notice how the majority of the Home win markers
            conglomerate at the lower right side of the plot. That is where the HTGD is the highest and teh ATGD is the 
            lowest</p>""",
                  unsafe_allow_html=True)
    col2.plotly_chart(plot2)

    col3, col4 = st.columns(2)

    col3.markdown("<h3 >Home Team Points (HTP) vs Away Team Points (ATP)</h3>",
                  unsafe_allow_html=True)
    col3.markdown("""<p style='color:gray';>From this scatter plot we see that there are more of the Home Win markers 
    on the right and lower side indicating that the home team generally won when they had a greater points difference 
    than the away team of the plot</p>""", unsafe_allow_html=True)
    col3.plotly_chart(plot3)

    col4.markdown("<h3 >Home Team Goal Difference (HTGD) vs Away Team Goal Difference (ATGD) vs Form Points Difference "
                  "(FPD)</h3>",
                  unsafe_allow_html=True)
    col4.markdown("""<p style='color:gray';>This 3D scatter plots has HTGD and ATGD like the plot above but it also
    plots FPD (Form Points Difference on the Z-axis. FPD is the difference in points from the home team and away team in
    the last 3 games. You would expect expect fixtures with a higher FPD, HTGD, and lower ATGD to have a higher home
     team win rate. At looking at the plot this is generally true</p>""", unsafe_allow_html=True)
    col4.plotly_chart(plot4)


with t2:
    # bar 1
    goals_by_season = stats_df.groupby(['Season']).sum()[['FTHG', 'FTAG']].reset_index()
    # Create a figure with two subplots
    bar1 = go.Figure()
    bar1.add_trace(go.Bar(x=goals_by_season['Season'], y=goals_by_season['FTHG'], name='Home Goals'))
    bar1.add_trace(go.Bar(x=goals_by_season['Season'], y=goals_by_season['FTAG'], name='Away Goals'))
    bar1.update_layout(title='Home and Away Goals by Season', xaxis_title='Season', yaxis_title='Goals',
                       width=700, height=500)

    # bar 2
    wdl_df = stats_df.groupby(['Season', 'FTR']).count().reset_index().iloc[:, :3]
    wdl_df = wdl_df.rename(columns={'Unnamed: 0': 'Outcome'})
    wdl_df = wdl_df.pivot_table('Outcome', ['Season'], 'FTR')
    wdl_df = wdl_df[['H', 'D', 'A']].reset_index()

    bar2 = go.Figure()
    bar2.add_trace(go.Bar(x=wdl_df['Season'], y=wdl_df['H'], name='Home Wins'))
    bar2.add_trace(go.Bar(x=wdl_df['Season'], y=wdl_df['D'], name='Draws'))
    bar2.add_trace(go.Bar(x=wdl_df['Season'], y=wdl_df['A'], name='Away Wins'))
    bar2.update_layout(title='Wins Draws by Season', xaxis_title='Season', yaxis_title='Occurences',
                       width=700, height=500)

    # bar 3
    home_goals = stats_df.groupby(['HomeTeam']).sum()[['FTHG', 'FTAG']].reset_index()
    away_goals = stats_df.groupby(['AwayTeam']).sum()[['FTHG', 'FTAG']].reset_index()
    team_goals_scored = home_goals[['HomeTeam', 'FTHG']].join(away_goals[['AwayTeam', 'FTAG']])
    team_goals_scored['Total Goals'] = team_goals_scored['FTHG'] + team_goals_scored['FTAG']
    team_goals_scored = team_goals_scored.drop(columns=['AwayTeam']).sort_values('FTHG', ascending=False)

    bar3 = go.Figure()

    bar3.add_trace(go.Bar(x=team_goals_scored['HomeTeam'], y=team_goals_scored['FTHG'], name='Home Goals'))
    bar3.add_trace(go.Bar(x=team_goals_scored['HomeTeam'], y=team_goals_scored['FTAG'], name='Away Goals'))
    bar3.update_layout(title='Home and Away Goals by Team since 2000-01', xaxis_title='Teams', yaxis_title='Goals',
                       width=1200, height=600)

    col1, col2 = st.columns(2)

    col1.plotly_chart(bar1)
    col2.plotly_chart(bar2)
    st.plotly_chart(bar3)

with t3:

    col1, col2 = st.columns(2)
    vars = ['Home Result', 'HTGD', 'HTS', 'HTTS', 'HTF', 'HTC', 'HTY', 'HTR', 'ATGD',
            'ATS', 'ATTS', 'ATF', 'ATC', 'ATY', 'ATR', 'HTP', 'ATP']

    col1.subheader('Custom Scatter Plots')

    x = col1.selectbox("Select an X variable", vars, index=1)
    y = col1.selectbox("Select y variable", vars, index=8)
    size = col1.selectbox("Select size variable", vars + [None], index=17)

    if (x == y) or (y == size) or (x == size):
        col1.warning('All Variables must be different')

    else:
        plot = make_scatter(df=stats_df, x=x, y=y, animation_frame='Season', hover_name='HomeTeam',
                            size=size, color='Home Result')

        col1.plotly_chart(plot)


    col2.subheader('Custom Bar Charts')


    def make_season_bar(stat):

        stat_dic = {'Goals':['FTHG', 'FTAG'],
                    'Shots':['HTS','ATS'],
                    'Target Shots':['HTTS','ATTS']}
        df_stat = stat_dic[stat]

        goals_by_season = stats_df.groupby(['Season']).sum()[df_stat].reset_index()
        # Create a figure with two subplots
        fig = go.Figure()

        # Add the first set of bars to the first subplot
        fig.add_trace(go.Bar(x=goals_by_season['Season'], y=goals_by_season[df_stat[0]], name=f'Home {stat}'))
        # Add the second set of bars to the second subplot
        fig.add_trace(go.Bar(x=goals_by_season['Season'], y=goals_by_season[df_stat[1]], name=f'Away {stat}'))
        fig.update_layout(title=f'Home and Away {stat} by Season', xaxis_title='Season', yaxis_title=stat,
                          width=700, height=500)
        return fig

    stats = ['Goals','Shots','Target Shots']
    stat = col2.selectbox("Select a Game Stat", stats, index=0)
    bar = make_season_bar(stat)
    col2.plotly_chart(bar)

