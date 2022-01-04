from django.urls import path
from .views import medicines, create, edit, delete, companies, companyEdit, companyCreate, companyDelete, MedicineList, MedicineCompanyList

app_name='medicines'

urlpatterns = [
    path('', medicines, name='medicines'),
    path('list', MedicineList.as_view(), name='list'),
    path('create', create, name='create'),
    path('companies', companies, name='companies'),
    path('companies/list', MedicineCompanyList.as_view(), name='company_list'),
    path('companies/create', companyCreate, name='company_create'),

    path('companies/<str:id>', companyEdit, name='company_detail'),
    path('companies/<str:id>/delete', companyDelete, name='company_delete'),
    path('<str:id>', edit, name='edit'),
    path('<str:id>/delete', delete, name='delete'),
    
]
