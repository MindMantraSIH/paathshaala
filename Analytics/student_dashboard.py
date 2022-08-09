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

