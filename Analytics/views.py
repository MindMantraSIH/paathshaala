from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
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
from profiles.models import School, Student
import smtplib
from suggestions.models import Data
from django.conf import settings
from django.core.mail import send_mail
import os
import csv
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.decomposition import NMF, LatentDirichletAllocation
import pickle as pkl
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.http import JsonResponse



def happiness_index(request):
    output = []
    print(request.user)
    query_set = Data.objects.filter(school=request.user.school)
    print(query_set)
    with open(os.getcwd() + "/data.csv", 'w',newline='') as file:
        writer = csv.writer(file)
        print(os.getcwd())
        writer.writerow(['Level Of Courses (Difficulty)', 'Standard','A Clean Environment',
       'Employing teachers with competency',
       'Preventing Discrimination and Persuasion',
       'Providing laboratory & workshop facilities', 'The school timetable',
       'Performing group work', 'Mental health assessment of all students',
       'Presenting more sporting & artistic classes',
       'Being able to solve problems of the learner',
       'Courses should have creative and colorful instructional materials and fun activities.',
       'Focus on the individual',
       'Involve with fundamental and critical aspects of learner , about manner of living',
       'Course relevance',
       'Issues of concern should be made a point of conversation within age appropriate classrooms and children made aware of existing realities.',
       'Are these problems being solved by the School?',
       'Any other factors , according to you , which contribute to happiness index'])
        for user in query_set:
            print("Im here")
            print(user)
            output.append([user.levelc, user.std, user.env, user.teachersc, user.prevdisc, user.fecilities, user.timetable,
                       user.grpwork, user.mentalhlth, user.sportart, user.solveprob, user.creativecourse,
                       user.foconindv, user.mannlearn, user.courserele, user.issuesofconc, user.aresolved, user.others])
        writer.writerows(output)
    print()
    df = pd.read_csv("Analytics\data\HI.csv").iloc[:,:-1]
    df_actual = pd.read_csv(os.getcwd() + "/data.csv")
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

    print(weights)
    print(type(weights))
    print(len(weights))
    happiness_index = 0
    print(features.shape)
    for i in range(features.shape[0]):
        intermediate = weights*features.drop(["Standard"],axis =1).iloc[i,:]
        happiness_index += intermediate.values.sum() * 10 **(-1* np.log(intermediate.values.sum()))
        # weights*features[i,:].values
    happiness_index = np.log(abs(happiness_index)/features.shape[0])

    # happiness_index = happiness_index* 10 ** np.log(happiness_index.sum())

    print(happiness_index)
    # happiness_index = happiness_index* 10 **(-1* np.log(happiness_index))
    print(request.user)
    school = School.objects.filter(user__slug = request.user.slug)[0]
    print(school)
    school.happiness_score = happiness_index
    school.save()
    # print(happiness_index.sum())
    # print(np.log(happiness_index.sum()))

    def standard_Happiness(features, weights):
        hi_standard = ""
        fn = len(features)
        print(fn)
        for std in range(1,11):
            happiness_index = 0
            print(features)
            features = features[features["Standard"] == std]
            print(features)
            print(features.shape[0])
            for i in range(features.shape[0]):
                intermediate = weights * features.drop(["Standard"], axis=1).iloc[i, :]
                happiness_index += intermediate.values.sum() * 10 ** (-1 * np.log(intermediate.values.sum()))
                # weights*features[i,:].values
            print(features)
            happiness_index = np.log(abs(happiness_index)/ fn)
            hi_standard += str(happiness_index) + " "
        return hi_standard

    # std_happiness = standard_Happiness(features,weights)
    # print(std_happiness)
    # school.standard_HI = std_happiness
    # school.save()







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
    schools = School.objects.all().order_by('-happiness_score')
    for i,school in enumerate(schools):
        school.rank = i+1
        school.save()



def dashboard(request):
    df = pd.read_csv('Analytics/data/HI.csv')
    label = []
    sizes = []
    total_suggestions = Data.objects.filter(school = request.user.school).count()
    total_students = Student.objects.filter(school = request.user.school).count()
    diff = df[df['Level Of Courses (Difficulty)'] > 2]
    students_course_difficult = diff['Level Of Courses (Difficulty)'].count()
    eas = df[df['Level Of Courses (Difficulty)'] <= 2]
    students_course_easy = eas['Level Of Courses (Difficulty)'].count()
    # students_course_easy += 1
    print(students_course_easy)
    to_plot = {'Students finding course difficult': students_course_difficult,
               'Students finding Course Easy': students_course_easy}
    fig0 = go.Figure(data=go.Scatterpolar(
        r=[df['A Clean Environment'].mean(), df['Providing laboratory & workshop facilities'].mean(),
           df['The school timetable'].mean(), df['Presenting more sporting & artistic classes'].mean(),
           df['Being able to solve problems of the learner'].mean()],
        theta=['A Clean Environment', 'Providing laboratory & workshop facilities',
               'Effectiveness of school timetable', 'Presenting more sporting & artistic classes',
               'Quality of doubt resolution'],
        fill='toself'
    ))

    fig0.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True
            ),
        ),
        showlegend=False
    )

    features = ['Level Of Courses (Difficulty)', 'Course relevance',
               'Critical learning of the learner']

    fig1 = go.Figure(data=[
        go.Bar(name='Rated greater than 2', x=features, y=[students_course_difficult,
                                                           len(df[df['Course relevance'] > 2]),
       len(df[df['Involve with fundamental and critical aspects of learner , about manner of living'] > 2])]),
        go.Bar(name='Rated lower than or equal to 2', x=features, y=[students_course_difficult,
                                                           len(df[df['Course relevance'] <= 2]),
       len(df[df['Involve with fundamental and critical aspects of learner , about manner of living'] <= 2])])])
    # Change the bar mode
    fig1.update_layout(barmode='group')

    graph1 = plotly.offline.plot(fig0, auto_open=False, output_type="div")
    fig = go.Figure(data=[go.Pie(labels=label, values=sizes)])
    graph2 = plotly.offline.plot(fig1, auto_open=False, output_type="div")

    fig3 = go.Figure(data=[go.Pie(labels=["<1","2-3","3-4","4-5"],
                                 values=[len(df[df['Mental health assessment of all students'] <= 1]),
                                         len(df[(df['Mental health assessment of all students'] > 1) &
                                                (df['Mental health assessment of all students'] <= 2)]),
                                         len(df[(df['Mental health assessment of all students'] > 2) &
                                                (df['Mental health assessment of all students'] <= 3)]),
                                         len(df[(df['Mental health assessment of all students'] > 3) &
                                                (df['Mental health assessment of all students'] <= 4)]),
                                         len(df[(df['Mental health assessment of all students'] > 4) &
                                                (df['Mental health assessment of all students'] <= 5)])
                                         ],
                    pull=[0.3, 0, 0, 0])])

    graph3 = plotly.offline.plot(fig3, auto_open=False, output_type="div")
    fig4 = go.Figure(data=go.Scatter(x=['Discrimination prevention',
                                        'Group Performance',
                                        'Extracurriculars',
                                        'Individual attention',
                                        'Problems solved',
                                        'Age-based conversations'
                                        ], y=[df['Preventing Discrimination and Persuasion'].mean(),
                                              df['Performing group work'].mean(),
                                              df['Presenting more sporting & artistic classes'].mean(),
                                              df['Focus on the individual'].mean(),
                                              df['Are these problems being solved by the School?'].mean(),
                                              df['Issues of concern should be made a point of conversation within age appropriate classrooms and children made aware of existing realities.'].mean()])
                     )
    graph4 = plotly.offline.plot(fig4, auto_open=False, output_type="div")

    context = {"graph": [graph1, graph2, graph3,graph4],
               'name': request.user.school,
                'city': request.user.school.city,
                'state': request.user.school.state,
               'rank': request.user.school.rank,
               'happinessindex': request.user.school.happiness_score,
               'total_suggestions':total_suggestions,
               'total_students': total_students,
               'school_user_id': request.user.id
               }
    return render(request,'Analytics/dashboard1.html',context)

def send_feedback_mails(request):
    school_user = request.POST['school']
    school = School.objects.get(user_id = school_user)
    msg_plain = render_to_string('analytics/send_feedback_email.txt')
    student_emails = []
    students = Student.objects.filter(school=school)
    for student in students:
        if student.user.email:
            student_emails.append(student.user.email)
    try:
        send_mail(
            'Fill Feedback Form',
            msg_plain,
            'mindmantrasih@gmail.com', #sender
            student_emails,
            html_message=render_to_string('analytics/send_feedback_email.html'),
        )
        return JsonResponse({'response':'success'})
    except Exception as e:
        print(e)
        return JsonResponse({'response':'failure'})
    

def upload_csv(request):
    if request.method == "POST":
        csv = request.FILES['csv']
        # print(csv.read().decode())
        lines = csv.read().decode().split('\r\n')
        print(lines)
        for i,line in enumerate(lines):
            # try:
            print(line)
            if i == 0 or i == len(lines) -1:
                continue
            elements = line.split(',')
            print(elements)
            school_obj = School.objects.get(user = request.user)
            student_obj = Student.objects.filter(school = school_obj, roll_number=elements[0], std=elements[2], division=elements[3])[0]
            p = Academics.objects.create(school = request.user.school,
                                        student = student_obj,
                                         roll_no= str(request.user.school) + " " +
                                                  elements[2] + " " +elements[3]
                                                  + " " +elements[0] + " " + elements[19],
                                         name=elements[1], standard = elements[2], division= elements[3],
                                         english = float(elements[4]), hindi = float(elements[5]),
                                         maths=float(elements[6]), science=float(elements[7]),
                                         history= float(elements[8]),
                                         geo=float(elements[9]),percent=float(elements[10]),
                                         interactivity=float(elements[11]),
                                         timely_submissions=float(elements[12]),
                                         attentiveness=float(elements[13]), creativity=float(elements[14]),
                                         participation=float(elements[15]), confidence=float(elements[16]),
                                         social_relationship=float(elements[17]), obedience=float(elements[18])
                                         )
            print("Hello",p)
            request
            # except:
            #     pass
        print("hulllllllllllllllllllllllaaaaaaaaaaaaaaaaaaaarrrrrrrrrrrrrrrrrrrrrrraaaaaaaaaaaaaaaaaaaaaaaaa")
        happiness_index(request)
        ranking()
        s = suggest()
    df = pd.read_csv('Analytics/data/HI.csv')
    label = []
    sizes = []
    diff = df[df['Level Of Courses (Difficulty)'] > 2]
    students_course_difficult = diff['Level Of Courses (Difficulty)'].count()
    eas = df[df['Level Of Courses (Difficulty)'] <= 2]
    students_course_easy = eas['Level Of Courses (Difficulty)'].count()
    # students_course_easy += 1
    print(students_course_easy)
    to_plot = {'Students finding course difficult': students_course_difficult,
               'Students finding Course Easy': students_course_easy}
    fig0 = go.Figure(data=go.Scatterpolar(
        r=[df['A Clean Environment'].mean(), df['Providing laboratory & workshop facilities'].mean(),
           df['The school timetable'].mean(), df['Presenting more sporting & artistic classes'].mean(),
           df['Being able to solve problems of the learner'].mean()],
        theta=['A Clean Environment', 'Providing laboratory & workshop facilities',
               'Effectiveness of school timetable', 'Presenting more sporting & artistic classes',
               'Quality of doubt resolution'],
        fill='toself'
    ))

    fig0.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True
            ),
        ),
        showlegend=False
    )

    features = ['Level Of Courses (Difficulty)', 'Course relevance',
                'Critical learning of the learner']

    fig1 = go.Figure(data=[
        go.Bar(name='Rated greater than 2', x=features, y=[students_course_difficult,
                                                           len(df[df['Course relevance'] > 2]),
                                                           len(df[df[
                                                                      'Involve with fundamental and critical aspects of learner , about manner of living'] > 2])]),
        go.Bar(name='Rated lower than or equal to 2', x=features, y=[students_course_difficult,
                                                                     len(df[df['Course relevance'] <= 2]),
                                                                     len(df[df[
                                                                                'Involve with fundamental and critical aspects of learner , about manner of living'] <= 2])])])
    # Change the bar mode
    fig1.update_layout(barmode='group')

    graph1 = plotly.offline.plot(fig0, auto_open=False, output_type="div")
    fig = go.Figure(data=[go.Pie(labels=label, values=sizes)])
    graph2 = plotly.offline.plot(fig1, auto_open=False, output_type="div")

    fig3 = go.Figure(data=[go.Pie(labels=["<1", "2-3", "3-4", "4-5"],
                                  values=[len(df[df['Mental health assessment of all students'] <= 1]),
                                          len(df[(df['Mental health assessment of all students'] > 1) &
                                                 (df['Mental health assessment of all students'] <= 2)]),
                                          len(df[(df['Mental health assessment of all students'] > 2) &
                                                 (df['Mental health assessment of all students'] <= 3)]),
                                          len(df[(df['Mental health assessment of all students'] > 3) &
                                                 (df['Mental health assessment of all students'] <= 4)]),
                                          len(df[(df['Mental health assessment of all students'] > 4) &
                                                 (df['Mental health assessment of all students'] <= 5)])
                                          ],
                                  pull=[0.3, 0, 0, 0])])

    graph3 = plotly.offline.plot(fig3, auto_open=False, output_type="div")
    fig4 = go.Figure(data=go.Scatter(x=['Discrimination prevention',
                                        'Group Performance',
                                        'Extracurriculars',
                                        'Individual attention',
                                        'Problems solved',
                                        'Age-based conversations'
                                        ], y=[df['Preventing Discrimination and Persuasion'].mean(),
                                              df['Performing group work'].mean(),
                                              df['Presenting more sporting & artistic classes'].mean(),
                                              df['Focus on the individual'].mean(),
                                              df['Are these problems being solved by the School?'].mean(),
                                              df[
                                                  'Issues of concern should be made a point of conversation within age appropriate classrooms and children made aware of existing realities.'].mean()])
                     )
    graph4 = plotly.offline.plot(fig4, auto_open=False, output_type="div")
    r = lda()
    context = {"graph": [graph1, graph2, graph3,graph4],
        'name': request.user.school,
        'city': request.user.school.city,
        'state': request.user.school.state,
        'rank': request.user.school.rank,
        'happinessindex': request.user.school.happiness_score,
        'improve': s,
               'topic': r
    }
    #print(context.name)
    return render(request, 'Analytics/dashboard1.html',context)

def send(request):
    school = School.objects.filter(user= request.user)[0]
    academics = Academics.objects.filter(school = school)
    email_list = []
    for acad in academics:
        email_list.append(acad.email)
    print(email_list)
    subject = 'Request to fill survey form'
    message = "Please login and fill the form."
    email_from = settings.EMAIL_HOST_USER
    send_mail(subject, message, email_from, email_list)

    df = pd.read_csv('Analytics/data/HI.csv')
    label = []
    sizes = []
    diff = df[df['Level Of Courses (Difficulty)'] > 2]
    students_course_difficult = diff['Level Of Courses (Difficulty)'].count()
    eas = df[df['Level Of Courses (Difficulty)'] <= 2]
    students_course_easy = eas['Level Of Courses (Difficulty)'].count()
    # students_course_easy += 1
    print(students_course_easy)
    to_plot = {'Students finding course difficult': students_course_difficult,
               'Students finding Course Easy': students_course_easy}
    fig0 = go.Figure(data=go.Scatterpolar(
        r=[df['A Clean Environment'].mean(), df['Providing laboratory & workshop facilities'].mean(),
           df['The school timetable'].mean(), df['Presenting more sporting & artistic classes'].mean(),
           df['Being able to solve problems of the learner'].mean()],
        theta=['A Clean Environment', 'Providing laboratory & workshop facilities',
               'Effectiveness of school timetable', 'Presenting more sporting & artistic classes',
               'Quality of doubt resolution'],
        fill='toself'
    ))

    fig0.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True
            ),
        ),
        showlegend=False
    )

    features = ['Level Of Courses (Difficulty)', 'Course relevance',
                'Critical learning of the learner']

    fig1 = go.Figure(data=[
        go.Bar(name='Rated greater than 2', x=features, y=[students_course_difficult,
                                                           len(df[df['Course relevance'] > 2]),
                                                           len(df[df[
                                                                      'Involve with fundamental and critical aspects of learner , about manner of living'] > 2])]),
        go.Bar(name='Rated lower than or equal to 2', x=features, y=[students_course_difficult,
                                                                     len(df[df['Course relevance'] <= 2]),
                                                                     len(df[df[
                                                                                'Involve with fundamental and critical aspects of learner , about manner of living'] <= 2])])])
    # Change the bar mode
    fig1.update_layout(barmode='group')

    graph1 = plotly.offline.plot(fig0, auto_open=False, output_type="div")
    fig = go.Figure(data=[go.Pie(labels=label, values=sizes)])
    graph2 = plotly.offline.plot(fig1, auto_open=False, output_type="div")

    fig3 = go.Figure(data=[go.Pie(labels=["<1", "2-3", "3-4", "4-5"],
                                  values=[len(df[df['Mental health assessment of all students'] <= 1]),
                                          len(df[(df['Mental health assessment of all students'] > 1) &
                                                 (df['Mental health assessment of all students'] <= 2)]),
                                          len(df[(df['Mental health assessment of all students'] > 2) &
                                                 (df['Mental health assessment of all students'] <= 3)]),
                                          len(df[(df['Mental health assessment of all students'] > 3) &
                                                 (df['Mental health assessment of all students'] <= 4)]),
                                          len(df[(df['Mental health assessment of all students'] > 4) &
                                                 (df['Mental health assessment of all students'] <= 5)])
                                          ],
                                  pull=[0.3, 0, 0, 0])])

    graph3 = plotly.offline.plot(fig3, auto_open=False, output_type="div")
    fig4 = go.Figure(data=go.Scatter(x=['Discrimination prevention',
                                        'Group Performance',
                                        'Extracurriculars',
                                        'Individual attention',
                                        'Problems solved',
                                        'Age-based conversations'
                                        ], y=[df['Preventing Discrimination and Persuasion'].mean(),
                                              df['Performing group work'].mean(),
                                              df['Presenting more sporting & artistic classes'].mean(),
                                              df['Focus on the individual'].mean(),
                                              df['Are these problems being solved by the School?'].mean(),
                                              df[
                                                  'Issues of concern should be made a point of conversation within age appropriate classrooms and children made aware of existing realities.'].mean()])
                     )
    graph4 = plotly.offline.plot(fig4, auto_open=False, output_type="div")
    context = {"graph": [graph1, graph2, graph3,graph4],
        'name': request.user.school,
        'city': request.user.school.city,
        'state': request.user.school.state,
        'rank': request.user.school.rank,
        'happinessindex': request.user.school.happiness_score,
    }
    return render(request, 'Analytics/dashboard1.html1', context)

def lda():
    schools = Data.objects.all()
    suggestions = []
    for i, school in enumerate(schools):
        suggestions.append(school.others)
    print(suggestions)
    no_features = 1000
    tf_vectorizer = CountVectorizer(max_features=no_features, stop_words='english')
    tf = tf_vectorizer.fit_transform(suggestions)
    tf_feature_names = tf_vectorizer.get_feature_names()
    no_topics = 1
    lda = LatentDirichletAllocation(no_topics, max_iter=5, learning_method='online', learning_offset=50.,
                                    random_state=0).fit(tf)

    def display_topics(model, feature_names, no_top_words):
        for topic_idx, topic in enumerate(model.components_):
            print("Topic %d:" % (topic_idx))
            return " ".join([feature_names[i]
                        for i in topic.argsort()[:-no_top_words - 1:-1]])

    no_top_words = 5
    display_topics(lda, tf_feature_names, no_top_words)


def suggest():
    suggestions = {0: 'Reduce the difficulty level & Make sure Students learn efficiently',
                   1: 'Clean Environment keeps student at ease , Strive to keep the place hospitable',
                   2: ' Teachers are one of the most imp role models in a students life , So capable and competent teachers are a must – make sure the right teachers are selected and trained',
                   3: 'Students being at a very impressionable age ,making sure their self confidence doesn’t go down is very important . Spread awareness about it ,try to make sure no student goes through it ,and if goes through – give proper councelling',
                   4: 'Studies show students learn and understand better with doing , hence emphasize on practical and hands on training',
                   5: 'Plan the time table in an efficient way such that students have enough break between lectures',
                   6: 'Plan more group based activites so that the interaction of students increases ',
                   7: 'Take frequent mental health assesment of students , detecting problems at an early stage can do a lot of good',
                   8: 'Plan more extra-curricular activities , helps students build a lot of life skills ',
                   9: 'Try to clear all the doubts of students , as students with a strong knowledge base become very keen of learning',
                   10: 'Courses should have creative and colorful instructional materials and fun activities',
                   11: 'Focus on the individual as every student should be mentored in a different way ',
                   12: 'Involve with fundamental and critical aspects of learner , about manner of living ',
                   13: 'Introduce relevant courses which can help the students ini life',
                   14: 'Issues of concern should be made a point of conversation within age appropriate classrooms and children made aware of existing realities',

                   }

    df_actual = pd.read_csv(os.getcwd() + "/data.csv")
    features = df_actual.iloc[:, :-1].mean().values
    improvements = []
    for i,feature in enumerate(features):
        if feature < 2.5:
            improvements.append(suggestions.get(i,""))
    # os.remove(os.getcwd() + "/data.csv")
    return improvements



def standard_analytics(request, std):
    output = []
    query_set = Academics.objects.filter(school=request.user.school,standard=std)
    print(query_set)
    with open(os.getcwd() + "/standard_data.csv", 'w', newline='') as file:
        writer = csv.writer(file)
        print(os.getcwd())
        writer.writerow(['Roll_number', 'Name', 'School', 'Standard', 'Division','English', 'Hindi',
       'Maths', 'Science', 'History', 'Geography', 'Percent',
       'How interactive in class', 'Assignments on time', 'Attentive in class',
       'Creativity', 'Participation in extra curricular', 'Confidence',
       'Social relationships', 'Obedient'])
        for user in query_set:
            print("Im here")
            print(user)
            output.append([user.roll_no, user.name, user.standard, user.division, user.english, user.hindi, user.maths,
                           user.science, user.history, user.geo, user.percent, user.interactivity,
                           user.timely_submissions, user.attentiveness, user.creativity,
                           user.participation, user.confidence, user.social_relationship,
                           user.obedience])
        writer.writerows(output)
    print()
    df = pd.read_csv(os.getcwd() + "/standard_data.csv")
    fig0 = go.Figure(data=go.Scatterpolar(
        r=[df['English'].mean(), df['Hindi'].mean(),
           df['Maths'].mean(), df['Science'].mean(),
           df['History'].mean(), df['Geography'].mean()],
        theta=['English', 'Hindi',
       'Maths', 'Science', 'History', 'Geography'],
        fill='toself'
    ))

    fig0.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True
            ),
        ),
        showlegend=False
    )
    graph1 = plotly.offline.plot(fig0, auto_open=False, output_type="div")

    features = ['How interactive in class', 'Assignments on time', 'Attentive in class',]

    fig1 = go.Figure(data=[
        go.Bar(name='Rated greater than 2', x=features, y=[len(df[df['How interactive in class'] > 2]),
                                                           len(df[df['Assignments on time'] > 2]),
                                                           len(df[df['Attentive in class'] > 2])]),
        go.Bar(name='Rated lower than or equal to 2', x=features, y=[
                                                           len(df[df['How interactive in class'] <= 2]),
                                                           len(df[df['Assignments on time'] <= 2]),
                                                           len(df[df['Attentive in class'] <= 2])])])
    # Change the bar mode
    fig1.update_layout(barmode='group')
    graph2 = plotly.offline.plot(fig1, auto_open=False, output_type="div")

    fig3 = go.Figure(data=[go.Pie(labels=["<1","2-3","3-4","4-5"],
                                 values=[len(df[df['Percent'] <= 20]),
                                         len(df[(df['Percent'] > 20) &
                                                (df['Percent'] <= 40)]),
                                         len(df[(df['Percent'] > 40) &
                                                (df['Percent'] <= 60)]),
                                         len(df[(df['Percent'] > 60) &
                                                (df['Percent'] <= 80)]),
                                         len(df[(df['Percent'] > 80) &
                                                (df['Percent'] <= 100)])
                                         ],
                    pull=[0.3, 0, 0, 0])])

    graph3 = plotly.offline.plot(fig3, auto_open=False, output_type="div")

    fig4 = go.Figure(data=go.Scatter(x=['Creativity',
                                        'Participation in extra curricular',
                                        'Confidence',
                                        'Social relationships',
                                        'Obedient'
                                        ], y=[df['Creativity'].mean(),
                                              df['Participation in extra curricular'].mean(),
                                              df['Confidence'].mean(),
                                              df['Social relationships'].mean(),
                                              df['Obedient'].mean()]))
    graph4 = plotly.offline.plot(fig4, auto_open=False, output_type="div")

    context = {"graph": [graph1, graph2, graph3,graph4],
               'name': request.user.school,
                'city': request.user.school.city,
                'state': request.user.school.state,
               'rank': request.user.school.rank,
               'std':std,
               'happinessindex': request.user.school.happiness_score
               }
    return render(request,"Analytics/standard_dashboard.html",context)
# return render(request, "Analytics/dashboard1.html")


# def dashboard1(request):
#     return render(request, "Analytics/dashboard1.html")

def student_dashboard(request):
    output = []
    print(request.user)
    query_set = Academics.objects.filter(school=request.user.student.school)
    print(query_set)
    with open(os.getcwd() + "/student_data.csv", 'w', newline='') as file:
        writer = csv.writer(file)
        print(os.getcwd())
        writer.writerow(['Roll_number', 'Name', 'Standard', 'Division','English', 'Hindi',
       'Maths', 'Science', 'History', 'Geography', 'Percent',
       'How interactive in class', 'Assignments on time', 'Attentive in class',
       'Creativity', 'Participation in extra curricular', 'Confidence',
       'Social relationships', 'Obedient'])
        for user in query_set:
            print("Im here")
            print(user)
            output.append([user.roll_no, user.name, user.standard, user.division, user.english, user.hindi,
                           user.maths, user.science, user.history, user.geo, user.percent,
                           user.interactivity, user.timely_submissions, user.attentiveness, user.participation,
                           user.confidence,user.social_relationship,user.obedience])
        writer.writerows(output)

    x = Student.objects.get(user=request.user)
    #print(x)

    #print(student)
    student = Student.objects.get(user=request.user)
    user = Data.objects.get(student=student)



    # file = []
    # with open("someobject.pickle", "rb") as input_file:
    #     weights = pkl.loads(input_file)
    #     print(weights)
    # print(weights)
    
    # hi = weights*features.drop(["Standard"],axis =1).iloc[i,:]

    #print(student.std)
    #print(type(student.std))
    standard = int(student.std)
    str_std = student.std
    div = student.division
    year = '2022'
    #print(div)
    rno = student.roll_number
    str_rno = str(student.roll_number)
    school = x.school.user.name
    #roll_no =
    #print(roll_no)
    r = [school,str_std,div,str_rno,'2022']
    roll_no = " ".join(r)
    #print(roll_no)
    #roll_no = str(school +" " + standard +" " + div + " " + rno + "2022")

    df_s = pd.read_csv(os.getcwd() + "/student_data.csv")
    #print(df_s)
    std_df = df_s[df_s['Standard'] == standard]
    #print(std_df)
    div = std_df[std_df['Division'] == div]
    #print(div)
    roll_no_df = div[div['Roll_number'] == roll_no]
    #print(roll_no)
    print(roll_no_df)
    std_mean = std_df['Percent'].mean()
    curr = roll_no_df[roll_no_df['Roll_number'] == roll_no].Percent.values[0]
    res = [std_mean, curr]
    lab = ['Class Average', 'Student"s Percent']
    fig1 = go.Figure([go.Bar(x=lab, y=res)])
    graph1 = plotly.offline.plot(fig1, auto_open=False, output_type="div")
    x = roll_no_df[roll_no_df['Roll_number'] == roll_no]
    subjects = ['English', 'Hindi', 'Maths', 'Science', 'History', 'Geography']
    marks = [x.English.values[0], x.Hindi.values[0], x.Maths.values[0], x.Science.values[0], x.History.values[0],
             x.Geography.values[0]]
    fig2 = go.Figure(data=[go.Pie(labels=subjects, values=marks, pull=[0.1, 0.1, 0.1, 0.1, 0.1])])
    graph2 = plotly.offline.plot(fig2, auto_open=False, output_type="div")

    fig3 = go.Figure(data=go.Scatterpolar(
        r=[x['How interactive in class'].values[0], x['Assignments on time'].values[0],
           x['Attentive in class'].values[0], x['Participation in extra curricular'].values[0]],
        theta=['How interactive in class', 'Assignments on time', 'Attentive in class',
               'Participation in extra curricular'],
        fill='toself'
    ))

    fig3.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True
            ),
        ),
        showlegend=False
    )
    graph3 = plotly.offline.plot(fig3, auto_open=False, output_type="div")

    fig4 = go.Figure(data=go.Scatterpolar(
        r=[x['Creativity'].values[0], x['Confidence'].values[0], x['Social relationships'].values[0],
           x['Obedient'].values[0]],
        theta=['Creativity', 'confidence', 'Social relationships', 'Obedient'],
        fill='toself'
    ))

    fig4.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True
            ),
        ),
        showlegend=False
    )
    graph4 = plotly.offline.plot(fig4, auto_open=False, output_type="div")
    context = {"graph": [graph1, graph2, graph3, graph4],
               'name': request.user.name,
               }
    return render(request,"Analytics/student_dashboard.html",context)


