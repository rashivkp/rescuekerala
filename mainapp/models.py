from django.db import models
from django.contrib.auth.models import User

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

status_types =(
    ('new', 'New'),
    ('pro', 'In progess'),
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


class RequestLog(models.Model):
    request = models.ForeignKey(Request, on_delete=models.CASCADE)
    details = models.TextField(blank=True, null=True)
