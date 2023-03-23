from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from django.db.models import Count, Sum

from bokeh.models import ColumnDataSource, HoverTool, Legend
from bokeh.models.tools import PanTool, ResetTool, SaveTool
from bokeh.embed import components
from bokeh.plotting import figure
from bokeh.resources import INLINE
from bokeh.palettes import Spectral5
from bokeh.transform import factor_cmap, dodge

from .filters import ProjectFilter
from .models import Project, Sector, Methodology, Region, Status, Credit, Buyer, PDD_consultant

from csp.decorators import csp_exempt


@csp_exempt
def index_view(request):
    return render(request, 'unepccc_app/index.html', {'message': 'index view'})


@csp_exempt
def project_list(request):
    project_filter = ProjectFilter(request.GET, Project.objects.all().annotate(
        credits=Sum('credit__credit')).order_by('name'))

    context = {
        'form': project_filter.form,
        'projects': project_filter.qs
    }

    if request.htmx:
        template_url = True
        message = "We can't find any projects that match your search."
        context = {
            'form': project_filter.form,
            'projects': project_filter.qs,
            'template_url': template_url,
            'message': message
        }
        return render(request, 'unepccc_app/partials/project_list.html', context)
    return render(request, 'unepccc_app/project.html', context)


@csp_exempt
def project_detail(request, pk):
    project = get_object_or_404(Project, pk=pk)
    credits = Credit.objects.filter(project=pk)
    credit_sum = Project.objects.annotate(
        total_credits=Sum('credit__credit')).get(pk=pk)
    total_credits = credit_sum.total_credits
    context = {'project': project, 'credits': credits,
               'total_credits': total_credits}
    return render(request, 'unepccc_app/project_detail.html', context)


@csp_exempt
def methodology_list(request):
    sectors = Sector.objects.all()
    context = {'sectors': sectors}
    return render(request, 'unepccc_app/methodology.html', context)


@csp_exempt
def methodology_detail(request, pk):
    methodology = get_object_or_404(Methodology, pk=pk)
    context = {'methodology': methodology}
    return render(request, 'unepccc_app/methodology_detail.html', context)


@csp_exempt
def buyer_list(request):
    buyers = Buyer.objects.all()
    context = {'buyers': buyers}
    return render(request, 'unepccc_app/buyers.html', context)


@csp_exempt
def consultant_list(request):
    consultants = PDD_consultant.objects.all()
    context = {'consultants': consultants}
    return render(request, 'unepccc_app/consultants.html', context)


# HTMX functions
@csp_exempt
def select_sector(request):
    sector = request.GET.get('sector')
    if sector == 'all':
        sectors = Sector.objects.all()
        context = {'sectors': sectors}
        return render(request, 'unepccc_app/partials/methodology_list.html', context)
    else:
        sector = Sector.objects.get(pk=sector)
        context = {'sector': sector}
        return render(request, 'unepccc_app/partials/methodology_list_selected.html', context)


@csp_exempt
def search_project(request, pk):
    search_text = request.POST.get('search')

    projects = Project.objects.filter(methodology=pk) & Project.objects.filter(
        Q(name__icontains=search_text) |
        Q(project_id__icontains=search_text) |
        Q(country__name__icontains=search_text) |
        Q(status__name__icontains=search_text)
    )

    context = {'projects': projects}
    if projects.count() == 0:
        message = "We can't find any projects that match your search."
        context = {
            'projects': projects,
            'message': message
        }
    return render(request, 'unepccc_app/partials/project_list.html', context)


@csp_exempt
def analysis(request):

    projects = Project.objects.all().values('country__sub_region__region__name').annotate(
        count=Count('country__sub_region__region__name')).order_by('count').reverse()

    region_names = [r['country__sub_region__region__name'] for r in projects]
    region_projects = [r['count'] for r in projects]

    data = {'region_names': region_names, 'region_projects': region_projects}
    cds = ColumnDataSource(data=data)

    fig = figure(x_range=region_names, y_range=(0, max(region_projects) + 1), height=450,
                 title=f'{"Number of projects by Region"}', tools=[SaveTool(), PanTool(), ResetTool()])

    fig.title.align = 'left'
    fig.title.text_font_size = '1.7em'
    fig.title.text_font_style = 'normal'
    fig.title.text_color = '#01465F'
    fig.border_fill_color = "whitesmoke"
    fig.min_border = 60
    fig.yaxis.axis_label = "Number of projects"
    fig.y_range.start = 0
    fig.toolbar.autohide = True
    fig.toolbar.logo = None
    fig.sizing_mode = "stretch_width"
    fig.axis.minor_tick_line_color = None

    tooltips = [
        ('Region', '@region_names'),
        ('Projects', '@region_projects')
    ]
    fig.vbar(source=cds, x='region_names',
             top='region_projects', width=0.5)

    fig.xgrid.grid_line_color = None
    fig.outline_line_color = None

    fig.add_tools(HoverTool(tooltips=tooltips))

    script, div = components(fig)

    context = {'resources': INLINE.render(), 'script': script,
               'div': div}

    if request.htmx:
        return render(request, 'unepccc_app/partials/bar_chart.html', context)
    return render(request, 'unepccc_app/analysis.html', context)


@csp_exempt
def projects_by_methodology(request):
    status_list = Status.objects.all()
    default_status = status_list.get(pk=1)
    status = request.GET.get('status', default_status)
    count = int(request.GET.get('count', 5))
    projects = Project.objects.filter(status=status).values('methodology__methodology_id').annotate(
        count=Count('methodology')).order_by('count').reverse()[:count]

    methodologies = [r['methodology__methodology_id'] for r in projects]
    projects = [r['count'] for r in projects]

    data = {'methodologies': methodologies, 'projects': projects}
    cds = ColumnDataSource(data=data)

    method_cmap = factor_cmap(
        'methodologies', palette=Spectral5, factors=methodologies)
    fig = figure(x_range=methodologies, y_range=(0, max(projects) + 1),
                 height=450, title=f'{"Number of projects by Methodology and Status"}')
    fig.title.align = 'left'
    fig.title.text_font_size = '1.7em'
    fig.title.text_font_style = 'normal'
    fig.title.text_color = '#01465F'
    fig.border_fill_color = "whitesmoke"
    fig.min_border = 60
    fig.yaxis.axis_label = "Number of projects"
    fig.y_range.start = 0
    fig.toolbar.autohide = True
    fig.toolbar.logo = None
    fig.sizing_mode = "stretch_width"
    # fig.axis.minor_tick_in = -3
    # fig.axis.minor_tick_out = 6
    fig.axis.minor_tick_line_color = None

    tooltips = [
        ('Methodology', '@methodologies'),
        ('Projects', '@projects')
    ]
    fig.vbar(source=cds, x='methodologies',
             top='projects', width=0.5, line_color=method_cmap, fill_color=method_cmap)

    fig.xgrid.grid_line_color = None
    fig.outline_line_color = None

    fig.add_tools(HoverTool(tooltips=tooltips))

    script, div = components(fig)
    context = {'resources': INLINE.render(), 'script': script,
               'div': div, 'status': status_list, 'status_selected': status, 'count': count}
    if request.htmx:
        return render(request, 'unepccc_app/partials/bar_chart.html', context)
    return render(request, 'unepccc_app/projects_by_methodology.html', context)


@csp_exempt
def credits_by_sector(request):
    projects = Project.objects.all().values('methodology__sector__name').annotate(
        count=Count('methodology__sector__name'), credits_2025=Sum('expected_CERs'), total_issuances=Sum('credit__credit')).order_by('count').reverse()[:3]

    sectors = [s['methodology__sector__name'] for s in projects]
    credits_2025 = [c['credits_2025'] for c in projects]
    total_issuances = [c['total_issuances'] for c in projects]

    data = {'sectors': sectors,
            'CERs 2025': credits_2025,
            'Total issuance': total_issuances}

    source = ColumnDataSource(data=data)

    fig = figure(x_range=sectors, height=450, title="CERs by Sector")

    v1 = fig.vbar(x=dodge('sectors', -0.25, range=fig.x_range),
                  top='CERs 2025', source=source, width=0.2, color="#0072B2")
    v2 = fig.vbar(x=dodge('sectors', 0.0, range=fig.x_range),
                  top='Total issuance', source=source, width=0.2, color="#E69F00")

    fig.title.align = 'left'
    fig.title.text_font_size = '1.7em'
    fig.title.text_font_style = 'normal'
    fig.title.text_color = '#01465F'
    fig.border_fill_color = "whitesmoke"
    fig.min_border = 60
    fig.y_range.start = 0
    fig.x_range.range_padding = 0.1
    fig.xgrid.grid_line_color = None
    # fig.axis.minor_tick_line_color = None
    fig.outline_line_color = None
    fig.sizing_mode = "stretch_width"
    fig.toolbar.autohide = True
    fig.toolbar.logo = None

    legend = Legend(items=[
        ("CERs 2025",   [v1]),
        ("Total issuance",   [v2]),
    ], location="center", orientation="horizontal")

    fig.add_layout(legend, 'below')

    script, div = components(fig)
    context = {'resources': INLINE.render(), 'script': script, 'div': div}

    return render(request, 'unepccc_app/credits_by_sector.html', context)
