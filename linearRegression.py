import pandas as pd
import requests
import pprint
import csv
import math
import locale
import collections
from datetime import date
import statsmodels.formula.api as sm
import statsmodels.api as sms
import matplotlib.pyplot as plt
import numpy as np
import statsmodels.formula.api as sm
import statsmodels.api as sms
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings("ignore")
locale.setlocale( locale.LC_ALL, 'en_US.UTF-8' )

allstar = pd.read_csv('AllStarData.csv')
salaries = pd.read_csv('SalariesData.csv')
master = pd.read_csv('MasterData.csv')

def PlayerAll():
    d = pd.DataFrame()
    merge = pd.merge(allstar, master, on='playerID')
    del merge['Unnamed: 0_x']
    del merge['Unnamed: 0_y']
    #calculate age
    byears = list(merge.birthYear)
    years = list(merge.yearID)
    age = []
    for i in range(len(byears)):
        yrs_diff = years[i] - byears[i]
        age.append(yrs_diff)
    merge['age'] = age
    del merge['birthYear']
    del merge['birthMonth']
    del merge['birthDay']
    merge1 = merge.loc[merge['yearID'] >= 1985]
    merge2 = pd.merge(merge1, salaries, on='playerID')
    merge2 = merge2[merge2.yearID_x == merge2.yearID_y]
    del merge2['yearID_x']
    del merge2['teamID_x']
    del merge2['Unnamed: 0']
    del merge2['playerID']
    merge2.columns = ['nameFirst', 'nameLast', 'age', 'yearID', 'teamID', 'salary']
    merge2 = merge2.reset_index(drop=True)
    return merge2

def getPlayerAVG():
    new = PlayerAll()
    new['FullName'] = new[['nameFirst', 'nameLast']].apply(lambda x: ' '.join(x), axis=1)
    del new['nameFirst']
    del new['nameLast']
    #pprint.pprint(new)
    lol = {k: g["salary"].tolist() for k,g in new.groupby("FullName")}
    players = list(lol.keys())
    for i in range(len(lol)):
        average = sum(lol[players[i]])/len(lol[players[i]])
        lol[players[i]] = average
    #list of all players with their average salaries
    #pprint.pprint(lol)
    final = pd.DataFrame.from_dict(lol, orient='index')
    final.columns = ["FullName"]
    final['FullName'] = final.index
    final.index = range(822)
    final['Average_Salary'] = lol.values()
    return final

def getAllStarApp():
    new = PlayerAll()
    new['FullName'] = new[['nameFirst', 'nameLast']].apply(lambda x: ' '.join(x), axis=1)
    del new['nameFirst']
    del new['nameLast']
    #pprint.pprint(new)
    lol = {k: g["salary"].tolist() for k,g in new.groupby("FullName")}
    players = list(lol.keys())
    for i in range(len(lol)):
        num = len(lol[players[i]])
        lol[players[i]] = num
    #list of all players with their average salaries
    #pprint.pprint(lol)
    final = pd.DataFrame.from_dict(lol, orient='index')
    final.columns = ["FullName"]
    final['FullName'] = final.index
    final.index = range(822)
    final['Number_All_Star_Appearances'] = lol.values()
    return final
    

#PlayerAll()
#getPlayerAVG()
#getAllStarApp()

d1 = getAllStarApp()
d2 = getPlayerAVG()
merged = pd.merge(d1, d2, on='FullName')
r = sm.ols(formula="Number_All_Star_Appearances ~ Average_Salary", data=merged).fit()
print(r.summary())

fig = plt.figure(figsize=(12,8))
fig = sms.graphics.plot_partregress_grid(r, fig=fig)
plt.show()

