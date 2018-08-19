from django.http import HttpResponse
from django.shortcuts import render
from .models import Request, RequestLog, Volunteer, Victim, Service
import json
from django.contrib.auth.models import User, Group
from django import forms
from os import system
from django.views.decorators.csrf import csrf_exempt
import json
from django.forms.models import model_to_dict


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
        services = Service.objects.filter(level=1)
        return render(request, 'mainapp/volunteer_form.html',
                {'services':services})

    volunteer_phone = request.POST.get('mobile')
    password = request.POST.get('password')
    location = request.POST.get('location')
    type = request.POST.get('type')
    name = request.POST.get('name')
    district = request.POST.get('district')
    panchayath = request.POST.get('panchayath')
    is_smartphone = request.POST.get('is_smartphone', False)
    services = request.POST.getlist('services')
    availability = request.POST.get('availability')
    area_willing_to_support = request.POST.get('area_willing_to_support')

    if volunteer_phone:
        if User.objects.filter(username=volunteer_phone).count():
            return HttpResponse('already exists')
        user = User.objects.create_user(volunteer_phone, '', password)
        user.first_name = name
        user.is_staff = True
        user.is_active = False
        user.save()
        volunteer = Volunteer.objects.create(user=user, location=location, type=type)
        volunteer.panchayath = panchayath
        volunteer.district = district
        volunteer.is_smartphone = is_smartphone
        volunteer.availability = availability
        volunteer.area_willing_to_support = area_willing_to_support
        for service_id in services:
            service = Service.objects.get(pk=service_id)
            volunteer.services.add(service)
        volunteer.save()
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
            dict = model_to_dict(volunteer)
            print('curl -vL "https://script.google.com/macros/s/AKfycbyirHH2K1rxt2Mhwe5xV9IJvenWVRfny7l64A7P/exec?From={}&Who=ground&Status={}&Comments={}"'.format(
                volunteer_phone,volunteer.type +','+ str(user.first_name), dict))
            #system('curl -vL "https://script.google.com/macros/s/AKfycbyirHH2K1rxt2Mhwe5xV9IJvenWVRfny7l64A7P/exec?From={}&Who=ground&Status={}&Comments={}"'.format(
                #volunteer_phone,volunteer.type +','+ str(user.first_name), dict))
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

@csrf_exempt
def update_victim(request):
    if request.method=='POST':
        json_data=json.loads(request.body.decode('utf-8'))
        victim, created = Victim.objects.get_or_create(row=json_data['rowNum'], timestamp=json_data['row'][0])

        victim.name = json_data['row'][1]
        victim.contact = json_data['row'][2]
        victim.coordinates = json_data['row'][3]
        victim.location = json_data['row'][4]
        victim.status = json_data['row'][5]
        victim.no_of_people = json_data['row'][6]
        victim.degree_of_emergency = json_data['row'][7]
        victim.district = json_data['row'][8]
        victim.help_required_now = json_data['row'][9]
        victim.done = json_data['row'][11]
        victim.save()

        if created:
            return HttpResponse('inserted')
        return HttpResponse('updated')
    return HttpResponse('')
