from django.contrib import admin
from .models import Request, NewRequest, CompletedRequest, Volunteer, GroundWorker, Service
import csv
from django.http import HttpResponse
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from check_assignment import *


class RequestAdmin(admin.ModelAdmin):
    actions = ['download_csv', 'update_resucue_status']
    readonly_fields = ('dateadded',)
    ordering = ('district',)
    list_display = ['requestee_phone', 'status', 'resuced', 'district', 'location', 'show_request', 'dateadded']
    list_per_page = 50

    def show_request(self, obj):
        return format_html(mark_safe('<a href="/api/view/%s/">View</a>' % obj.id))

    def download_csv(self, request, queryset):
        f = open('test.csv', 'w')
        writer = csv.writer(f)
        l = []
        for i in (Request._meta.get_fields()):
            l.append(i.name)
        writer.writerow(l)
        data = Request.objects.all().values_list()
        for s in data:
            writer.writerow(s)
        f.close()
        f = open('test.csv', 'r')
        response = HttpResponse(f, content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=requests.csv'
        return response

    def update_resucue_status(self, request, queryset):
        if request.user.is_superuser:  # or Volunteer.objects.filter(user=request.user, type='hotline').exists():
            queryset.update(resuced=True)

    update_resucue_status.short_description = "Mark selected requests as resuced"


    list_filter = ('district', 'status',)

    def get_queryset(self, request):
        qs = super(RequestAdmin, self).get_queryset(request)
        return qs


class NewRequestAdmin(RequestAdmin):
    list_display = ['requestee_phone', 'status', 'dateadded']
    exclude = ('status', 'user',)

    def get_queryset(self, request):
        qs = super(NewRequestAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        if qs.filter(user=request.user, status='new').count() == 0:
            for req in qs.filter(status='new', user=None).order_by('id')[:5]:
                #if check_if_assigned(req.requestee_phone):
                    #req.status = 'ais'
                    #req.save()
                    #continue
                req.user = request.user
                req.save()

        return qs.filter(status='pro', user=request.user).order_by('id')


class CompletedRequestAdmin(RequestAdmin):
    exclude = ('status', 'user',)

    def get_queryset(self, request):
        qs = super(CompletedRequestAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs.filter(status='cmp')
        return qs.filter(status='cmp', user=request.user)

class GroundWorkerAdmin(admin.ModelAdmin):
    exclude = ('user',)
    list_display = ['location', 'type', 'name']
    list_per_page = 50

    def name(self, obj):
        if obj.user:
            return str(obj.user.first_name)+'-'+str(obj.user.username)
        return ''

    def get_queryset(self, request):
        qs = super(GroundWorkerAdmin, self).get_queryset(request)
        return qs.filter(type='ground')

class VolunteerAdmin(admin.ModelAdmin):
    exclude = ('user',)
    list_display = ['phone', 'name', 'type', 'district', 'panchayath', 'location']
    list_filter = ('district', 'type')
    list_per_page = 50
    actions = ['download_csv']

    def name(self, obj):
        if obj.user:
            return obj.user.first_name
        return ''

    def phone(self, obj):
        if obj.user:
            return obj.user.username
        return obj.location

    def download_csv(self, request, queryset):
        f = open('vtest.csv', 'w')
        writer = csv.writer(f)
        l = ['name', 'phone', 'district', 'panchayath', 'location', 'type']
        writer.writerow(l)
        for volunteer in Volunteer.objects.all().exclude(district=None):
            row = [volunteer.user.first_name, volunteer.user.username, volunteer.get_district_display(),
                    volunteer.panchayath, volunteer.location, volunteer.type]
            row = [x.encode('utf-8') for x in row]
            writer.writerow(row)

        f.close()
        f = open('vtest.csv', 'r')
        response = HttpResponse(f, content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=volunteers-other.csv'
        return response

    def get_queryset(self, request):
        qs = super(__class__, self).get_queryset(request)
        return qs.exclude(district=None)

class ServiceAdmin(admin.ModelAdmin):
    ordering = ('level',)
    list_display = ['name', 'level', 'parent']


admin.site.register(Service, ServiceAdmin)
admin.site.register(Volunteer, VolunteerAdmin)
admin.site.register(GroundWorker, GroundWorkerAdmin)
admin.site.register(Request, RequestAdmin)
admin.site.register(NewRequest, NewRequestAdmin)
admin.site.register(CompletedRequest, CompletedRequestAdmin)
