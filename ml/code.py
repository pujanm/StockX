#f = open("nse_data.txt", "r")
import pandas as pd
myList = []
news = []
date = []
date_in_correct_format = []
demoList = []

with open("nse_data.txt", "r") as f:
    for line in f:
        myList.append(line)

for i in range(2, 12000, 6):
    myList[i] = myList[i].replace(",", ";")
    print(myList[i])
    news.append(myList[i])

f = open("News.txt", "w")
f3 = open("Data.csv", 'w')

for i in range(4, 12000, 6):
    date.append(myList[i])

for i in news:
    f.write(i)

f2 = open("Date.txt", "w")

months = {"Jan." : "01", "Feb." : "02", "March" : "03"}

for i in date:
    demoList = i.split()
    str = demoList[2]
    if(len(demoList[3]) is 2):
        demoList[3] = '0' + demoList[3]
#    if i[-9] == " ":
#        i[-9] = "0"
    date_in_correct_format.append(i[-5:-1] + "-" + months[str] + "-" + demoList[3][0:2])


for i in range(len(date_in_correct_format)):
    f3.write(date_in_correct_format[i] + "," + news[i])
