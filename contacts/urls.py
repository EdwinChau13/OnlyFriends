from django.urls import path
from . import views

urlpatterns = [
    path('', views.contact, name='contact'),
    path('import/', views.import_csv, name='import_csv'),
    path('export/', views.export_csv, name='export_csv'),
    path('add/', views.add_record, name='add_record'),
    path('<int:person_id>/preference/', views.preference, name='preference'),
    path('<int:person_id>/availability/', views.availability, name='availability'),
    path('<int:person_id>/edit/', views.edit_record, name='edit_person'),
    path('<int:person_id>/delete/', views.delete_record, name='delete_person'),
]