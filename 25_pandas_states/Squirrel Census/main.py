import pandas

data = pandas.read_csv("2018_Central_Park_Squirrel_Census_-_Squirrel_Data.csv")

squirrel_count = data["Primary Fur Color"].value_counts()

print(squirrel_count)

data = pandas.DataFrame(squirrel_count)

print(data)

data.to_csv("squirrel_count.csv")