from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic.edit import CreateView
from django.views.generic.base import TemplateView
from .models import Request, RequestLog
import django_filters
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
import json
from django.contrib.auth.models import User, Group
from django import forms

def proces_log(request):
    requestee_phone = request.GET.get('From')

    if requestee_phone:
        obj, created = Request.objects.filter(requestee_phone=requestee_phone, status='new')

        obj, created = Request.objects.get_or_create(requestee_phone=requestee_phone,
                status='new')
        RequestLog.objects.create(request=obj, details=json.dumps(request.GET))

    return HttpResponse('success')

def create_volunteer(request):
    if request.method == 'GET':
        return render(request, 'mainapp/volunteer_form.html')

    volunteer_phone = request.POST.get('mobile')
    password = request.POST.get('password')

    if volunteer_phone:
        if User.objects.filter(username=volunteer_phone).count():
            return HttpResponse('already exists')
        user = User.objects.create_user(volunteer_phone, '', password)
        user.is_staff = True
        user.is_active = False
        user.save()
        group, created = Group.objects.get_or_create(name='Volunteer')
        group.user_set.add(user)
        return render(request, 'volunteer_created.html', {'user':user})

    return HttpResponse('')

def approve_volunteer(request):
    volunteer_phone = request.GET.get('From')

    if volunteer_phone:
        user = User.objects.filter(username=volunteer_phone).first()
        if user:
            user.is_active = True
            return HttpResponse('appproved')
        return HttpResponse('not found')

    return HttpResponse('')

def view_request(request, pk):
    try:
        req = Request.objects.get(pk=pk)
    except:
        return HttpResponse('')

    return render(request, 'request_view.html', {'req':req})


