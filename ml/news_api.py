import requests

url = ('https://newsapi.org/v2/everything?'
       'q=stock&'
       'from=2016-09-17&'
       'sortBy=popularity&'
       'apiKey=eed4aded64c8468397e812208c418488')

r = requests.get(url).json()['articles']

print(r)