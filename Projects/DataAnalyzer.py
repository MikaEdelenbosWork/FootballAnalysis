import csv
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
from adjustText import adjust_text

sns.set(style='darkgrid', context='notebook', palette='pastel', font_scale=0.8)
teamShootingData = []
teamPassingData = []
playerShootingData = []
playerPassingData = []


def open_data(data_title):
    data = []
    with open(f'../Data/{data_title}', 'r', encoding="utf-8") as csvfile:
        file_reader = csv.reader(csvfile, delimiter=',')
        for row in file_reader:
            data.append(row)
    data = np.array(data)
    return data


teamShootingData = pd.read_csv('../Data/MLS_Team_Shooting_Data.csv')
teamPassingData = pd.read_csv('../Data/MLS_Team_Passing_Data.csv')
playerShootingData = pd.read_csv('../Data/MLS_Player_Shooting_Data.csv')
playerPassingData = pd.read_csv('../Data/MLS_Player_Passing_Data.csv')

# Filter playing time for at least 90 minutes
playerShootingData = playerShootingData[playerShootingData.iloc[:, 4] >= 1]
playerPassingData = playerPassingData[playerPassingData.iloc[:, 4] >= 1]
# Filter Position
playerShootingData = playerShootingData[playerShootingData.iloc[:, 2].str.contains('FW')]
playerPassingData = playerPassingData[playerPassingData.iloc[:, 2].str.contains('MF')]
playerShootingData.reset_index(inplace=True)
playerPassingData.reset_index(inplace=True)

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

# ---Plotting the Data---
fig1, axes = plt.subplots(2, 2)
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
plt.show()
