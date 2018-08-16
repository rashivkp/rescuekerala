from django.contrib import admin
from .models import Request, NewRequest
import csv
from django.http import HttpResponse

class NewRequestAdmin(admin.ModelAdmin):
    actions = ['download_csv']
    readonly_fields = ('dateadded',)
    exclude = ('status',)
    ordering = ('district',)
    list_display = ['requestee_phone', 'status', 'district', 'location']
    def download_csv(self, request, queryset):
        f = open('test.csv', 'w')
        writer = csv.writer(f)
        l = []
        for i in (NewRequest._meta.get_fields()):
            l.append(i.name)
        writer.writerow(l)
        data = NewRequest.objects.all().values_list()
        for s in data:
            writer.writerow(s)
        f.close()
        f = open('test.csv', 'r')
        response = HttpResponse(f, content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=requests.csv'
        return response

    list_filter = ('district',)

    def get_queryset(self, request):
        qs = super(NewRequestAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        if qs.filter(user=request.user).count() == 0:
            for req in qs.filter(status='new', user=None).order_by('id')[:5]:
                req.user = request.user
                req.save()
                print(req.id)

        return qs.filter(status='pro', user=request.user)


class RequestAdmin(admin.ModelAdmin):
    actions = ['download_csv']
    readonly_fields = ('dateadded',)
    ordering = ('district',)
    list_display = ['requestee_phone', 'status', 'district', 'location']
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
        return qs.filter(status='new')


class VolunteerAdmin(admin.ModelAdmin):
    readonly_fields = ('joined',)
    list_display = ('name', 'phone', 'organisation', 'joined')
    list_filter = ('district', 'joined',)

class ContributorAdmin(admin.ModelAdmin):
    list_filter = ('district', 'status',)

#admin.site.register(Request, RequestAdmin)
admin.site.register(NewRequest, NewRequestAdmin)
