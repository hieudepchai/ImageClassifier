from django.shortcuts import render
# from .utils import ImageCollector
from selenium import webdriver
# Create your views here.
def index(request):
    chromepath ='chromedriver.exe'
    driver = webdriver.Chrome(chromepath)
    driver.get('https://images.google.com/')
    return render(request, 'ClassifierApp/index.html', {'data': 1})