# from sklearn.datasets.samples_generator import make_blobs
#
# # creating datasets X containing n_samples
# # Y containing two classes
# X, Y = make_blobs(n_samples=500, centers=2,
#                   random_state=0, cluster_std=0.40)
# import matplotlib.pyplot as plt
#
# # plotting scatters
# plt.scatter(X[:, 0], X[:, 1], c=Y, s=50, cmap='spring');
# plt.show()
#


import pandas as pd

import matplotlib.pyplot as plt

# csv_path  = "G:\Ajith\Others\Ajith-self-emp\Image-classification\Training_set.csv"
csv_path  = "G:\Ajith\Others\Ajith-self-emp\Image-classification\med_Training_set.csv"
# csv_path  = "https://raw.githubusercontent.com/fivethirtyeight/data/master/college-majors/recent-grads.csv"
df = pd.read_csv(csv_path)
print('type :',type(df))
# print('df.head() :',df.head())
# df.plot(x="Rank", y=['Major_code','Major','Total','Men','Women','Major_category','ShareWomen','Sample_size','Employed','Full_time','Part_time','Full_time_year_round','Unemployed','Unemployment_rate','Median','P25th','P75th','College_jobs','Non_college_jobs','Low_wage_jobs'])
# df.plot(x="Rank", y=["P25th", "Median", "P75th"]).area()
# df.area(x='Rank', y=['P25th', 'Median', 'P75th'])
# df.bar(x='Rank', y=['P25th', 'Median', 'P75th'])
# df.barh(x='Rank', y=['P25th', 'Median', 'P75th'])
# df.box(x='Rank', y=['P25th', 'Median', 'P75th'])
# df.hexbin(x='Rank', y=['P25th', 'Median', 'P75th'])
# df.hist(x='Rank', y=['P25th', 'Median', 'P75th'])
# df.kde(x='Rank', y=['P25th', 'Median', 'P75th'])
# df.density(x='Rank', y=['P25th', 'Median', 'P75th'])
# df.line(x='Rank', y=['P25th', 'Median', 'P75th'])
# df.pie(x='Rank', y=['P25th', 'Median', 'P75th'])
# df.scatter(x='Rank', y=['P25th', 'Median', 'P75th'])

# df.plot().area()



df.plot(x="Subject ID",y=['Age','Gender'])
plt.show()
