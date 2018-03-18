from django.shortcuts import render
import pandas as pd
# Create your views here.

data = pd.read_csv('/home/pujan/Desktop/github/nse-ml-hack/hack/GOOGL.csv')


def index(request):
    context = {}
    if request.POST:
        stock = request.POST.get('stock')
        tweets = request.POST.get('tweets')
        print(stock + " " + tweets)
        two(int(tweets))
        context = {
            'open': list(data['Open'][:8]),
            'close': list(data['Close'][:8]),
            'company': stock.upper()
        }
    return render(request, 'hack/dashboard.html', context)


def two(num):
    print("HII")


def user(request):
    return render(request, 'hack/user.html')
