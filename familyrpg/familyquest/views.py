from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from .forms import UploadImageForm
from django.http import Http404
from django.core.exceptions import PermissionDenied
import os
import json
from django.contrib import auth
from django.contrib.auth.models import User
from tastypie.models import ApiKey


def handle_uploaded_file(temp_file, folder_path, file_name):
    """ Generic uploaded file handler """
    if isinstance(folder_path, tuple):
        folder_path = folder_path[0]
    with open(os.path.join(folder_path, file_name), 'wb+') as destination:
        for chunk in temp_file.chunks():
            destination.write(chunk)

# Create your views here.
@csrf_exempt
def photo_upload(request):
    if request.method == 'POST':
        form = UploadImageForm(request.POST, request.FILES)
        if form.is_valid():
            original_filename = str(request.FILES['image'])
            folder = os.path.join(settings.PROJECT_PATH, "familyrpg", "static"),
            handle_uploaded_file(request.FILES['image'],
                folder, original_filename)
    else:
        form = UploadImageForm()
    return render(request, 'familyquest/import.html', {'form': form})


@csrf_exempt
def request_api_key(request):
    if request.method != 'POST':
        raise PermissionDenied

    try:
        json_data = json.loads(request.body)
    except:
        return HttpResponse(json.dumps({'error': 'Invalid JSON'}),
            mimetype='application/json')

    if not 'username' in json_data:
        return HttpResponse(json.dumps({'error': 'Please provide a username'}),
            mimetype='application/json')

    if not 'password' in json_data:
        return HttpResponse(json.dumps({'error': 'Please provide a password'}),
            mimetype='application/json')

    user = auth.authenticate(username=json_data['username'],
                             password=json_data['password'])

    print 'USERNAME', json_data['username']
    print 'PASSWORD', json_data['password']
    print 'USER: ', user

    if not user:
        return HttpResponse(json.dumps({'error': 'Invalid credentials provided'}),
            mimetype='application/json')

    try:
        user.api_key
    except:
        api_key = ApiKey(user=user)
        api_key.save()

    return HttpResponse(json.dumps({'api_key': user.api_key.key, 'id': user.pk}),
            mimetype='application/json')







