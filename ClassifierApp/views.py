from django.shortcuts import render
from django.http import JsonResponse
# from .utils import ImageCollector as IC

# Create your views here.
def index(request):
    # IC.process()
    # IC.delete_dataset('batman')
    return render(request, 'ClassifierApp/index.html', {'data': 1})
def collect_image(request):
    responseData = {
        'text': 'hieu dep trai'
    }
    return JsonResponse(responseData)