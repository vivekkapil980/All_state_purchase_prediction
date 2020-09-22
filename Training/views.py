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
import concurrent.futures
import pandas as pd
import numpy as np

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
#contains dataframe
class TrainingData:
    def __init__(self):
        self.train_data_path = path.join(path.dirname(__file__) , "train.csv")
        self.columns = ['shopping_pt', 'state', 'group_size', 'homeowner', 'car_age', 'car_value', 'age_oldest',
                'age_youngest', 'married_couple', 'C_previous', 'duration_previous', 'A', 'B', 'C', 'D', 'E', 'F', 'G']
        self.df = pd.read_csv(self.train_data_path)
        self.last_row = self.df.tail(1)
        self.count = len(self.df)
        print(self.count)
        self.df = self.df[self.df['record_type'] == 1]
        self.data = dict()
        self.extract_data()
    def extract_data(self):
        for col in self.columns:
            self.data[col] = dict()
            for i in ['A', 'B', 'C', 'D', 'E', 'F', 'G']:
                if col == i:
                    continue
                try:
                    details = self.df.groupby([col, i]).size().reset_index().to_numpy().astype(int).tolist()
                except:
                    details = self.df.groupby([col, i]).size().reset_index().to_numpy().tolist()
                self.data[col][i] = defaultdict(dict)
                #print(details)
                for a, b, count in details:
                    self.data[col][i][a][b] = count
    # To update the csv dataframe
    def update_data(self, new_df):
        self.count += len(new_df)
        new_df  = new_df[new_df['record_type'] == 1]
        self.last_row = new_df.tail(1)
        self.df = self.df.append(new_df, ignore_index = True)
        print(new_df,self.df.tail(), self.count)
        for col in self.columns:
            for i in ['A', 'B', 'C', 'D', 'E', 'F', 'G']:
                if col == i:
                    continue
                try:
                    details = new_df.groupby([col, i]).size().reset_index().to_numpy().astype(int).tolist()
                except:
                    details = new_df.groupby([col, i]).size().reset_index().to_numpy().tolist()
                    #print(size, i, col)
                for a, b, count in details:
                    #print(a, b, count, self.data[col][i][a][b])
                    self.data[col][i][a][b] += count
    def check_for_update(self):
        new_df = pd.read_csv(self.train_data_path, skiprows=range(1,self.count))
        #print(new_df.tail())
        if not int(new_df.tail(1)['customer_ID']) == int(self.last_row['customer_ID']):
            #print('RUN', new_df.tail(1), train.last_row)
            self.update_data(new_df.iloc[1:])

def pie_chart(request):
    ''' format of data : first_index = columns(refer TrainingData class above to know about all columns available)
    # second_index:  result columns [A,B,C,D,E,F,G]
    # third_index: value of first_column eg: shopping_pt has [3, 13] values
    # fourth_index: value of second_column i.e values of A, B.....G
    # How to process this data?: first select first and second column value from drop down
    # and then directly use it inside dictionary to extract the values. then use two for loops to
    # access count values for every data point.
    '''
    train.check_for_update() #to detect any updation to training data
    context = json.dumps(train.data)
    #print(context)
    return render(request, 'Training/analysis.html', {'context':context})


def Home_Page(request):
    #dictionary to store and send it over and access in html file
    context = {}
    #store the quote values given by user from table
    quotes = []
    #list with all states for states dropdown box
    states=['NE', 'WY', 'OH', 'OK', 'AR', 'OR', 'MD', 'MT', 'CT', 'UT', 'GA', 'IN', 'FL', 'TN', 'DC', 'MS', 'CO', 'RI', 'NV', 'KY', 'WA', 'NH', 'MO', 'PA', 'DE', 'ME', 'AL', 'KS', 'SD', 'WI', 'ND', 'NY', 'NM', 'ID', 'IA', 'WV']
    
    #POST request method logic
    if request.method=='POST':

        #For a POST request get all the html textbox,radio button,dropdown box values provided by user in form
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

        #history values of customer quote details
        table = request.POST.get('table')
        #json data of all the values
        table = json.loads(table)

        #populate quotes list to process it using developed model
        for i, row in enumerate(table):
            quotes.append(row)
        # predict G
        states=['NE', 'WY', 'OH', 'OK', 'AR', 'OR', 'MD', 'MT', 'CT', 'UT', 'GA', 'IN', 'FL', 'TN', 'DC', 'MS', 'CO', 'RI', 'NV', 'KY', 'WA', 'NH', 'MO', 'PA', 'DE', 'ME', 'AL', 'KS', 'SD', 'WI', 'ND', 'NY', 'NM', 'ID', 'IA', 'WV']
        with concurrent.futures.ThreadPoolExecutor() as executor:
            process = executor.submit(predict_G,context['state'], quotes[-1][-1], quotes[-2][-1])
            G = process.result()
        #predicted quote from the model
        ans = quotes[-1][:6] + [G[0]]
        #print('ans is ',ans)
        ans[len(ans)-1]=int(ans[len(ans)-1])

        #POST request return value
        return render(request, 'Training/display_data.html', {'context': context,'states':states,'ans':ans})

    #GET request return value
    return render(request,'Training/mainpage.html',{'context':context,'states':states})


def Test(request):
    #to navigate to about.html file which has details about ePrediction website
    return render(request,'Training/about.html')

train = TrainingData()
