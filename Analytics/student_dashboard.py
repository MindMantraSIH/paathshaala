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
    curr = df_s[df_s['Roll_number'] == s].Percent.values[0]
    res = [std_mean, curr]
    lab = ['Class Average', 'Student"s Percent']
    fig = go.Figure([go.Bar(x=lab, y=res)])
    graph1 = plotly.offline.plot(fig, auto_open=False, output_type="div")
    context = {"graph": [graph1],
               'name': request.user.name,
               }
    return render(request,"Analytics/student_dashboard.html", context)
