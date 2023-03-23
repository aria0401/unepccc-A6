from django.test import TestCase, Client
from django.urls import reverse, resolve
from unepccc_app.models import Project, Methodology, Buyer, PDD_consultant, Sector, Country, Status, Sub_type, Type, Organisation, Region, Validator, Sub_region
from unepccc_app.views import index_view, project_list, project_detail, methodology_list, search_project, select_sector, analysis, projects_by_methodology, buyer_list



class TestViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.index_url = reverse('unepccc_app:index-view')
        self.project_list_url = reverse('unepccc_app:project-view')
        self.methodology_list_url = reverse('unepccc_app:methodology-view')

        region = Region.objects.create(
            name='test region'
        )
        sub_region = Sub_region.objects.create(
            name='test sub_region',
            region=region
        )
        organisation = Organisation.objects.create(
            name='test organisation'
        )
        country = Country.objects.create(
            name='test country',
            sub_region=sub_region
        )
        status = Status.objects.create(
            id=1,
            name='test status'
        )
        type = Type.objects.create(
            name='test type'
        )
        sub_type = Sub_type.objects.create(
            name='test sub_type',
            type=type
        )
        sector = Sector.objects.create(
            id=1,
            name='test sector'
        )
        sector = Sector.objects.create(
            id=2,
            name='test sector 2'
        )
        buyer = Buyer.objects.create(
            name='test buyer',
            organisation=organisation,
            country=country
        )
        pdd_consultant = PDD_consultant.objects.create(
            name='test pdd_consultant',
            organisation=organisation,
            country=country
        )
        methodology = Methodology.objects.create(
            id=1,
            name='test methodology',
            sector=sector
        )
        validator = Validator.objects.create(
            name='test validator',
            short_name='test short_name',
            country=country
        )

        project = Project.objects.create(
            id=1,
            name='test project Daniel',
            methodology=methodology,
            buyer=buyer,
            pdd_consultant=pdd_consultant,
            status=status,
            sub_type=sub_type,
            country=country,
            validator=validator,
            project_id='DANIEL TEST-ID',
            project_ref='test project_ref',
            credit_start='2020-01-01',

        )
        self.project = project


    def test_index_view_get(self):
        response = self.client.get(self.index_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'unepccc_app/index.html')


    def test_project_list_get(self):
        response = self.client.get(self.project_list_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'unepccc_app/project.html')


    def test_project_list_htmx(self):
        headers = {'HTTP_HX-Request': 'true'}
        response = self.client.get(self.project_list_url, **headers)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'unepccc_app/partials/project_list.html')


    def test_project_detail_get(self):
        project = self.project
        response = self.client.get(reverse('unepccc_app:project-details', args=[project.id]))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'unepccc_app/project_detail.html')


    def test_methodology_list(self):
        response = self.client.get(self.methodology_list_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'unepccc_app/methodology.html')


    def test_methodology_detail(self):
        methodology = self.project.methodology
        response = self.client.get(reverse('unepccc_app:methodology-details', args=[methodology.id]))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'unepccc_app/methodology_detail.html')


    def test_buyer_list(self):
        response = self.client.get(reverse('unepccc_app:buyers-view'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'unepccc_app/buyers.html')


    def test_consultant_list(self):
        response = self.client.get(reverse('unepccc_app:consultants-view'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'unepccc_app/consultants.html')


    def test_analysis(self):
        response = self.client.get(reverse('unepccc_app:projects-by-region-view'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'unepccc_app/analysis.html')


    def test_analysis_htmx(self):
        headers = {'HTTP_HX-Request': 'true'}
        response = self.client.get(reverse('unepccc_app:projects-by-region-view'), **headers)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'unepccc_app/partials/bar_chart.html')


    def test_projects_by_methodology(self):
        response = self.client.get(reverse('unepccc_app:projects-by-methodology-view'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'unepccc_app/projects_by_methodology.html')


    def test_projects_by_methodology_htmx(self):
        headers = {'HTTP_HX-Request': 'true'}
        response = self.client.get(reverse('unepccc_app:projects-by-methodology-view'), **headers)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'unepccc_app/partials/bar_chart.html')


    def test_credits_by_sector(self):
        response = self.client.get(reverse('unepccc_app:credits-by-sector-view'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'unepccc_app/credits_by_sector.html')
