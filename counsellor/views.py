from django.shortcuts import render
from .models import CounselorRequest
from profiles.models import Counselor
from huggingface_hub.inference_api import InferenceApi
import numpy as np
import geopy.distance
import requests
import urllib
import json

# Create your views here.
def counsellor(request):
    if request.method == 'POST':

        query = list(Counselor.objects.all().values_list('user','description','speciality', 'latitude','longitude',
                                                         named=True))
        ids = []
        inp_sentences = []
        geoPos_list = []
        for sentence in query:
            ids.append(sentence.user)
            inp_sentences.append(sentence.description)
            geoPos_list.append((float(sentence.latitude), float(sentence.longitude)))
        print(geoPos_list)
        if request.method == "POST":
            infer_api = InferenceApi("sentence-transformers/all-MiniLM-L12-v1")
            email = request.POST.get('email')
            address = request.POST.get('address')
            pincode = request.POST.get('pincode')
            problem = request.POST.get('problem')
            where = urllib.parse.quote_plus("""
                    {
                        "postalCode": "%s"
                    }
                    """ % pincode)
            url = 'https://parseapi.back4app.com/classes/Indiapincode_Dataset_India_Pin_Code?limit=10&order=geoPosition&where=%s' % where
            headers = {
                'X-Parse-Application-Id': 'XVP5z4O2TOGHKYc7LbbUCFX5Tbctw4dYw1r5zRri',  # This is your app's application id
                'X-Parse-REST-API-Key': 'uVTRFN5134RMaQzCw1YFhWn5RohmS63ryEACBrxI'  # This is your app's REST API key
            }
            data = json.loads(
                requests.get(url, headers=headers).content.decode('utf-8'))
            latitude = data.get('results')[0].get('geoPosition').get('latitude')
            longitude = data.get('results')[0].get('geoPosition').get('longitude')
            current_geoPos = (latitude,longitude)
            counselor_patient_distance = []
            for co_ord in geoPos_list:
                counselor_patient_distance.append(geopy.distance.geodesic(current_geoPos,co_ord).km)
                #distance order will be same as id order as in the first for loop
            print(counselor_patient_distance)
            in1 = infer_api({"source_sentence": problem,"sentences": inp_sentences})
            print(in1)
            counsel_id = ids[np.argmax(in1)]
            counselor = Counselor.objects.get(user = counsel_id)
            print(f'assigned counselor: {counselor}')
            c = CounselorRequest.objects.create(email=email,address=address,problem=problem,assigned_counselor=counselor)
    return render(request, 'counsellor/counsellor.html')