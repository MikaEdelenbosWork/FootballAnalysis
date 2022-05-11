import os

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from PIL import Image
from matplotlib.offsetbox import OffsetImage, AnnotationBbox


def get_league_average(dataframe, columnname, decimals):
    # Get the league average and round to specific decimals
    temp_total = dataframe[columnname].sum()
    temp_participants = dataframe[columnname].count()
    temp_average = temp_total / temp_participants
    temp_average = temp_average.round(decimals)
    return temp_average


sns.set(style='darkgrid', context='notebook', palette='pastel', font_scale=0.8)

teamShootingData = pd.read_csv('../Data/MLS/MLS_Team_Shooting_Data.csv')
teamPassingData = pd.read_csv('../Data/MLS/MLS_Team_Passing_Data.csv')
playerShootingData = pd.read_csv('../Data/MLS/MLS_Player_Shooting_Data.csv')
playerPassingData = pd.read_csv('../Data/MLS/MLS_Player_Passing_Data.csv')

# Filter playing time for at least 90 minutes
playerShootingData = playerShootingData[playerShootingData['90s'] >= 1]
playerPassingData = playerPassingData[playerPassingData['90s'] >= 1]
# Filter Position
playerShootingData = playerShootingData[playerShootingData['Pos'].str.contains('FW')]
playerPassingData = playerPassingData[playerPassingData['Pos'].str.contains('MF')]
playerShootingData.reset_index(inplace=True)
playerPassingData.reset_index(inplace=True)

# Filter Player Data
playerShootingData['Player'] = playerShootingData['Player'].astype('string')
specificPlayerData = playerShootingData.loc[playerShootingData['Player'] == 'Leonardo Campana']
specificPlayerData2 = playerShootingData.loc[playerShootingData['Player'] == 'Taxiarchis Fountas']

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

# Get League Max
leagueMaxGoals = playerShootingData['Gls'].max()
leagueMaxNpxG = playerShootingData['npxG'].max()
leagueMaxShots = playerShootingData['Sh'].max()
leagueMaxSoT = playerShootingData['SoT'].max()
leagueMaxGoalsSoT = playerShootingData['G/SoT'].max()
leagueMaxPasses = playerPassingData['Cmp'].max()
leagueMaxProg = playerPassingData['Prog'].max()

# ---Player Specific Data---
psGoals = specificPlayerData['Gls'].item()
psNpxG = specificPlayerData['npxG'].item()
psShots = specificPlayerData['Sh'].item()
psSoT = specificPlayerData['SoT'].item()
psGoalsSoT = specificPlayerData['G/SoT'].item()
psGoals2 = specificPlayerData2['Gls'].item()
psNpxG2 = specificPlayerData2['npxG'].item()
psShots2 = specificPlayerData2['Sh'].item()
psSoT2 = specificPlayerData2['SoT'].item()
psGoalsSoT2 = specificPlayerData2['G/SoT'].item()

# Data Manipulation
league80PercentileGoals = ((leagueMaxGoals/100) * 80)
league80PercentileNpxG = ((leagueMaxNpxG/100)*80)
league80PercentilePasses = ((leagueMaxPasses/100)*80)
league80PercentileProg = ((leagueMaxProg/100)*80)

# ---Plotting the Data---
fig1, axes = plt.subplots(1, 2)
fig2, axes2 = plt.subplots(1, 2)
fig3 = go.Figure()

# Data for the RadarGraph
theta = ['Goals per 90', 'npxG per 90', 'Shots per 90', 'SoT per 90', 'G/SoT per 90']
scales = [leagueMaxGoals, leagueMaxNpxG, leagueMaxShots, leagueMaxSoT, leagueMaxGoalsSoT]
r1 = [psGoals, psNpxG, psShots, psSoT, psGoalsSoT]
r2 = [leagueAverageGoals, leagueAverageNpxG, leagueAverageShots, leagueAverageSoT, leagueAverageGoalsSoT]
r3 = [psGoals2, psNpxG2, psShots2, psSoT2, psGoalsSoT2]

# Scale it to 0-1 for the Graph
r1scaled = [i/j for i, j in zip(r1, scales)]
r2scaled = [i/j for i, j in zip(r2, scales)]
r3scaled = [i/j for i, j in zip(r3, scales)]

# Close the line in the Graph
theta = [*theta, theta[0]]
r1 = [*r1, r1[0]]
r2 = [*r2, r2[0]]
r3 = [*r3, r3[0]]
r1scaled = [*r1scaled, r1scaled[0]]
r2scaled = [*r2scaled, r2scaled[0]]
r3scaled = [*r3scaled, r3scaled[0]]

fig = px.scatter(teamShootingData, x='npxG', y='Gls', color='Squad', text='Squad', log_x=True)
fig.update_traces(textposition='top center')

images = []
for file in os.listdir('../Assets/MLS Logos'):
    filename = os.fsdecode(file)
    if filename.endswith(".png"):
        images.append('../Assets/MLS Logos/' + filename)

sns.scatterplot(ax=axes[0], data=teamShootingData, x='npxG', y='Gls', hue='Squad', legend=False)
axes[0].title.set_text("MLS Most Clinical Teams")
axes[0].set_xlabel("Non Penalty Expected Goals per 90")
axes[0].set_ylabel("Goals Scored per 90")
for i, label in enumerate(teams):
    axes[0].annotate(label, (tnpxG[i], tGoals[i]), textcoords="offset points", xytext=(0, 10), ha='center')

sns.scatterplot(ax=axes[1], data=teamPassingData, x='Cmp', y='Prog', hue='Squad', legend=False)
axes[1].title.set_text("MLS Most Progressive Passing Teams")
axes[1].set_xlabel("Completed Passes per 90")
axes[1].set_ylabel("Progressive Passes per 90")
for i, label in enumerate(teams):
    axes[1].annotate(label, (tPasses[i], tProgPasses[i]), textcoords="offset points", xytext=(0, 10), ha='center')

sns.scatterplot(ax=axes2[0], data=playerShootingData, x='npxG', y='Gls', hue='Squad', legend=False)
axes2[0].title.set_text("MLS Most Efficient Forwards")
axes2[0].set_xlabel("Non Penalty Expected Goals per 90")
axes2[0].set_ylabel("Goals Scored per 90")
for i, label in enumerate(players):
    if pnpXG[i] >= league80PercentileNpxG or pGoals[i] >= league80PercentileGoals:
        axes2[0].annotate(label, (pnpXG[i], pGoals[i]), textcoords="offset points", xytext=(0, 10), ha='center',
                          arrowprops=dict(arrowstyle="->", connectionstyle="arc3", color='black'))

sns.scatterplot(ax=axes2[1], data=playerPassingData, x='Cmp', y='Prog', hue='Squad', legend=False)
axes2[1].title.set_text("MLS Best Passing Midfielders")
axes2[1].set_xlabel("Completed Passes per 90")
axes2[1].set_ylabel("Progressive Passes per 90")
for i, label in enumerate(players):
    if pPasses[i] >= league80PercentilePasses or pProgPasses[i] >= league80PercentileProg:
        axes2[1].annotate(label, (pPasses[i], pProgPasses[i]), textcoords="offset points", xytext=(0, 10), ha='center',
                          arrowprops=dict(arrowstyle="->", connectionstyle="arc3", color='black'))
x1 = [league80PercentilePasses, league80PercentilePasses]
y1 = [0, league80PercentileProg]
x2 = [0, league80PercentilePasses]
y2 = [league80PercentileProg, league80PercentileProg]
axes2[1].plot(x1, y1)
axes2[1].plot(x2, y2)

fig3.add_trace(
    go.Scatterpolar(
        customdata=r3,
        r=r3scaled,
        theta=theta,
        name='Taxiarchis Fountas',
        fill='toself',
        hovertemplate='%{theta}: %{customdata}'
    )
)
fig3.add_trace(
    go.Scatterpolar(
        customdata=r1,
        r=r1scaled,
        theta=theta,
        name='Leonardo Campana',
        fill='toself',
        hovertemplate='%{theta}: %{customdata}'
    )
)
fig3.add_trace(
    go.Scatterpolar(
        customdata=r2,
        r=r2scaled,
        theta=theta,
        name='League Average',
        fill='toself',
        hovertemplate='%{theta}: %{customdata}'
    )
)
fig3.update_layout(
    polar=dict(
        radialaxis=dict(
            visible=False,
            range=[0, 1]
        )),
    showlegend=True,
    title='Leonardo Campana per 90 Evaluation',
    hovermode='closest'
)
fig.show()
fig3.show()
plt.show()
