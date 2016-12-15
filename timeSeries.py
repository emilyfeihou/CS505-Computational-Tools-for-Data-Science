import pandas as pd
import csv
import dateutil.parser
import matplotlib.pyplot as plt
import scipy.spatial 
import pprint
import warnings

allstar = pd.read_csv('AllStarData.csv')
master = pd.read_csv('MasterData.csv')
salaries = pd.read_csv('SalariesData.csv')

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

def getAverageAge():
    new = PlayerAll()
    new['FullName'] = new[['nameFirst', 'nameLast']].apply(lambda x: ' '.join(x), axis=1)
    del new['nameFirst']
    del new['nameLast']
    #pprint.pprint(new)
    lol = {k: g["age"].tolist() for k,g in new.groupby("FullName")}
    players = list(lol.keys())
    for i in range(len(lol)):
        average = sum(lol[players[i]])/len(lol[players[i]])
        lol[players[i]] = average
    #list of all players with their average age
    #pprint.pprint(lol)
    final = pd.DataFrame.from_dict(lol, orient='index')
    final.columns = ["FullName"]
    final['FullName'] = final.index
    final.index = range(822)
    final['Average_Age'] = lol.values()
    return final

def timeSeries():
    num = getAllStarApp()
    years = PlayerAll()
    years['FullName'] = years[['nameFirst', 'nameLast']].apply(lambda x: ' '.join(x), axis=1)
    del years['nameFirst']
    del years['nameLast']

    #years["yearID"] = pd.to_datetime(years["yearID"])
    years['yearID'] = pd.to_datetime(pd.Series(years['yearID']), format = '%Y')
    #players' allstar appearances in descending order
    sort = num.sort_values(by='Number_All_Star_Appearances', ascending=False)
    #pprint.pprint(sort)
    #get top 100 players with the most all-star appearances
    top_100 = sort.head(100)
    top_100 = top_100.reset_index()
    #print(top_100)
    age = getAverageAge()
    masterAge = pd.merge(top_100, age, on='FullName')
    result = pd.merge(top_100, years, on='FullName')
    del result['teamID']
    del result['salary']
    #print(result)
    biglist = []
    for i in range(100):
        #dataframe for just each user
        player = result.loc[result['FullName'] == top_100['FullName'][i]]
        del player['index']
        player.index = player['yearID']
        player['num'] = 1
        #print(player)
        month = player.num.resample('5A').sum()
        #month.plot()
        #print(month)
        months_of_users = month.fillna(0).tolist()
        biglist.append(months_of_users)
    
    min1 = 0
    max1 = 0
    min2 = 0
    max2 = 0
    min_dist = 5000
    max_dist = 0
    for i in range(len(biglist)):
        for j in range(len(biglist)):
            if (i != j and len(biglist[i]) == len(biglist[j])):
                mink = scipy.spatial.distance.minkowski(biglist[i], biglist[j], 1)
                if (mink > max_dist):
                    max_dist = mink
                    max1 = i
                    max2 = j
                if (mink < min_dist):
                    min_dist = mink
                    min1 = i
                    min2 = j
    
    #least similar
    plt.figure()
    pd.Series(biglist[max1]).plot(label=(top_100['FullName'][max1], int(masterAge['Average_Age'][max1])))
    pd.Series(biglist[max2]).plot(label=(top_100['FullName'][max2], int(masterAge['Average_Age'][max2])))
    plt.title("Least Similar")
    plt.xlabel('Year Intervals')
    plt.ylabel('Frequency')
    plt.legend()
    plt.show()

    #most similar
    plt.figure()
    pd.Series(biglist[min1]).plot(label=(top_100['FullName'][min1], int(masterAge['Average_Age'][min1])))
    pd.Series(biglist[min2]).plot(label=(top_100['FullName'][min2], int(masterAge['Average_Age'][min2])))
    plt.title("Most Similar")
    plt.xlabel('Year Intervals')
    plt.ylabel('Frequency')
    plt.legend()
    plt.show()

warnings.filterwarnings("ignore")

timeSeries()
#getAverageAge()

'''
We attempted Jaccard but the results came out very strangely. We decided that it was trivial to our analysis.
'''

'''
def jaccard(c1, c2):
    intersect = set(c1).intersection(c2)
    union = set(c1).union(c2)
    return len(intersect) / len(union)

num = getAllStarApp()
years = PlayerAll()
years['FullName'] = years[['nameFirst', 'nameLast']].apply(lambda x: ' '.join(x), axis=1)
del years['nameFirst']
del years['nameLast']

#years["yearID"] = pd.to_datetime(years["yearID"])
years['yearID'] = pd.to_datetime(pd.Series(years['yearID']), format = '%Y')
#players' allstar appearances in descending order
sort = num.sort_values(by='Number_All_Star_Appearances', ascending=False)
#pprint.pprint(sort)
#get top 100 players with the most all-star appearances
top_100 = sort.head(100)
top_100 = top_100.reset_index()
#print(top_100)
age = getAverageAge()
masterAge = pd.merge(top_100, age, on='FullName')
result = pd.merge(top_100, years, on='FullName')
del result['teamID']
del result['salary']
#print(result)
biglist = []
for i in range(100):
    #dataframe for just each user
    player = result.loc[result['FullName'] == top_100['FullName'][i]]
    del player['index']
    player.index = player['yearID']
    player['num'] = 1
    #print(player)
    month = player.num.resample('5A').sum()
    #month.plot()
    #print(month)
    months_of_users = month.fillna(0).tolist()
    biglist.append(months_of_users)

min1 = 0
max1 = 0
min2 = 0
max2 = 0
min_dist = 5000
max_dist = 0
for i in range(len(biglist)):
    for j in range(len(biglist)):
        if (i != j and len(biglist[i]) == len(biglist[j])):
            jac = jaccard(biglist[i], biglist[j])
            if (jac > max_dist):
                max_dist = jac
                max1 = i
                max2 = j
            if (jac < min_dist):
                min_dist = jac
                min1 = i
                min2 = j
                
#least dissimilar
plt.figure()
pd.Series(biglist[max1]).plot(label=(top_100['FullName'][max1], int(masterAge['Average_Age'][max1])))
pd.Series(biglist[max2]).plot(label=(top_100['FullName'][max2], int(masterAge['Average_Age'][max2])))
plt.title("Most Similar (Least Dissimilar)")
plt.xlabel('Year Intervals')
plt.ylabel('Frequency')
plt.legend()
plt.show()

#most dissimilar
plt.figure()
pd.Series(biglist[min1]).plot(label=(top_100['FullName'][min1], int(masterAge['Average_Age'][min1])))
pd.Series(biglist[min2]).plot(label=(top_100['FullName'][min1], int(masterAge['Average_Age'][min2])))
plt.title("Least Similar (Most Dissimilar)")
plt.xlabel('Year Intervals')
plt.ylabel('Frequency')
plt.legend()
plt.show()
'''
