from django.contrib import admin
from .models import Request, NewRequest, CompletedRequest, Volunteer, GroundWorker
import csv
from django.http import HttpResponse
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from check_assignment import *


class RequestAdmin(admin.ModelAdmin):
    actions = ['download_csv']
    readonly_fields = ('dateadded',)
    ordering = ('district',)
    list_display = ['requestee_phone', 'status', 'district', 'location', 'show_request', 'dateadded']
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
    list_display = ['location', 'type']
    list_per_page = 50

    def get_queryset(self, request):
        qs = super(GroundWorkerAdmin, self).get_queryset(request)
        return qs.filter(type='ground')

class VolunteerAdmin(admin.ModelAdmin):
    exclude = ('user',)
    list_display = ['phone', 'type', 'district', 'panchayath', 'location']
    list_filter = ('district', 'type')
    list_per_page = 50

    def phone(self, obj):
        if obj.user:
            return obj.user.username
        return obj.location

admin.site.register(Volunteer, VolunteerAdmin)
admin.site.register(GroundWorker, GroundWorkerAdmin)
admin.site.register(Request, RequestAdmin)
admin.site.register(NewRequest, NewRequestAdmin)
admin.site.register(CompletedRequest, CompletedRequestAdmin)
