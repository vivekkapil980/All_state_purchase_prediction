from django.shortcuts import render,redirect
import json
from pprint import pprint
from os import path
import joblib
# Create your views here.
def predict_G(state, G1, G2):
    clf_G = joblib.load(path.join(path.dirname(__file__) , "clf_G.sav"))
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

def Home_Page(request):
    context = {}
    quotes = []
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
        print(context)
        ans = predict_G(context['state'], quotes[-1][-1], quotes[-2][-1])
        print(ans)
        pprint(quotes)
        return render(request, 'Training/display_data.html', {'context': context})
    return render(request,'Training/mainpage.html',{'context':context})


def Test(request):
    return render(request,'Training/about.html')