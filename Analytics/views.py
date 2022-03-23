from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import pandas as pd
import numpy as np
import csv
import os
from profiles.models import *
import plotly
import plotly.express as px
import os
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from .models import Academics
from profiles.models import School





def happiness_index():

    df = pd.read_csv("Analytics\data\HI.csv").iloc[:,:-1]
    df_actual = pd.read_csv("Analytics\data\student_data.csv")
    features = df_actual.iloc[:,:-1]
    number_of_students = len(df[df["Who is filling this form?"] == "Student"])
    number_of_teachers = len(df[df["Who is filling this form?"] == "Teacher"])
    number_of_counsellors = len(df[df["Who is filling this form?"] == "Counsellor"])
    number_categories= {"Students": number_of_students,
                        "Teachers": number_of_teachers,
                        "Counsellors": number_of_counsellors}
    ratings_students = df[df["Who is filling this form?"] == "Student"].drop(["Timestamp", "Who is filling this form?"],axis =1)
    ratings_teachers = df[df["Who is filling this form?"] == "Teacher"].drop(["Timestamp", "Who is filling this form?"], axis =1)
    ratings_counsellors = df[df["Who is filling this form?"] == "Counsellor"].drop(["Timestamp", "Who is filling this form?"],
                                                                                   axis =1)
    ratings = {"Students": ratings_students,
                "Teachers": ratings_teachers,
                "Counsellors": ratings_counsellors}
    normalized_ratings = normalize_ratings(ratings)
    weights = calculate_weights(number_categories,normalized_ratings)
    happiness_index = 0
    print(features.shape)
    for i in range(features.shape[0]):
        intermediate = weights*features.iloc[i,:]
        happiness_index += intermediate.values.sum() * 10 **(-1* np.log(intermediate.values.sum()))
        # weights*features[i,:].values
    happiness_index = happiness_index/features.shape[0]

    happiness_index = happiness_index* 10 ** np.log(happiness_index.sum())

    happiness_index = happiness_index* 10 ** np.log(intermediate.sum())

    print(happiness_index)
    # happiness_index = happiness_index* 10 **(-1* np.log(happiness_index))
    print(request.user)
    school = School.objects.filter(user__slug = request.user.slug)[0]
    print(school)
    school.happiness_score = happiness_index
    school.save()
    # print(happiness_index.sum())
    # print(np.log(happiness_index.sum()))











def calculate_weights(number_categories, normalized_ratings):
    weight_students = []
    weight_teachers = []
    weight_counsellors = []
    total = 0
    for name, count in number_categories.items():
        nr = normalized_ratings.get(name)
        print("Hello")
        print(nr)
        for i in range(nr.shape[1]):
            if name == "Students":
                weight_students.append(count*nr.iloc[:,i].sum())
            elif name == "Teachers":
                weight_teachers.append(count*nr.iloc[:,i].sum())
            else:
                weight_counsellors.append(count*nr.iloc[:,i].sum())
            total += count

    weight_student = np.array(weight_students)
    weight_teacher = np.array(weight_teachers)
    weight_counsellor = np.array(weight_counsellors)
    weights = (weight_student + weight_teacher + weight_counsellor)/total
    return weights


def normalize_ratings(rating):
    for name,ratings in rating.items():
        means = ratings.mean()
        sd = ratings.std()
        for i in range(len(ratings.columns)):
            ratings.iloc[:,i] = ratings.iloc[:,i].apply(lambda x: (x-means.iloc[i])/sd.iloc[i])
    print(rating)
    return rating

def ranking():
    pass

def dashboard(request):
    df = pd.read_csv('Analytics/data/Parents Feedback (Responses) - Form Responses 1.csv')
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

    # color_discrete_map = { 'Open': 'rgb(255,0,0)'}
    fig = go.Figure(data=[go.Pie(labels=labels, values=sizes)])
    graph1 = plotly.offline.plot(fig, auto_open=False, output_type="div")
    fig = px.bar(df['Steps taken to spread awareness about mental health'])
    graph2 = plotly.offline.plot(fig, auto_open=False, output_type="div")
    fig = px.box(df, y=['How self confident are your children ?'])
    graph3 = plotly.offline.plot(fig, auto_open=False, output_type="div")
 #   fig = px.line(coin_data, x="Date", y=coin_data.columns[3:4], width=1050, height=500)
 #   graph4 = plotly.offline.plot(fig, auto_open=False, output_type="div")
    context = {"graph": [graph1, graph2, graph3]}
    return render(request,'Analytics/dashboard.html',context)

def upload_csv(request):
    if request.method == "POST":
        csv = request.FILES['csv']
        # print(csv.read().decode())
        for i,line in enumerate(csv.read().decode().splitlines()):
            if i == 0:
                continue
            elements = line.split(',')
            print(request.user)
            p = Academics(school = request.user.school,name=elements[0], email=elements[1], english = elements[2])
            p.save()
            happiness_index()
    return render(request, 'Analytics/dashboard.html')

def send(request):
    school = School.objects.get(user__slug = request.user.school)
    print(school)
    return render(request, 'Analytics/dashboard.html')