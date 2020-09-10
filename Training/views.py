from django.shortcuts import render,redirect
from django.core import serializers

def dashboard(request):
    return render(request, 'Training/analysis.html', {})

def Home_Page(request):
    context = {}
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
        print(context)
        return render(request, 'Training/display_data.html', {'context': context})
    return render(request,'Training/mainpage.html',{'context':context})


def Test(request):
    return render(request,'Training/about.html')