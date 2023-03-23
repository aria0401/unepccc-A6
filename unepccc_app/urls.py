from django.urls import path
from . import views

app_name = 'unepccc_app'

urlpatterns = [
    path('', views.index_view, name='index-view'),
    path('projects/', views.project_list, name='project-view'),
    path('projects/<int:pk>', views.project_detail, name='project-details'),
    path('methodologies/', views.methodology_list, name='methodology-view'),
    path('methodologies/<int:pk>', views.methodology_detail,
         name='methodology-details'),
    path('analysis/', views.analysis, name='projects-by-region-view'),
    path('analysis/1/', views.projects_by_methodology, name='projects-by-methodology-view'),
    path('analysis/2/', views.credits_by_sector, name='credits-by-sector-view'),
    path('buyers/', views.buyer_list, name='buyers-view'),
    path('consultants/', views.consultant_list, name='consultants-view'),
]

htmx_urlpatterns = [
    path('select-sector/', views.select_sector, name="select-sector"),
    path('search-project/<int:pk>', views.search_project, name="search-project"),
]

urlpatterns += htmx_urlpatterns
