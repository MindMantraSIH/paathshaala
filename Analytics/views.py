from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import pandas as pd
import numpy as np



def happiness_index(request):
    df = pd.read_csv("Analytics\data\HI.csv").iloc[:,:-1]
    df_actual = pd.read_csv("Analytics\data\student_data.csv")
    features = df_actual.iloc[1,:-1]
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
    happiness_index = weights*features.values
    print(happiness_index.sum())
    print(np.log(happiness_index.sum()))
    print(happiness_index.sum()*10**np.log(happiness_index.sum()))

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

