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
import smtplib
from suggestions.models import Data
from django.conf import settings
from django.core.mail import send_mail
import os
import csv

def insights():
    roll_no = Student.objects.filter(user=request.user)[1]
    df_s = pd.read_csv('Analytics/data/student_data.csv')
    curr = df_s[df_s['Roll_number'] == roll_no]
    std = df_s[df_s['Roll_number'] == roll_no].Standard.values[0]
    std_df = df_s[df_s["Standard"] == std]
    std_mean = std_df['Percent'].mean()
    curr = df_s[df_s['Roll_number'] == roll_no].Percent.values[0]
    res = [std_mean, curr]
    lab = ['Class Average', 'Student"s Percent']
    fig1 = go.Figure([go.Bar(x=lab, y=res)])
    graph1 = plotly.offline.plot(fig1, auto_open=False, output_type="div")
    x = df_s[df_s['Roll_number'] == roll_no]
    subjects = ['English', 'Hindi', 'Maths', 'Science', 'History', 'Geography']
    marks = [x.English.values[0], x.Hindi.values[0], x.Maths.values[0], x.Science.values[0], x.History.values[0],
             x.Geography.values[0]]
    fig2 = go.Figure(data=[go.Pie(labels=subjects, values=marks,pull=[0.1,0.1,0.1,0.1,0.1])])
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
        r=[x['Creativity'].values[0], x['confidence'].values[0], x['Social relationships'].values[0],
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
    context = {"graph": [graph1,graph2,graph3,graph4],
               'name': request.user.name,
               }
    return render(request,"Analytics/student_dashboard.html", context)
