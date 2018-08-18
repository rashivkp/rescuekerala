from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic.edit import CreateView
from django.views.generic.base import TemplateView
from .models import Request, RequestLog, Volunteer
import django_filters
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
import json
from django.contrib.auth.models import User, Group
from django import forms
from os import system

def proces_log(request):
    requestee_phone = request.GET.get('From')

    if requestee_phone:
        if Request.objects.filter(requestee_phone=requestee_phone, status='pro').count():
            return HttpResponse('duplicate')

        obj, created = Request.objects.get_or_create(requestee_phone=requestee_phone,
                status='new')
        RequestLog.objects.create(request=obj, details=json.dumps(request.GET))

    return HttpResponse('success')

def create_volunteer(request):
    if request.method == 'GET':
        return render(request, 'mainapp/volunteer_form.html')

    volunteer_phone = request.POST.get('mobile')
    password = request.POST.get('password')
    location = request.POST.get('location')
    type = request.POST.get('type')
    name = request.POST.get('name')
    district = request.POST.get('district')
    panchayath = request.POST.get('panchayath')

    if volunteer_phone:
        if User.objects.filter(username=volunteer_phone).count():
            return HttpResponse('already exists')
        user = User.objects.create_user(volunteer_phone, '', password)
        user.first_name = name
        user.is_staff = True
        user.is_active = False
        user.save()
        volunteer = Volunteer.objects.create(user=user, location=location, type=type, panchayath=panchayath, district=district)
        group, created = Group.objects.get_or_create(name='Volunteer')
        group.user_set.add(user)
        return render(request, 'volunteer_created.html', {'user':user})

    return HttpResponse('')

def approve_volunteer(request):
    volunteer_phone = request.GET.get('From')

    if volunteer_phone:
        if len(volunteer_phone) == 11:
            volunteer_phone = volunteer_phone[1:]
        user = User.objects.filter(username=volunteer_phone).first()
        if user:
            if user.is_active == True:
                return HttpResponse('Already Appproved')
            user.is_active = True
            user.save()
            volunteer = Volunteer.objects.filter(user=user).first()
            system('curl -vL "https://script.google.com/macros/s/AKfycbyirHH2K1rxt2Mhwe5xV9IJvenWVRfny7l64A7P/exec?From={}&Status={}&Comments={}&Who=ground"'.format(
                volunteer_phone,volunteer.type +','+ str(user.first_name),str(volunteer.get_district_display())+','+str(volunteer.panchayath)+','+str(volunteer.location) ))
            return HttpResponse('appproved')
        else:
            volunteer, created = Volunteer.objects.get_or_create(user=None, location=volunteer_phone, type='ground')
            if created:
                system('curl -vL "https://script.google.com/macros/s/AKfycbyirHH2K1rxt2Mhwe5xV9IJvenWVRfny7l64A7P/exec?From={}&Status=&Comments=&Who=ground"'.format(volunteer_phone))
            return HttpResponse('ground worker created')

    return HttpResponse('invalid')

def view_request(request, pk):
    try:
        req = Request.objects.get(pk=pk)
    except:
        return HttpResponse('')

    return render(request, 'request_view.html', {'req':req})


