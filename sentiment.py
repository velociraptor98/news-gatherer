import pandas as pd
from pprint import pprint
import json
from nltk.sentiment.vader import SentimentIntensityAnalyzer as SIA
import csv
from matplotlib import pyplot as plt
import seaborn as sns



def addHeader(fileName):
    row=['Headline','Link','Source']
    with open(fileName,'w')as csvFile:
        writer=csv.writer(csvFile)
        writer.writerow(row)
    csvFile.close()


with open('data.json','r') as fp:
    temp=json.load(fp)
headlines=[]
for i in temp:
    headlines.append(i)
sia=SIA()
results=[]
for line in headlines:
    pol_score=sia.polarity_scores(line)
    pol_score['headline']=line
    results.append(pol_score)
#>0.2 compound score as positive
#<-0.2 compound score as negative
df=pd.DataFrame.from_records(results)
df.head()
df['label']=0
df.loc[df['compound']>0.2,'label']=1
df.loc[df['compound']<-0.1,'label']=-1
df2 = df[['headline','label']]
addHeader('positive.csv')
addHeader('neutral.csv')
addHeader('negative.csv')

positive=[]
neutral=[]
negative=[]
# i - columns 
# rows - rows
for i, rows in df2.iterrows():
    if(rows['label']==1):
        positive.append(rows['headline'])
        positive.extend(temp[rows['headline']])
        with open('positive.csv','a') as csvFile:
            writer=csv.writer(csvFile)
            writer.writerow(positive)
        csvFile.close()
        positive.clear()
    elif(rows['label']==0):
        neutral.append(rows['headline'])
        neutral.extend(temp[rows['headline']])
        with open('neutral.csv','a') as csvFile:
            writer=csv.writer(csvFile)
            writer.writerow(neutral)
        csvFile.close()
        neutral.clear()
    else:
        negative.append(rows['headline'])
        negative.extend(temp[rows['headline']])
        with open('negative.csv','a') as csvFile:
            writer=csv.writer(csvFile)
            writer.writerow(negative)
        csvFile.close()
        negative.clear()
#number of positive neutral and negative headlines
df2.to_csv('output_data.csv',encoding='utf-8',index=False) 
fig,ax=plt.subplots(figsize=(8,8))
counts=df.label.value_counts(normalize=True)*100
sns.barplot(x=counts.index,y=counts,ax=ax)
ax.set_xticklabels(['Negative','Neutral','Positive'])
ax.set_ylabel('Percentage')
fig.savefig('data.png')




