# -*- coding: utf-8 -*-

import pandas as pd

'''
all star information for all players by year: 
['playerID', 'yearID', 'teamID']
'''
'''
def getAllStar():
    allstar = pd.read_csv('AllstarFull.csv')
    allstar = allstar[['playerID', 'yearID', 'teamID']]
    print("ALL STAR")
    #pprint.pprint(allstar)
    allstar.to_csv('AllStarData.csv')
    '''
    
'''
individual player information: 
['playerID', 'birthYear', 'birthMonth', 'birthDay', 'nameFirst', 'nameLast']
'''
def getMaster():
    master = pd.read_csv('Master.csv')
    master = master[['playerID', 'birthYear', 'birthMonth', 'birthDay', 'nameFirst', 'nameLast']]
    print("MASTER")
    #pprint.pprint(master)
    master.to_csv('MasterData.csv')

'''
Salary information for each player by year: 
['yearID', 'teamID', 'playerID', 'salary']
'''
def getSalaries():
    salaries = pd.read_csv('Salaries.csv')
    del salaries['lgID']
    print("SALARIES")
    #pprint.pprint(salaries)
    salaries.to_csv('SalariesData.csv')
    
'''
Team information:
['yearID', 'teamID', 'Rank', 'LGwin', 'WSwin', 'name'] 
'''
def getTeams():
    teams = pd.read_csv('Teams.csv')
    teams = teams[['yearID', 'teamID', 'Rank', 'LgWin', 'WSWin', 'name']]
    print("TEAMS")
    #pprint.pprint(teams)
    teams.to_csv('TeamsData.csv')

#getAllStar()
getMaster()
getSalaries()
getTeams()

'''
All these datasets will be used for merging and comparison analysis in the second progress report.
'''
