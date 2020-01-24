from django.shortcuts import render
from .utils import ImageModel

# Create your views here.
def index(request):
    return render(request, 'ClassifierApp/index.html', {'data': 1})