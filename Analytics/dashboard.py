import pandas as pd
import numpy as np
import seaborn as sns
from matplotlib import pyplot as plt

def analytics(request):
    df = pd.read_csv('/content/Parents Feedback (Responses) - Form Responses 1.csv')
    anx = df[df['Anxiety and pressure felt by students during exams'] > 3]
    number_of_anxious = anx['Anxiety and pressure felt by students during exams'].count()
    soc = df[df['How socially active are your children ?'] < 3]
    nuumber_of_soc_active = soc['How socially active are your children ?'].count()
    self_conf = df[df['How self confident are your children ?'] < 3]
    number_of_low_confid = self_conf['How self confident are your children ?'].count()
    sub_col = ['How satisfied are you with school ', 'Schools emphasis on practical learning',
               'Curriculums emphasis on life and social skills']
    box_df = df['How satisfied are you with school ']

    to_plot = {'Number of Anxious Students': number_of_anxious, 'Less Socially Active': nuumber_of_soc_active,
               'Less Confident': number_of_low_confid}
    labels = []
    sizes = []
    for x, y in to_plot.items():
        labels.append(x)
        sizes.append(y)
    fig = plt.figure(figsize=(28, 20))
    ax1 = plt.subplot2grid((2, 2), (0, 0))
    box_df.plot.box()
    ax1 = plt.subplot2grid((2, 2), (0, 1))
    plt.pie(sizes, labels=labels)
    plt.legend(loc='upper left')
    ax1 = plt.subplot2grid((2, 2), (1, 0))
    sns.countplot(df['Steps taken to spread awareness about mental health'])
    ax1 = plt.subplot2grid((2, 2), (1, 1))
    sns.countplot(df['Steps taken to spread awareness about Physical health'])
    plt.show()