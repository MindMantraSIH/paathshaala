from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import pandas as pd
import numpy as np



def happiness_index(request):
    df = pd.read_csv("")
    df_actual = pd.read_csv("")
    features = df_actual.iloc[:, 0]
    number_of_students = len(df[df["Category"] == "Student"])
    number_of_teachers = len(df[df["Category"] == "Teachers"])
    number_of_counsellors = len(df[df["Category"] == "Counsellors"])
    number_categories= {"Students": number_of_students,
                        "Teachers": number_of_teachers,
                        "Counsellors": number_of_counsellors}
    ratings_students = df[df["Category"] == "Student"].drop()
    ratings_teachers = df[df["Category"] == "Teachers"].drop()
    ratings_counsellors = df[df["Category"] == "Counsellors"].drop()
    ratings = {"Students": ratings_students,
                "Teachers": ratings_teachers,
                "Counsellors": ratings_counsellors}
    normalized_ratings = normalize_ratings(ratings)
    weights = calculate_weights(number_categories,normalized_ratings)

    happiness_index = weights*features


def calculate_weights(number_categories, normalized_ratings):
    weight_students = []
    weight_teachers = []
    weight_counsellors = []
    total = 0
    for name, count in number_categories.items():
        nr = normalized_ratings.get(name)
        for i in range(len(nr)):
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
            ratings.iloc[:,i] = ratings.iloc[:,i].apply(lambda x: (x-means[1,i])/sd)
    return rating

def ranking():
    pass

