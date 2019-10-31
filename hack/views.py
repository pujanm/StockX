from django.shortcuts import render
import pandas as pd
import re
import sys
import time
import datetime
import requests
from threading import Thread
from time import sleep

# Create your views here.
import os
import tweepy
import requests
import numpy as np

from keras.models import Sequential
from keras.layers import Dense
from textblob import TextBlob


consumer_key = 'K8rDGMdTDwKz2tWpNIuurZSr7'
consumer_secret = 'wb1ZWvuC9loX78f6GVDVgNzoG0YATKLhPwjtXlnWrOiplm901u'
access_token = '962553243116204032-XWr3Ud2mD56izQFWFXu2aZMCZ9MkGxZ'
access_token_secret = 'fqYgYnEAkwy15NZBHhjb0ZCoL67hybGZe7fni8QXFL2RY'
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
user1 = tweepy.API(auth)

data = '/Users/sahiljajodia/nse-ml-hack/data.csv'


def stock_sentiment(quote, num_tweets):
    # Checks if the sentiment for our quote is
    # positive or negative, returns True if
    # majority of valid tweets have positive sentiment
    print("stock_sentiment")
    list_of_tweets = user1.search(quote, count=num_tweets)
    positive, null = 0, 0

    for tweet in list_of_tweets:
        blob = TextBlob(tweet.text).sentiment
        if blob.subjectivity == 0:
            null += 1
            next
        if blob.polarity > 0:
            positive += 1

    if positive > ((num_tweets - null)/2):
        return True


def stock_prediction(stock):

    # Collect data points from csv
    dataset = []

    f = open(data)

    for n, line in enumerate(f):
        if n != 0:
            dataset.append(float(line.split(',')[1]))

    dataset = np.array(dataset)

    # Create dataset matrix (X=t and Y=t+1)
    def create_dataset(dataset):
        rang = len(dataset)-2
        dataX = [dataset[n+1] for n in range(rang)]
        return np.array(dataX), dataset[2:]

    trainX, trainY = create_dataset(dataset)

    # Create and fit Multilinear Perceptron model
    model = Sequential()
    model.add(Dense(8, input_dim=1, activation='relu'))
    model.add(Dense(1))
    model.compile(loss='mean_squared_error', optimizer='adam')
    model.fit(trainX, trainY, epochs=200, batch_size=2, verbose=0)

    # Our prediction for tomorrow
    prediction_var = np.array([dataset[0]])
    prediction = model.predict(prediction_var)
    result = "%s's stock price will move from %s to %s on the next open day of the stock exchange." % (stock, dataset[0], prediction[0][0])
    return result


def split_crumb_store(v):
    return v.split(':')[2].strip('"')


def find_crumb_store(lines):
    # Looking for
    # ,"CrumbStore":{"crumb":"9q.A4D1c.b9
    for l in lines:
        if re.findall(r'CrumbStore', l):
            return l
    print("Did not find CrumbStore")


def get_cookie_value(r):
    return {'B': r.cookies['B']}


def get_page_data(symbol):
    url = "https://finance.yahoo.com/quote/%s/?p=%s" % (symbol, symbol)
    r = requests.get(url)
    cookie = get_cookie_value(r)

    # Code to replace possible \u002F value
    # ,"CrumbStore":{"crumb":"FWP\u002F5EFll3U"
    # FWP\u002F5EFll3U
    lines = r.content.decode('unicode-escape').strip(). replace('}', '\n')
    return cookie, lines.split('\n')


def get_cookie_crumb(symbol):
    cookie, lines = get_page_data(symbol)
    crumb = split_crumb_store(find_crumb_store(lines))
    return cookie, crumb


def get_data_quote(symbol, start_date, end_date, cookie, crumb):
    filename = 'data.csv'
    url = "https://query1.finance.yahoo.com/v7/finance/download/%s?period1=%s&period2=%s&interval=1d&events=history&crumb=%s" % (symbol, start_date, end_date, crumb)
    response = requests.get(url, cookies=cookie)
    with open(filename, 'wb') as handle:
        for block in response.iter_content(1024):
            handle.write(block)


def get_now_epoch():
    # @see https://www.linuxquestions.org/questions/programming-9/python-datetime-to-epoch-4175520007/#post5244109
    return int(time.time())


def download_quotes(symbol):
    start_date = 0
    end_date = get_now_epoch()
    cookie, crumb = get_cookie_crumb(symbol)
    get_data_quote(symbol, start_date, end_date, cookie, crumb)


stock = ""


def index(request):
    context = {}
    if request.POST:
        stock = request.POST.get('stock')
        tweets = request.POST.get('tweets')
        print(stock + " " + tweets)
        download_quotes(stock)
        if stock_sentiment(stock, int(tweets)):
            print('This stock has good sentiment on Twitter.')
            res = 'This stock has good sentiment on Twitter.'

        if not stock_sentiment(stock, int(tweets)):
            print('This stock has bad sentiment on Twitter.')
            res = 'This stock has bad sentiment on Twitter.'

        # res = stock_prediction(stock)

        data1 = pd.read_csv(data)
        context = {
            'open': list(data1['Open'][:366]),
            'close': list(data1['Close'][:366]),
            'company': stock.upper(),
            'result': res,
        }
    return render(request, 'hack/dashboard.html', context)
