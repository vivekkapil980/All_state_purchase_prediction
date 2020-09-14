from django.shortcuts import render,redirect
from django.core import serializers
import json
from pprint import pprint
import csv
from django.contrib.staticfiles.storage import staticfiles_storage
from django.shortcuts import render
import time
from collections import defaultdict, Counter
import collections
from os import path
import joblib
import threading
import concurrent.futures
# Create your views here.
clf_G = joblib.load(path.join(path.dirname(__file__) , "clf_G.sav"))
def predict_G(state, G1, G2):
    # state dummies
    features = [0] * 11
    features[G1 - 1] = 1
    features[G2 + 3] = 1
    if state == 'FL':
        features[8] = 1
    elif state == 'ND':
        features[9] = 1
    elif state == 'SD':
        features[10] = 1
    print(features, state, G1, G2)
    return clf_G.predict([features])

def getPerc(d,name):
    s=0
    for i in d.keys():
        s+=d[i]
    for i in d.keys():
        d[i]=int((d[i]/s)*100)
    labels=[]
    data=[]
    ans=[]
    for i in sorted(d.keys()):
        if i not in 'ABCDEFG':
            labels.append(str(i))
            data.append(d[i])
    ans.append(labels)
    ans.append(data)
    ans.append(name)
    return ans
car_age=[]
age_oldest=[]
age_youngest=[]
duration_prev=[]
state=[]
group_size=[]
location=[]
homeowner=[]
risk_factor=[]
car_value=[]
married_couple=[]
C_previous=[]
A=B=C=D=E=F=G=[]
def pie_chart(request):
    url = path.join(path.dirname(__file__) , "train.csv")
    with open(url, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)

        for line in csv_reader:
            state.append(line[5])
            location.append(line[6])
            group_size.append(line[7])
            homeowner.append(line[8])
            car_age.append(line[9])
            car_value.append(line[10])
            risk_factor.append(line[11])
            age_oldest.append(line[12])
            age_youngest.append(line[13])
            married_couple.append(line[14])
            C_previous.append(line[15])
            duration_prev.append(line[16])
            A.append(line[17])
            B.append(line[18])
            C.append(line[19])
            D.append(line[20])
            E.append(line[21])
            F.append(line[22])
            G.append(line[23])
    time.sleep(5)
    state_f=(dict(Counter(state)))
    state_f.pop('state')
    married_couple_f=(dict(Counter(married_couple)))
    married_couple_f.pop('married_couple')
    risk_factor_f=(dict(Counter(risk_factor)))
    risk_factor_f.pop('risk_factor')
    homeowner_f=(dict(Counter(homeowner)))
    homeowner_f.pop('homeowner')
    location_f=(dict(Counter(location)))
    location_f.pop('location')
    group_size_f=(dict(Counter(group_size)))
    group_size_f.pop('group_size')
    car_age_f=(dict(Counter(car_age)))
    car_age_f.pop('car_age')
    car_value_f=(dict(Counter(car_value)))
    car_value_f.pop('car_value')
    age_oldest_f=(dict(Counter(age_oldest)))
    age_oldest_f.pop('age_oldest')
    age_youngest_f=(dict(Counter(age_youngest)))
    age_youngest_f.pop('age_youngest')
    C_previous_f=(dict(Counter(C_previous)))
    C_previous_f.pop('C_previous')
    duration_prev_f=(dict(Counter(duration_prev)))
    duration_prev_f.pop('duration_previous')
    A_f=(dict(Counter(A)))
    A_f.pop('A')
    B_f=(dict(Counter(B)))
    B_f.pop('B')
    C_f=(dict(Counter(C)))
    C_f.pop('C')
    D_f=(dict(Counter(D)))
    D_f.pop('D')
    E_f=(dict(Counter(E)))
    E_f.pop('E')
    F_f=(dict(Counter(F)))
    F_f.pop('F')
    G_f=(dict(Counter(G)))
    G_f.pop('G')


    risk=getPerc(risk_factor_f,'Risk Factor')
    married=getPerc(married_couple_f,'Married Couple(0/1)')
    st = getPerc(state_f,'State')
    owner = getPerc(homeowner_f,'Home Owner')
    loc = getPerc(location_f,'Location')
    group = getPerc(group_size_f,'Group Size')
    age = getPerc(car_age_f,'Car Age')
    carvalue = getPerc(car_value_f,'Car Value')
    old = getPerc(age_oldest_f,'Oldest Age')
    young = getPerc(age_youngest_f,'Youngest Age')
    cprev = getPerc(C_previous_f,'C previous')
    prev_duraation = getPerc(duration_prev_f,'With Previous Customer')
    a = getPerc(A_f,'A')
    b = getPerc(B_f,'B')
    c = getPerc(C_f,'C')
    d = getPerc(D_f,'D')
    e = getPerc(E_f,'E')
    f = getPerc(F_f,'F')
    g = getPerc(G_f,'G')


    array_context=[{'label':risk[0], 'data':risk[1],'title':risk[2]}, {'label':married[0],'data':married[1],'title':married[2]},{'label':st[0],'data':st[1],'title':st[2]},{'label':owner[0],'data':owner[1],'title':owner[2]},
                   {'label':loc[0],'data':loc[1],'title':loc[2]},{'label':group[0],'data':group[1],'title':group[2]},{'label':age[0],'data':age[1],'title':age[2]},{'label':carvalue[0],'data':carvalue[1],'title':carvalue[2]},
                   {'label': old[0], 'data': old[1],'title': old[2]},{'label':young[0],'data':young[1],'title':young[2]},{'label':cprev[0],'data':cprev[1],'title':cprev[2]},
                   {'label':prev_duraation[0],'data':prev_duraation[1],'title':prev_duraation[2]},{'label': a[0], 'data': a[1],'title': a[2]},{'label':b[0],'data':b[1],'title':b[2]},{'label':c[0],'data':c[1],'title':c[2]},
                   {'label':d[0],'data':d[1],'title':d[2]},{'label': e[0], 'data': e[1],'title': e[2]},{'label':f[0],'data':f[1],'title':f[2]},{'label':g[0],'data':g[1],'title':g[2]}
                   ]
    context = json.dumps(array_context)
    return render(request, 'Training/analysis.html', {'context':context})

def dashboard(request):
    pie_chart()
    return render(request, 'Training/analysis.html', {})
    
def Home_Page(request):
    context = {}
    quotes = []
    states=['NE', 'WY', 'OH', 'OK', 'AR', 'OR', 'MD', 'MT', 'CT', 'UT', 'GA', 'IN', 'FL', 'TN', 'DC', 'MS', 'CO', 'RI', 'NV', 'KY', 'WA', 'NH', 'MO', 'PA', 'DE', 'ME', 'AL', 'KS', 'SD', 'WI', 'ND', 'NY', 'NM', 'ID', 'IA', 'WV']
    if request.method=='POST':
        context['customer_id']=request.POST.get('customer_id')
        context['state']=request.POST.get('state')
        context['shop_id']=request.POST.get('shop_id')
        context['location'] = request.POST.get('location')
        context['group_size'] = request.POST.get('group_size')
        context['car_age'] = request.POST.get('car_age')
        context['car_value'] = request.POST.get('car_value')
        context['young_age'] = request.POST.get('young_age')
        context['elder_age'] = request.POST.get('elder_age')
        context['price'] = request.POST.get('price')
        context['married']=request.POST.get('married')
        context['risk'] = request.POST.get('risk')
        context['prev_duration'] = request.POST.get('prev_duration')
        table = request.POST.get('table')
        table = json.loads(table)
        for i, row in enumerate(table):
            quotes.append(row)
        # predict G
        states=['NE', 'WY', 'OH', 'OK', 'AR', 'OR', 'MD', 'MT', 'CT', 'UT', 'GA', 'IN', 'FL', 'TN', 'DC', 'MS', 'CO', 'RI', 'NV', 'KY', 'WA', 'NH', 'MO', 'PA', 'DE', 'ME', 'AL', 'KS', 'SD', 'WI', 'ND', 'NY', 'NM', 'ID', 'IA', 'WV']
        with concurrent.futures.ThreadPoolExecutor() as executor:
            process = executor.submit(predict_G,context['state'], quotes[-1][-1], quotes[-2][-1])
            G = process.result()
        ans = quotes[-1][:6] + [G[0]]
        print('ans is ',ans)
        ans[len(ans)-1]=int(ans[len(ans)-1])
        return render(request, 'Training/display_data.html', {'context': context,'states':states,'ans':ans})
    return render(request,'Training/mainpage.html',{'context':context,'states':states})


def Test(request):
    return render(request,'Training/about.html')
