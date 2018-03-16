from django.shortcuts import render

# Create your views here.


def index(request):
    return render(request, 'hack/dashboard.html')


def user(request):
    return render(request, 'hack/user.html')
