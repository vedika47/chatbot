from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import logout, authenticate
from django.contrib.auth import login as log
# from django.views.decorators.csrf import csrf_protect
# from django.views.decorators.cache import cache_page

import openai
from .config import apikey
# password for test user is Harry$$$***000
# Create your views here.
healthCareKeyword = ["Health",'deases',"Wellness","Medical","Healthcare","Doctor","Physician","Hospital","Clinic","Patient","Treatment","Diagnosis","Medicine","Prescription","Surgery","Nurse","Caregiver","Health insurance","Pharmacy","Medical equipment","Rehabilitation","Therapy","Vaccination","Preventive care","Health check-up","Telemedicine","Telehealth","Health technology","Medical research","Disease","Chronic condition","Mental health","Nutrition","Fitness","Exercise","Lifestyle","Maternity care","Pediatric care","Elderly care","Home healthcare","Palliative care","Emergency medicine","Radiology","Laboratory","Health screening","Health education","Public health","Health promotion","Hygiene","Wellness program","Rehabilitation therapy","Occupational therapy","Physical therapy","Respiratory therapy","Cardiology","Oncology","Gynecology","Dermatology","Neurology","Pediatrics","Geriatrics","Obstetrics","Allergy","Immunization","Diabetes","Arthritis","Asthma","Heart disease","Cancer","Mental illness","Alzheimer's","Stroke","Infection","Wound care","Rehabilitation center","Assisted living","Hospice care","Health assessment","Health monitoring","Health records","Health informatics","Medical imaging","Medical technology","Healthcare policy","Healthcare reform","Healthcare system","Healthcare provider","Healthcare professional","Electronic health records","Personalized medicine","Gene therapy","Regenerative medicine","Biotechnology","Medical device","Health and safety","Health promotion","Health campaign","Health insurance coverage","Health benefits","Healthcare costs","Healthcare disparities","Rehabilitation services","Physical rehabilitation","Mental health counseling","Behavioral health","Home health services","Palliative care services","Hospice care services","Health screening programs","Preventive health measures","Health and wellness coaching","Health education programs","Community health programs","Health risk assessment","Health behavior change","Chronic disease management","Health tracking apps","Telehealth services","Remote patient monitoring","Healthcare technology advancements","Medical breakthroughs","Surgical procedures","Minimally invasive surgery","Emergency medical services","Critical care","Intensive care unit","Patient care protocols","Medical consultation","Second opinion services","Maternal healthcare","Neonatal care","Fertility treatments","Genetic counseling","Precision medicine","Integrative medicine","Holistic healthcare","Complementary therapies","Alternative medicine","Traditional Chinese medicine","Ayurvedic medicine","Nutraceuticals","Dietary supplements","Herbal remedies","Medical research studies","Clinical trials","Medical ethics","Healthcare regulations""Health law","Healthcare accreditation",
]
def login(request):
    # print(request.user)
    # if request.user.is_anonymous:
    # return redirect("/login")
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(username, password)

        # check if user has entered correct credentials
        user = authenticate(username=username, password=password)

        if user is not None:
            # A backend authenticated the credentials
            log(request, user)
            return redirect("home")
            # return render(request, 'index.html')

        else:
            # No backend authenticated the credentials
            return redirect("login.html")
        
    return render(request,"login.html")

def index(request):
    print(request.user)
    if request.user.is_anonymous:
        return redirect("login")
    else:
        return render(request,"index.html")
#    return render(request,'login.html')


def signup(request):
    if request.method == 'POST':
        fname = request.POST.get('first_name')
        lname = request.POST.get('last_name')
        Mobile = request.POST.get('mobile')
        Username = request.POST.get('username')
        Password = request.POST.get('password')
        user = User.objects.create_user(username=Username, password=Password)
        user.first_name = fname
        user.last_name = lname
        user.save()

        return redirect("/")
    else:
        return render(request, "signup.html")
    

def logoutUser(request):
    logout(request)
    return redirect("login")


def Healthpage(request):
    context={}
    flag=0
    if request.method == "POST":
        prompt = request.POST.get("prompt")
        words=prompt.split(" ")
        print(words)
        openai.api_key = apikey
        response=None
        for i in healthCareKeyword:
            for j in words:
                i.lower()
                j.lower()
                if i==j:
                    response = openai.Completion.create(
                    model="text-davinci-003",
                    prompt=prompt,
                    temperature=0.7,
                    max_tokens=200,
                    top_p=1,
                    frequency_penalty=0,
                    presence_penalty=0
                    )
                    context['response']=response['choices'][0]['text']
                    context['prompt']=prompt
                    flag=1
        # return render(request, 'Healthcare.html',context)
                    
        else:
            if flag==1:
                message=prompt
            else:
                message="Ask health related questions"
            context['meg']=message
            return render(request, 'Healthcare.html',context)


def ImgGenerator(request):
    if request.method == "POST":
        prompt = request.POST.get("prompt")
        openai.api_key = apikey
        imgRespose = openai.Image.create(
            prompt=prompt,
            n=1,
            size="512x512"
        )
        context={
            "question":prompt,
            "img_url":imgRespose['data'][0]['url']
        }
        return render(request, 'ImageGenerate.html',context)
    else:
        return render(request, 'ImageGenerate.html')
