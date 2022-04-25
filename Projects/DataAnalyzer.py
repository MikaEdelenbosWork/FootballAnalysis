import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import plotly.graph_objects as go


def get_league_average(dataframe, columnname, decimals):
    # Get the league average and round to specific decimals
    temp_total = dataframe[columnname].sum()
    temp_participants = dataframe[columnname].count()
    temp_average = temp_total / temp_participants
    temp_average = temp_average.round(decimals)
    return temp_average


sns.set(style='darkgrid', context='notebook', palette='pastel', font_scale=0.8)
teamShootingData = []
teamPassingData = []
playerShootingData = []
playerPassingData = []

teamShootingData = pd.read_csv('../Data/MLS_Team_Shooting_Data.csv')
teamPassingData = pd.read_csv('../Data/MLS_Team_Passing_Data.csv')
playerShootingData = pd.read_csv('../Data/MLS_Player_Shooting_Data.csv')
playerPassingData = pd.read_csv('../Data/MLS_Player_Passing_Data.csv')

# Filter playing time for at least 90 minutes
playerShootingData = playerShootingData[playerShootingData['90s'] >= 1]
playerPassingData = playerPassingData[playerPassingData['90s'] >= 1]
# Filter Position
playerShootingData = playerShootingData[playerShootingData['Pos'].str.contains('FW')]
playerPassingData = playerPassingData[playerPassingData['Pos'].str.contains('MF')]
playerShootingData.reset_index(inplace=True)
playerPassingData.reset_index(inplace=True)
print(playerShootingData)
print(playerPassingData)

# Filter Player Data
playerShootingData['Player'] = playerShootingData['Player'].astype('string')
specificPlayerData = playerShootingData.loc[playerShootingData['Player'] == 'Leonardo Campana']

# ---Team Data---
tnpxG = teamShootingData['npxG']
tGoals = teamShootingData['Gls']
tPasses = teamPassingData['Cmp']
tProgPasses = teamPassingData['Prog']
teams = teamShootingData['Squad']

# ---Player Data---
pPasses = playerPassingData['Cmp']
pProgPasses = playerPassingData['Prog']
pGoals = playerShootingData['Gls']
pnpXG = playerShootingData['npxG']
pFWSquad = playerShootingData['Squad']
pMFSquad = playerPassingData['Squad']
players = playerShootingData['Player']

# Get League Average
leagueAverageGoals = get_league_average(playerShootingData, 'Gls', 2)
leagueAverageNpxG = get_league_average(playerShootingData, 'npxG', 2)
leagueAverageShots = get_league_average(playerShootingData, 'Sh', 2)
leagueAverageSoT = get_league_average(playerShootingData, 'SoT', 2)
leagueAverageGoalsSoT = get_league_average(playerShootingData, 'G/SoT', 2)

# ---Player Specific Data---
psGoals = specificPlayerData['Gls'].item()
psNpxG = specificPlayerData['npxG'].item()
psShots = specificPlayerData['Sh'].item()
psSoT = specificPlayerData['SoT'].item()
psGoalsSoT = specificPlayerData['G/SoT'].item()

# ---Plotting the Data---
fig1, axes = plt.subplots(2, 2)
fig2 = go.Figure()
r1 = [psGoals, psNpxG, psShots, psSoT, psGoalsSoT]
r2 = [leagueAverageGoals, leagueAverageNpxG, leagueAverageShots, leagueAverageSoT, leagueAverageGoalsSoT]
theta = ['Goals', 'npxG', 'Shots', 'SoT', 'G/SoT']
fig1.set_figheight(15)
fig1.set_figwidth(15)

sns.scatterplot(ax=axes[0, 0], x=tnpxG, y=tGoals, hue=teams, legend=False)
axes[0, 0].title.set_text("MLS Most Clinical Teams")
axes[0, 0].set_xlabel("Non Penalty Expected Goals per 90")
axes[0, 0].set_ylabel("Goals Scored per 90")
for i, label in enumerate(teams):
    axes[0, 0].annotate(label, (tnpxG[i], tGoals[i]), textcoords="offset points", xytext=(0, 10), ha='center')

sns.scatterplot(ax=axes[0, 1], x=tPasses, y=tProgPasses, hue=teams, legend=False)
axes[0, 1].title.set_text("MLS Most Progressive Passing Teams")
axes[0, 1].set_xlabel("Completed Passes per 90")
axes[0, 1].set_ylabel("Progressive Passes per 90")
for i, label in enumerate(teams):
    axes[0, 1].annotate(label, (tPasses[i], tProgPasses[i]), textcoords="offset points", xytext=(0, 10), ha='center')

sns.scatterplot(ax=axes[1, 0], x=pnpXG, y=pGoals, hue=pFWSquad, legend=False)
axes[1, 0].title.set_text("MLS Most Efficient Forwards")
axes[1, 0].set_xlabel("Non Penalty Expected Goals per 90")
axes[1, 0].set_ylabel("Goals Scored per 90")
for i, label in enumerate(players):
    if pnpXG[i] >= 0.8 or pGoals[i] >= 0.8:
        axes[1, 0].annotate(label, (pnpXG[i], pGoals[i]), textcoords="offset points", xytext=(0, 10), ha='center'
                            , arrowprops=dict(arrowstyle="->", connectionstyle="arc3", color='black'))

sns.scatterplot(ax=axes[1, 1], x=pPasses, y=pProgPasses, hue=pMFSquad, legend=False)
axes[1, 1].title.set_text("MLS Best Passing Midfielders")
axes[1, 1].set_xlabel("Completed Passes per 90")
axes[1, 1].set_ylabel("Progressive Passes per 90")
for i, label in enumerate(players):
    if pPasses[i] >= 60 or pProgPasses[i] >= 8:
        axes[1, 1].annotate(label, (pPasses[i], pProgPasses[i]), textcoords="offset points", xytext=(0, 10), ha='center'
                            , arrowprops=dict(arrowstyle="->", connectionstyle="arc3", color='black'))

fig2.add_trace(go.Scatterpolar(r=r1, theta=theta, name='Leonardo Campana', fill='toself', hovertemplate='%{theta}: %{r}'))
fig2.add_trace(go.Scatterpolar(r=r2, theta=theta, name='League Average', fill='toself', hovertemplate='%{theta}: %{r}'))
fig2.update_layout(
    polar=dict(
        radialaxis=dict(
            visible=True
        )),
    showlegend=True,
    title='Leonardo Campana Evaluation',
    hovermode='closest'
)

plt.show()
fig2.show()
