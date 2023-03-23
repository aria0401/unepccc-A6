from django.test import TestCase
from unepccc_app.models import Region, Sub_region, Country, Buyer, Organisation


class TestModels(TestCase):

    def test_sub_regions(self):
        region = Region.objects.create(
            name='test region'
        )
        sub_region = Sub_region.objects.create(
            name='test sub_region',
            region=region
        )
        self.assertEquals(sub_region.name, 'test sub_region')
        self.assertEquals(sub_region.region, region)
        self.assertEquals(sub_region.__str__(), 'test sub_region')


    def test_regions_filter(self):
        region = Region.objects.create(
            name='test region'
        )
        sub_region = Sub_region.objects.create(
            name='test sub_region',
            region=region
        )
        self.assertEquals(region.sub_regions.count(), 1)
        self.assertEquals(region.sub_regions.first(), sub_region)
        self.assertEquals(region.sub_regions.first().name, 'test sub_region')
        self.assertEquals(region.sub_regions.first().region, region)

    def test_region_countries_filter(self):
        region = Region.objects.create(
            name='test region'
        )
        sub_region = Sub_region.objects.create(
            name='test sub_region',
            region=region
        )
        country = Country.objects.create(
            name='test country',
            sub_region=sub_region
        )
        self.assertEquals(region.countries.count(), 1)
        self.assertEquals(region.countries.first(), country)
        self.assertEquals(region.countries.first().name, 'test country')
        self.assertEquals(region.countries.first().sub_region.region, region)


    def test_sub_regions_countries_filter(self):
        region = Region.objects.create(
            name='test region'
        )
        sub_region = Sub_region.objects.create(
            name='test sub_region',
            region=region
        )
        country = Country.objects.create(
            name='test country',
            sub_region=sub_region
        )
        self.assertEquals(sub_region.countries.count(), 1)
        self.assertEquals(sub_region.countries.first(), country)
        self.assertEquals(sub_region.countries.first().name, 'test country')
        self.assertEquals(sub_region.countries.first().sub_region, sub_region)


    def test_buyer(self):
        organisation = Organisation.objects.create(
            name='test organisation'
        )
        region = Region.objects.create(
            name='test region'
        )
        sub_region = Sub_region.objects.create(
            name='test sub_region',
            region=region
        )
        country = Country.objects.create(
            name='test country',
            sub_region=sub_region
        )

        buyer = Buyer.objects.create(
            name='test buyer',
            organisation=organisation,
            country=country
        )
        self.assertEquals(buyer.name, 'test buyer')
        self.assertEquals(buyer.organisation, organisation)
        self.assertEquals(buyer.country, country)
        self.assertEquals(buyer.__str__(), 'test buyer')
