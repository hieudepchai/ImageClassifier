from django.shortcuts import render
from django.http import JsonResponse
from .utils import ImageCollector as IC
import os
import shutil

# Create your views here.
def index(request):
    if not request.session.session_key:
        request.session.save()
    print('session keys and values: ')
    for key, value in request.session.items():
        print('{} => {}'.format(key, value))
    if 'session_id' not in request.session:
        request.session['session_id'] = request.session.session_key
    if 'work_status' not in request.session:
        request.session['work_status'] = 'free'
    if 'client_ip' not in request.session:
        request.session['client_ip'] = get_client_ip(request)
    print('session keys and values: ')
    for key, value in request.session.items():
        print('{} => {}'.format(key, value))
    # IC.delete_dataset('batman')
    request.session.modified = True
    return render(request, 'ClassifierApp/index.html',{
        'work_status': request.session['work_status']
    })

def collect_image(request):
    responseData = {
        'name': 'collect_image',
        'status': 'successful',
        'error': 'none'
    }
    try:   
        if request.method == 'POST':
            if request.session['work_status'] =='free':
                # request.session['work_status'] = 'busy'
                print(request.session['work_status'])
                request.session.save()
                print('Request: ', request)
                dataset_name = request.POST['dataset_name']
                print('Request dataset_name: ', dataset_name)
                num_classes = request.POST['num_classes']
                print('Request num_classes: ', num_classes)
                img_classes = request.POST.getlist('img_classes')
                print('Request img_classes: ', img_classes)
                #collect and download image
                IC.process(dataset_name, num_classes, img_classes)
                #dislay images
                request.session['work_status'] = 'free'
            else:
                responseData['status'] = 'pending'
        else:
            responseData['status'] = 'failed'
    except Exception as e:
        responseData['status'] = 'failed'
        responseData['error'] = e
    return JsonResponse(responseData)

def display_image(request):
    responseData = {
        'name': 'display_image',
        'status': 'successful',
        'error': 'none'
    }
    try:
        if request.method =='POST' or request.method=='GET':
            dataset = os.listdir('dataset')
            dataset_dict = dict.fromkeys(dataset)
            for ds in dataset:
                dataset_childs = dict.fromkeys(os.listdir('dataset/'+ds))
                for key in dataset_childs.keys():
                    dataset_childs[key] = os.listdir('dataset/'+ds+'/'+key+'/')
                dataset_dict[ds] = dataset_childs
            print(dataset_dict)
        else:
            responseData['status'] = 'failed'
    except Exception as e:
        responseData['status'] = 'failed'
        responseData['error'] = e
    return JsonResponse(responseData)

def clear_session(request):
    for key in list(request.session.keys()):
        del request.session[key]
    return JsonResponse({'result': 'clear session!!!'})



# ----------- functions -----------
def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def delete_dataset(dataset_name):
    try:
        print('Deleting dataset {}'.format(dataset_name))
        shutil.rmtree('dataset/'+dataset_name)
    except OSError as e:
        print ("Fail to deleting dataset %s: %s - %s." % (dataset_name, e.filename, e.strerror))