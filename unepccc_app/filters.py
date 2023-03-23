import django_filters
from django import forms
from django.db.models import Count
from .models import Project, Region, Country, Status, Type, Sub_type, Validator


class ProjectFilter(django_filters.FilterSet):

    name = django_filters.CharFilter(
        lookup_expr='icontains',
        label='',
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Project name or keyword',
                'class': 'form-group'
            }
        ))
    project_id = django_filters.CharFilter(
        lookup_expr='icontains',
        label='',
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Project ID',
                'class': 'form-group'
            }
        ))

    STATUS = []

    try:
        status_options = Status.objects.all()
        for status in status_options:
            if status.project_count > 0:
                STATUS.append((status.id, status))
    except:
        pass

    status = django_filters.MultipleChoiceFilter(
        choices=STATUS, widget=forms.CheckboxSelectMultiple(
            attrs={
                'class': 'status-wrapper form-group'
            }
        ), label='Status')

    REGION = []

    try:
        region_options = Region.objects.all().order_by('name')
        for region in region_options:
            if region.project_count > 0:
                REGION.append((region.id, region))
    except:
        pass

    country__sub_region__region = django_filters.MultipleChoiceFilter(
        choices=REGION, widget=forms.CheckboxSelectMultiple(
            attrs={
                'class': 'region-wrapper form-group'
            }
        ), label='Region')

    COUNTRY = []

    try:
        country_options = Country.objects.all().order_by('name')
        for country in country_options:
            if country.project_count > 0:
                COUNTRY.append((country.id, country))
    except:
        pass

    country = django_filters.MultipleChoiceFilter(
        choices=COUNTRY, widget=forms.CheckboxSelectMultiple(
            attrs={
                'class': 'country-wrapper form-group'
            }
        ), label='Country')

    VALIDATOR = []

    try:
        validator_options = Validator.objects.all()
        for validator in validator_options:
            if validator.project_count > 0:
                VALIDATOR.append((validator.id, validator))
    except:
        pass

    validator = django_filters.MultipleChoiceFilter(
        choices=VALIDATOR, widget=forms.CheckboxSelectMultiple(
            attrs={
                'class': 'validator-wrapper form-group'
            }
        ), label='Validator')

    TYPE = []

    try:
        type_options = Type.objects.all()
        for type in type_options:
            if type.project_count > 0:
                TYPE.append((type.id, type))
    except:
        pass

    sub_type__type = django_filters.MultipleChoiceFilter(
        choices=TYPE, widget=forms.CheckboxSelectMultiple(
            attrs={
                'class': 'type-wrapper form-group'
            }
        ), label='Type')

    SUB_TYPE = []

    try:
        sub_type_options = Sub_type.objects.all()
        for sub_type in sub_type_options:
            if sub_type.project_count > 0:
                SUB_TYPE.append((sub_type.id, sub_type))
    except:
        pass

    sub_type = django_filters.MultipleChoiceFilter(
        choices=SUB_TYPE, widget=forms.CheckboxSelectMultiple(
            attrs={
                'class': 'sub-type-wrapper form-group'
            }
        ), label='Sub-type')

    class Meta:
        model = Project
        fields = ['name', 'project_id', 'status',
                  'country__sub_region__region', 'country', 'validator', 'sub_type__type', 'sub_type']
