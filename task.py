import plotly
import plotly.graph_objs as go
doc = "results.csv"

def getDataset(files, dataset = dict(), counter = 1):

    doc = files.readlines()
    while counter != len(doc):
        game_number = "game "+str(counter)
        values = doc[counter].split(",")
        if values[5] in dataset:
            if values[4] in dataset[values[5]]:
                dataset[values[5]][values[4]][game_number] = {values[0] : int(float(values[2])), values[1]: int(float(values[3]))}
            else:
                dataset[values[5]][values[4]] = {game_number : {values[0] : int(float(values[2])), values[1]: int(float(values[3]))}}
        else:
            dataset[values[5]] = {values[4] : {game_number : {values[0] : int(float(values[2])), values[1]: int(float(values[3]))}}}
        counter+=1
    print(counter)
    return dataset

def totalGoals(dataset, total_dict = dict(), team_set = set()):
    for season in dataset:
        for result in dataset[season]:
            numbers = list(dataset[season][result].keys())
            for game in numbers:
                team_set.update(set(dataset[season][result][game].keys()))
    for team in team_set:
        counter = 1
        for season in dataset:
            for result in dataset[season]:
                numbers = list(dataset[season][result].keys())
                for game in numbers:
                    if team in dataset[season][result][game].keys():
                        counter += int(float(dataset[season][result][game][team]))
        total_dict[team] = counter
    bar = [go.Bar(x = list(total_dict.keys()), y = list(total_dict.values()))]
    return plotly.offline.plot(bar, filename = "bar.html")

def  allResults(dataset, total_dict = dict(), total_set = set()):
    for season in dataset:
        total_set.update(dataset[season].keys())
    for result in total_set:
        counter = 0
        for season in dataset:
            counter += len(dataset[season][result].keys())
        total_dict[result] = counter
    pie = [go.Pie(labels = list(total_dict.keys()), values = list(total_dict.values()))]
    return plotly.offline.plot(pie, filename = "pie.html")

def draws(dataset, total_dict = dict()):
    seasons = list(dataset.keys())
    for season in seasons:
        total_dict[season] = len(list(dataset[season]["H"].keys()))
    trace  = [go.Scatter(x = list((total_dict.keys())), y = list(total_dict.values()))]
    return plotly.offline.plot(trace, filename = "trace.html")

doc = "results.csv"
with open(doc, encoding="utf-8", mode='r') as doc:
    a = getDataset(doc)
    totalGoals(a)
    allResults(a)
    draws(a)