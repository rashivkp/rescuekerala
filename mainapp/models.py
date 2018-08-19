from django.db import models
from django.contrib.auth.models import User, AbstractUser

districts = (
    ('tvm','Thiruvananthapuram'),
    ('ptm','Pathanamthitta'),
    ('alp','Alappuzha'),
    ('ktm','Kottayam'),
    ('idk','Idukki'),
    ('mpm','Malappuram'),
    ('koz','Kozhikode'),
    ('wnd','Wayanad'),
    ('knr','Kannur'),
    ('ksr','Kasaragod'),
    ('pkd','Palakkad'),
    ('tcr','Thrissur'),
    ('ekm','Ernakulam'),
    ('kol','Kollam'),
)

volunteer_types = (
    ('ground','Ground Work'),
    ('it','IT'),
    ('manager','Manager'),
    ('hotline','Hotline'),
)
status_types =(
    ('new', 'New'),
    ('pro', 'In progess'),
    ('ais', 'Assigned in Spreadsheet'),
    ('cmp', 'Completed'),
)

contrib_status_types =(
    ('new', 'New'),
    ('ful', 'Fullfilled'),
)

vol_categories = (
    ('dcr', 'Doctor'),
    ('hsv', 'Health Services'),
    ('elw', 'Electrical Works'),
    ('mew', 'Mechanical Work'),
    ('cvw', 'Civil Work'),
    ('plw', 'Plumbing work'),
    ('vls', 'Vehicle Support'),
    ('ckg', 'Cooking'),
    ('rlo', 'Relief operation'),
    ('cln', 'Cleaning'),
    ('oth', 'Other')
)

class Service(models.Model):
    name = models.CharField(max_length=200)
    level = models.IntegerField(blank=True, null=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        if self.parent:
            return str(self.parent) + '-' + str(self.name)
        return str(self.name)

    def children(self):
        return Service.objects.filter(parent=self)


class Volunteer(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    district = models.CharField(
        blank=True, null=True,
        max_length = 15,
        choices = districts,
        verbose_name='Districts - ജില്ല'
    )
    location = models.CharField(blank=True, null=True, max_length=500,verbose_name='Location')
    panchayath = models.CharField(blank=True, null=True, max_length=500,verbose_name='Panchayath')
    type = models.CharField(
        blank=True, null=True,
        max_length = 15,
        choices = volunteer_types
    )
    area_willing_to_support = models.CharField(blank=True, null=True, max_length = 500)
    is_smartphone = models.BooleanField(blank=True, default=False)
    availability = models.CharField(blank=True, null=True, max_length = 100)
    services = models.ManyToManyField(Service)

class Request(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    district = models.CharField(
        blank=True, null=True,
        max_length = 15,
        choices = districts,
        verbose_name='Districts - ജില്ല'
    )
    location = models.CharField(blank=True, null=True, max_length=500,verbose_name='Location - സ്ഥലം')
    requestee = models.CharField(blank=True, null=True, max_length=100,verbose_name='Requestee - അപേക്ഷകന്‍റെ പേര്')
    requestee_phone = models.CharField(max_length=15,verbose_name='Requestee Phone - അപേക്ഷകന്‍റെ ഫോണ്‍ നമ്പര്‍')

    needwater = models.BooleanField(default=False, verbose_name='Water - വെള്ളം')
    detailwater = models.CharField(max_length=250, verbose_name='Details for required water - ആവശ്യമായ വെള്ളത്തിന്‍റെ വിവരങ്ങള്‍', blank=True, null=True)
    needfood = models.BooleanField(default=False, verbose_name='Food - ഭക്ഷണം')
    detailfood = models.CharField(max_length=250, verbose_name='Details for required food - ആവശ്യമായ ഭക്ഷണത്തിന്‍റെ വിവരങ്ങള്‍', blank=True, null=True)
    needcloth = models.BooleanField(default=False, verbose_name='Clothing - വസ്ത്രം')
    detailcloth = models.CharField(max_length=250, verbose_name='Details for required clothing - ആവശ്യമായ വസ്ത്രത്തിന്‍റെ വിവരങ്ങള്‍', blank=True, null=True)
    needmed = models.BooleanField(default=False, verbose_name='Medicine - മരുന്നുകള്‍')
    detailmed = models.CharField(max_length=250, verbose_name='Details for required medicine - ആവശ്യമായ മരുന്നിന്‍റെ  വിവരങ്ങള്‍', blank=True, null=True)
    needtoilet = models.BooleanField(default=False, verbose_name='Toiletries - ശുചീകരണ സാമഗ്രികള്‍ ')
    detailtoilet = models.CharField(max_length=250, verbose_name='Details for required toiletries - ആവശ്യമായ  ശുചീകരണ സാമഗ്രികള്‍', blank=True, null=True)
    needkit_util = models.BooleanField(default=False, verbose_name='Kitchen utensil - അടുക്കള സാമഗ്രികള്‍')
    detailkit_util = models.CharField(max_length=250, verbose_name='Details for required kitchen utensil - ആവശ്യമായ അടുക്കള സാമഗ്രികള്‍', blank=True, null=True)

    needothers = models.CharField(max_length=500, verbose_name="Other needs - മറ്റു ആവശ്യങ്ങള്‍", blank=True, null=True)
    status = models.CharField(
        max_length = 10,
        choices = status_types,
        default = 'new'
    )
    supply_details = models.CharField(max_length=100, blank=True, null=True)
    dateadded = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    resuced = models.BooleanField(default=False)

    def summarise(self):
        return 1
        out = ""
        if(self.needwater):
            out += "Water Requirements :\n {}".format(self.detailwater)
        if(self.needfood):
            out += "\nFood Requirements :\n {}".format(self.detailfood)
        if(self.needcloth):
            out += "\nCloth Requirements :\n {}".format(self.detailcloth)
        if(self.needmed):
            out += "\nMedicine Requirements :\n {}".format(self.detailmed)
        if(self.needtoilet):
            out += "\nToilet Requirements :\n {}".format(self.detailtoilet)
        if(self.needkit_util):
            out += "\nKit Requirements :\n {}".format(self.detailkit_util)
        if(len(self.needothers.strip()) != 0):
            out += "\nOther Needs :\n {}".format(self.needothers)
        return out

    def __str__(self):
        return str(self.get_district_display()) + ' ' + str(self.location)

    def save(self, **kwargs):
        if self.user and self.status == 'new':
            self.status = 'pro'
        elif self.user and self.status == 'pro':
            self.status = 'cmp'

        return super(Request, self).save(**kwargs)


class NewRequest(Request):
    class Meta:
        proxy = True

    def save(self, **kwargs):
        if self.user and self.status == 'new':
            self.status = 'pro'
        elif self.user and self.status == 'pro':
            self.status = 'cmp'

        return super(Request, self).save(**kwargs)


class CompletedRequest(Request):
    class Meta:
        proxy = True

class GroundWorker(Volunteer):
    class Meta:
        proxy = True

class RequestLog(models.Model):
    request = models.ForeignKey(Request, on_delete=models.CASCADE)
    details = models.TextField(blank=True, null=True)

class Victim(models.Model):
    row = models.IntegerField(blank=True, null=True)
    timestamp = models.CharField(max_length=30, blank=True, null=True)
    name = models.CharField(blank=True, null=True, max_length=200,verbose_name='Name')
    contact = models.CharField(max_length=500, blank=True, null=True)
    coordinates = models.TextField(blank=True, null=True)
    status = models.TextField(blank=True, null=True)
    location = models.TextField(blank=True, null=True)
    no_of_people =  models.CharField(max_length=100, blank=True, null=True)
    degree_of_emergency = models.TextField(blank=True, null=True)
    district = models.CharField(max_length=100, blank=True, null=True)
    help_required_immediatly = models.TextField(blank=True, null=True)
    done = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    updated_at = models.DateTimeField(blank=True, null=True, auto_now=True)

    def __str__(self):
        return str(self.name) + '-' + str(self.contact)

