from django.shortcuts import render
from .models import CounselorRequest
from profiles.models import Counselor
from huggingface_hub.inference_api import InferenceApi
import numpy as np

# Create your views here.
def counsellor(request):
    query = list(Counselor.objects.all().values_list('user','description','speciality', named=True))
    ids = []
    inp_sentences = []
    for sentence in query:
        ids.append(sentence.user)
        inp_sentences.append(sentence.description)
    if request.method == "POST":
        infer_api = InferenceApi("sentence-transformers/all-MiniLM-L12-v1")
        email = request.POST.get('email')
        address = request.POST.get('address')
        problem = request.POST.get('problem') 
        in1 = infer_api({"source_sentence": problem,"sentences": inp_sentences})   
        print(in1)
        counsel_id = ids[np.argmax(in1)]
        counselor = Counselor.objects.get(user = counsel_id)
        print(f'assigned counselor: {counselor}')
        c = CounselorRequest.objects.create(email=email,address=address,problem=problem,assigned_counselor=counselor)
    return render(request, 'counsellor/counsellor.html')