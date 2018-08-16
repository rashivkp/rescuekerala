from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic.edit import CreateView
from django.views.generic.base import TemplateView
from .models import Request, RequestLog
import django_filters
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
import json

def proces_log(request):
    requestee_phone = request.GET.get('From')

    if requestee_phone:
        obj, created = Request.objects.get_or_create(requestee_phone=requestee_phone,
                status='new')
        RequestLog.objects.create(request=obj, details=json.dumps(request.GET))

    return HttpResponse('')

def view_request(request, pk):
    try:
        req = Request.objects.get(pk=pk)
    except:
        return HttpResponse('')

    return render(request, 'request_view.html', {'req':req})


