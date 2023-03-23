import uuid
from django.db import models
from django.db.models.query import QuerySet
from django.db.models import Sum


class Region(models.Model):
    name = models.CharField(max_length=50, unique=True)

    @property
    def sub_regions(self) -> QuerySet:
        return Sub_region.objects.filter(region=self.id)

    @property
    def countries(self) -> QuerySet:
        return Country.objects.filter(sub_region__region=self.id)

    @property
    def project_count(self):
        return Project.objects.filter(country__sub_region__region=self.id).count()

    def __str__(self):
        return self.name


class Sub_region(models.Model):
    name = models.CharField(max_length=50, unique=True)
    region = models.ForeignKey(Region, on_delete=models.PROTECT)

    @property
    def countries(self) -> QuerySet:
        return Country.objects.filter(sub_region=self.id)

    def __str__(self):
        return self.name


class Country(models.Model):
    name = models.CharField(max_length=50, unique=True)
    sub_region = models.ForeignKey(Sub_region, on_delete=models.PROTECT)

    @property
    def project_count(self) -> QuerySet:
        return Project.objects.filter(country=self.id).count()

    class Meta:
        verbose_name_plural = 'countries'

    def __str__(self):
        return self.name


class Sector(models.Model):
    name = models.CharField(max_length=100)

    @property
    def methodologies(self) -> QuerySet:
        return Methodology.objects.filter(sector=self.id).annotate(credits=Sum('project__credit__credit'))

    @property
    def project_count(self):
        return Project.objects.filter(methodology__sector=self.id).count()

    def __str__(self):
        return self.name


class Methodology(models.Model):
    name = models.CharField(max_length=500)
    methodology_id = models.CharField(max_length=20)
    sector = models.ForeignKey(Sector, on_delete=models.PROTECT)
    description = models.TextField()

    @property
    def projects(self) -> QuerySet:
        return Project.objects.filter(methodology=self.id).annotate(credits=Sum('credit__credit'))

    @property
    def project_count(self) -> QuerySet:
        return Project.objects.filter(methodology=self.id).count()

    class Meta:
        verbose_name_plural = 'methodologies'

    def __str__(self):
        return self.methodology_id


class Organisation(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Buyer(models.Model):
    name = models.CharField(max_length=200)
    organisation = models.ForeignKey(Organisation, on_delete=models.PROTECT)
    country = models.ForeignKey(Country, on_delete=models.PROTECT)

    @property
    def project_count(self) -> QuerySet:
        return Project.objects.filter(buyer=self.id).count()

    def __str__(self):
        return self.name


class PDD_consultant(models.Model):
    name = models.CharField(max_length=200)
    organisation = models.ForeignKey(Organisation, on_delete=models.PROTECT)
    country = models.ForeignKey(Country, on_delete=models.PROTECT)

    @property
    def project_count(self) -> QuerySet:
        return Project.objects.filter(pdd_consultant=self.id).count()

    def __str__(self):
        return self.name


class Status(models.Model):
    name = models.CharField(max_length=80)

    @property
    def project_count(self) -> QuerySet:
        return Project.objects.filter(status=self.id).count()

    class Meta:
        verbose_name_plural = 'status'

    def __str__(self):
        return self.name


class Type(models.Model):
    name = models.CharField(max_length=100)

    @property
    def project_count(self) -> QuerySet:
        return Project.objects.filter(sub_type__type=self.id).count()

    def __str__(self):
        return self.name


class Sub_type(models.Model):
    name = models.CharField(max_length=100)
    type = models.ForeignKey(Type, on_delete=models.PROTECT)

    @property
    def project_count(self) -> QuerySet:
        return Project.objects.filter(sub_type=self.id).count()

    def __str__(self):
        return self.name


class Validator(models.Model):
    name = models.CharField(max_length=200)
    short_name = models.CharField(max_length=50)
    country = models.ForeignKey(Country, on_delete=models.PROTECT)

    @property
    def project_count(self) -> QuerySet:
        return Project.objects.filter(validator=self.id).count()

    def __str__(self):
        return self.short_name


class Project(models.Model):
    name = models.CharField(max_length=500)
    project_id = models.CharField(max_length=50)
    project_ref = models.CharField(max_length=20)
    idVal = models.UUIDField(default=uuid.uuid4, primary_key=False)
    methodology = models.ForeignKey(Methodology, on_delete=models.PROTECT)
    country = models.ForeignKey(Country, on_delete=models.PROTECT)
    status = models.ForeignKey(Status, on_delete=models.PROTECT)
    sub_type = models.ForeignKey(Sub_type, on_delete=models.PROTECT)
    buyer = models.ForeignKey(Buyer, on_delete=models.PROTECT)
    pdd_consultant = models.ForeignKey(
        PDD_consultant, on_delete=models.PROTECT)
    validator = models.ForeignKey(Validator, on_delete=models.PROTECT)
    expected_CERs = models.IntegerField(default=0)
    credit_start = models.DateField(auto_now_add=False, blank=True, null=True)

    def __str__(self):
        return self.project_id


class Credit(models.Model):
    credit = models.IntegerField()
    date = models.DateField(auto_now_add=False, blank=True)
    project = models.ForeignKey(Project, on_delete=models.PROTECT)

    def __int__(self):
        return self.credit
