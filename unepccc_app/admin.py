from django.contrib import admin
from .models import Region, Sub_region, Country, Sector, Methodology, Buyer, PDD_consultant, Status, Type, Sub_type, Validator, Project, Credit, Organisation


class CountryAdmin(admin.ModelAdmin):
    list_display = ('name', 'sub_region')


class MethodologyAdmin(admin.ModelAdmin):
    list_display = ('methodology_id', 'name', 'sector')


class BuyerAdmin(admin.ModelAdmin):
    list_display = ('name', 'organisation', 'country')


class PDDAdmin(admin.ModelAdmin):
    list_display = ('name', 'organisation', 'country')


class SubtypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'type')


class ValidatorAdmin(admin.ModelAdmin):
    list_display = ('name', 'short_name', 'country')


class ProjectAdmin(admin.ModelAdmin):
    list_display = ('project_id', 'project_ref', 'name', 'country', 'status', 'methodology', 'credit_start', 'expected_CERs')


class CreditAdmin(admin.ModelAdmin):
    list_display = ('credit', 'project', 'date')


admin.site.register(Region)
admin.site.register(Sub_region)
admin.site.register(Country, CountryAdmin)
admin.site.register(Sector)
admin.site.register(Methodology, MethodologyAdmin)
admin.site.register(Organisation)
admin.site.register(Buyer, BuyerAdmin)
admin.site.register(PDD_consultant, PDDAdmin)
admin.site.register(Status)
admin.site.register(Type)
admin.site.register(Sub_type, SubtypeAdmin)
admin.site.register(Validator, ValidatorAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(Credit, CreditAdmin)
